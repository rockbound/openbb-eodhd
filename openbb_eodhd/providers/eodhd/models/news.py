"""Fetcher for news — generated from spec.

Hits ``https://eodhd.com/api/news`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field, field_validator

from ....utils import safe_json_loads, unpack_response


class NewsQueryParams(QueryParams):
    """Query parameters for news.

    Parameters
    ----------
    s : str, optional
        Ticker code to get news for (e.g., 'AAPL.US'). Required if 't' is not provided.
    t : str, optional
        Tag to get news on a given topic. Required if 's' is not provided.
    from_ : str, optional
        Start date for news data (YYYY-MM-DD).
    to : str, optional
        End date for news data (YYYY-MM-DD).
    limit : int, optional
        The number of results to return. (default: 50)
    offset : int, optional
        The offset of the data. (default: 0)
    fmt : Literal['json'], optional
        Response format (e.g., 'json'). Choices: json.
    """

    s: str | None = Field(
        default=None,
        description="Ticker code to get news for (e.g., 'AAPL.US'). Required if 't' is not provided.",
    )
    t: str | None = Field(
        default=None,
        description="Tag to get news on a given topic. Required if 's' is not provided.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for news data (YYYY-MM-DD).",
    )
    to: str | None = Field(
        default=None,
        description="End date for news data (YYYY-MM-DD).",
    )
    limit: int | None = Field(
        default=50,
        description="The number of results to return.",
    )
    offset: int | None = Field(default=0, description="The offset of the data.")
    fmt: Literal["json"] | None = Field(
        default=None,
        description="Response format (e.g., 'json'). Choices: json.",
    )


class NewsDataSentiment(BaseModel):
    """NewsDataSentiment.

    Parameters
    ----------
    polarity : float, optional
    neg : float, optional
    neu : float, optional
    pos : float, optional
    """

    polarity: float | None = Field(default=None, description="")
    neg: float | None = Field(default=None, description="")
    neu: float | None = Field(default=None, description="")
    pos: float | None = Field(default=None, description="")


class NewsData(Data):
    """Response row for news.

    Parameters
    ----------
    date : datetime.datetime, optional
    title : str, optional
    content : str, optional
    link : str, optional
    symbols : list[str], optional
    tags : list[str], optional
    sentiment : NewsDataSentiment, optional
        Inner fields: polarity (float), neg (float), neu (float), pos (float).
    """

    date: datetime.datetime | None = Field(default=None, description="")
    title: str | None = Field(default=None, description="")
    content: str | None = Field(default=None, description="")
    link: str | None = Field(default=None, description="")
    symbols: list[str] | None = Field(default=None, description="")
    tags: list[str] | None = Field(default=None, description="")
    sentiment: NewsDataSentiment | None = Field(
        default=None,
        description="Inner fields: polarity (float), neg (float), neu (float), pos (float).",
    )

    @field_validator("sentiment", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class NewsFetcher(Fetcher[NewsQueryParams, list[NewsData]]):
    """Retrieve financial news articles for a specific company ticker or topic."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> NewsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        NewsQueryParams
            Validated query parameters.
        """
        return NewsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: NewsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/news and split rows from metadata.

        Parameters
        ----------
        query : NewsQueryParams
            Validated query parameters.
        credentials : dict[str, str] | None
            Provider credentials registered on the ``Provider`` instance.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        dict[str, Any]
            ``{'rows': [...], 'metadata': {...}}`` — single-element list and single-key envelope wrappers are stripped at the response boundary, scalar fields beside the data array become metadata.
        """
        _creds = credentials or {}
        _cred_api_token = _creds.get("eodhd_api_token", "")
        _path = "/news"

        _query_dict = query.model_dump(by_alias=True, exclude_none=True)
        if _cred_api_token:
            _query_dict["api_token"] = _cred_api_token
        _query_string = get_querystring(_query_dict, [])
        _url = f"https://eodhd.com/api{_path}" + ("?" + _query_string if _query_string else "")

        _headers: dict[str, str] = {}

        _method = "GET"
        _request_kwargs: dict[str, Any] = {}
        async with await get_async_requests_session() as _session:
            async with await _session.request(
                _method, _url, headers=_headers, **_request_kwargs
            ) as _resp:
                _ct = (_resp.headers.get("Content-Type") or "").lower()
                _text = await _resp.text()
                if _resp.status >= 400:
                    raise OpenBBError(f"HTTP {_resp.status} from {_url}: {_text[:500]}")
                if "json" in _ct or _text.lstrip().startswith(("{", "[")):
                    try:
                        _payload = safe_json_loads(_text)
                    except ValueError as _exc:
                        raise OpenBBError(
                            f"Upstream {_url} returned malformed JSON: {_exc}"
                        ) from _exc
                else:
                    return {"rows": [{"content": _text, "content_type": _ct}], "metadata": {}}
        _rows, _metadata = unpack_response(_payload)
        return {"rows": _rows, "metadata": _metadata}

    @staticmethod
    def transform_data(
        query: NewsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[NewsData] | AnnotatedResult[list[NewsData]]:
        """Type the unpacked rows as NewsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : NewsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[NewsData] | AnnotatedResult[list[NewsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [NewsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"date": {"format": "date-time"}, "link": {"format": "uri"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
