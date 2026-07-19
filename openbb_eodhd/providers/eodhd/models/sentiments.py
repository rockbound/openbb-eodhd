"""Fetcher for sentiments — generated from spec.

Hits ``https://eodhd.com/api/sentiments`` via HTTP GET.
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


class SentimentsQueryParams(QueryParams):
    """Query parameters for sentiments.

    Parameters
    ----------
    s : str
        Comma-separated list of ticker codes to retrieve sentiment data for (e.g., 'btc-usd.cc,aapl.us').
    from_ : str, optional
        Start date for sentiment data (YYYY-MM-DD).
    to : str, optional
        End date for sentiment data (YYYY-MM-DD).
    fmt : Literal['json'], optional
        Response format (only 'json' is supported). Choices: json.
    """

    s: str = Field(
        description="Comma-separated list of ticker codes to retrieve sentiment data for (e.g., 'btc-usd.cc,aapl.us').",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for sentiment data (YYYY-MM-DD).",
    )
    to: str | None = Field(
        default=None,
        description="End date for sentiment data (YYYY-MM-DD).",
    )
    fmt: Literal["json"] | None = Field(
        default=None,
        description="Response format (only 'json' is supported). Choices: json.",
    )


class SentimentsDataTickerValueItem(BaseModel):
    """SentimentsDataTickerValueItem.

    Parameters
    ----------
    date : datetime.date
    count : int
        Number of articles or mentions analyzed for the given date.
    normalized : float
        Normalized sentiment score, where -1 represents a very negative sentiment, 0 is neutral, and 1 is very positive.
    """

    date: datetime.date = Field(description="")
    count: int = Field(
        description="Number of articles or mentions analyzed for the given date.",
    )
    normalized: float = Field(
        description="Normalized sentiment score, where -1 represents a very negative sentiment, 0 is neutral, and 1 is very positive.",
    )


class SentimentsData(Data):
    """Response row for sentiments.

    Parameters
    ----------
    ticker : dict[str, list[SentimentsDataTickerValueItem]], optional
    """

    ticker: dict[str, list[SentimentsDataTickerValueItem]] | None = Field(
        default=None,
        description="",
    )

    @field_validator("ticker", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class SentimentsFetcher(Fetcher[SentimentsQueryParams, list[SentimentsData]]):
    """Retrieve sentiment analysis for financial news related to specified tickers."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SentimentsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SentimentsQueryParams
            Validated query parameters.
        """
        return SentimentsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SentimentsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/sentiments and split rows from metadata.

        Parameters
        ----------
        query : SentimentsQueryParams
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
        _path = "/sentiments"

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
        query: SentimentsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SentimentsData] | AnnotatedResult[list[SentimentsData]]:
        """Type the unpacked rows as SentimentsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SentimentsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SentimentsData] | AnnotatedResult[list[SentimentsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SentimentsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
