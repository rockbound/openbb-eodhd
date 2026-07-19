"""Fetcher for search — generated from spec.

Hits ``https://eodhd.com/api/search/{query}`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field

from ....utils import safe_json_loads, unpack_response


class SearchQueryParams(QueryParams):
    """Query parameters for search.

    Parameters
    ----------
    query : str
        The search query (e.g., 'AAPL', 'Amazon', or ISIN 'US3453708600').
    fmt : Literal['json', 'xml'], optional
        Response format (e.g., 'json'). Choices: json, xml. (default: 'json')
    limit : int, optional
        Limit the number of results returned.
    type : Literal['all', 'stock', 'etf', 'fund', 'bond', 'index', 'crypto'], optional
        Filter by security type. Choices: all, stock, etf, fund, bond, index, crypto.
    exchange : str, optional
        Filter by exchange code (e.g., 'US', 'LSE').
    bonds_only : Literal[0, 1], optional
        Set to 1 to return bonds only. Choices: 0, 1.
    """

    query: str = Field(
        description="The search query (e.g., 'AAPL', 'Amazon', or ISIN 'US3453708600').",
    )
    fmt: Literal["json", "xml"] | None = Field(
        default="json",
        description="Response format (e.g., 'json'). Choices: json, xml.",
    )
    limit: int | None = Field(
        default=None,
        description="Limit the number of results returned.",
    )
    type: Literal["all", "stock", "etf", "fund", "bond", "index", "crypto"] | None = Field(
        default=None,
        description="Filter by security type. Choices: all, stock, etf, fund, bond, index, crypto.",
    )
    exchange: str | None = Field(
        default=None,
        description="Filter by exchange code (e.g., 'US', 'LSE').",
    )
    bonds_only: Literal[0, 1] | None = Field(
        default=None,
        description="Set to 1 to return bonds only. Choices: 0, 1.",
    )


class SearchData(Data):
    """Response row for search.

    Parameters
    ----------
    Code : str, optional
    Exchange : str, optional
    Name : str, optional
    Type : str, optional
    Country : str, optional
    Currency : str, optional
    ISIN : str, optional
    previousClose : float, optional
    previousCloseDate : datetime.date, optional
    """

    Code: str | None = Field(default=None, description="")
    Exchange: str | None = Field(default=None, description="")
    Name: str | None = Field(default=None, description="")
    Type: str | None = Field(default=None, description="")
    Country: str | None = Field(default=None, description="")
    Currency: str | None = Field(default=None, description="")
    ISIN: str | None = Field(default=None, description="")
    previousClose: float | None = Field(default=None, description="")
    previousCloseDate: datetime.date | None = Field(default=None, description="")


class SearchFetcher(Fetcher[SearchQueryParams, list[SearchData]]):
    """Search for stocks, companies, or ISINs by a query (e.g., company name, stock symbol, or ISIN)."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SearchQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SearchQueryParams
            Validated query parameters.
        """
        return SearchQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SearchQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/search/{query} and split rows from metadata.

        Parameters
        ----------
        query : SearchQueryParams
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
        _path = f"/search/{query.query}"

        _query_dict = query.model_dump(by_alias=True, exclude={"query"}, exclude_none=True)
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
        query: SearchQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SearchData] | AnnotatedResult[list[SearchData]]:
        """Type the unpacked rows as SearchData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SearchQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SearchData] | AnnotatedResult[list[SearchData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SearchData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"previousCloseDate": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
