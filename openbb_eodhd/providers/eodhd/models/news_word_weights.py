"""Fetcher for news-word-weights — generated from spec.

Hits ``https://eodhd.com/api/news-word-weights`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field

from ....utils import safe_json_loads, unpack_response


class NewsWordWeightsQueryParams(QueryParams):
    """Query parameters for news-word-weights.

    Parameters
    ----------
    s : str
        Ticker to analyze, e.g., AAPL or AAPL.US.
    filter_date_from_ : str, optional
        Start date (YYYY-MM-DD).
    filter_date_to_ : str, optional
        End date (YYYY-MM-DD). Prefer this over the legacy alias `filter[to]`.
    filter_to_ : str, optional
        Deprecated alias for `filter[date_to]` (YYYY-MM-DD). Use only one of these parameters.
    page_limit_ : int, optional
        Number of top words to return. (default: 10)
    fmt : Literal['json', 'xml'], optional
        Response format. Choices: json, xml. (default: 'json')
    """

    s: str = Field(description="Ticker to analyze, e.g., AAPL or AAPL.US.")
    filter_date_from_: str | None = Field(
        default=None,
        alias="filter[date_from]",
        description="Start date (YYYY-MM-DD).",
    )
    filter_date_to_: str | None = Field(
        default=None,
        alias="filter[date_to]",
        description="End date (YYYY-MM-DD). Prefer this over the legacy alias `filter[to]`.",
    )
    filter_to_: str | None = Field(
        default=None,
        alias="filter[to]",
        description="Deprecated alias for `filter[date_to]` (YYYY-MM-DD). Use only one of these parameters.",
    )
    page_limit_: int | None = Field(
        default=10,
        alias="page[limit]",
        description="Number of top words to return.",
    )
    fmt: Literal["json", "xml"] | None = Field(
        default="json",
        description="Response format. Choices: json, xml.",
    )


class NewsWordWeightsDataMeta(BaseModel):
    """NewsWordWeightsDataMeta.

    Parameters
    ----------
    news_found : int
    news_processed : int
    """

    news_found: int = Field(description="")
    news_processed: int = Field(description="")


class NewsWordWeightsDataLinks(BaseModel):
    """NewsWordWeightsDataLinks.

    Parameters
    ----------
    next : str
        URL for the next page, or null.
    """

    next: str | None = Field(description="URL for the next page, or null.")


class NewsWordWeightsData(Data):
    """Response row for news-word-weights.

    Parameters
    ----------
    data : dict[str, float]
        Map of keyword Ã¢ÂÂ weight.
    meta : NewsWordWeightsDataMeta
        Inner fields: news_found (int), news_processed (int).
    links : NewsWordWeightsDataLinks
        Inner fields: next (Any).
    """

    data: dict[str, float] = Field(description="Map of keyword Ã¢ÂÂ weight.")
    meta: NewsWordWeightsDataMeta = Field(
        description="Inner fields: news_found (int), news_processed (int).",
    )
    links: NewsWordWeightsDataLinks = Field(description="Inner fields: next (Any).")


class NewsWordWeightsFetcher(Fetcher[NewsWordWeightsQueryParams, list[NewsWordWeightsData]]):
    """Returns the most relevant words from financial news for the given ticker and period, with weights (frequency ? significance)."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> NewsWordWeightsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        NewsWordWeightsQueryParams
            Validated query parameters.
        """
        return NewsWordWeightsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: NewsWordWeightsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/news-word-weights and split rows from metadata.

        Parameters
        ----------
        query : NewsWordWeightsQueryParams
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
        _path = "/news-word-weights"

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
        query: NewsWordWeightsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[NewsWordWeightsData] | AnnotatedResult[list[NewsWordWeightsData]]:
        """Type the unpacked rows as NewsWordWeightsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : NewsWordWeightsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[NewsWordWeightsData] | AnnotatedResult[list[NewsWordWeightsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [NewsWordWeightsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"data": {"description": "Map of keyword Ã¢ÂÂ weight"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
