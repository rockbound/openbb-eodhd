"""Fetcher for v1_1.fundamentals — generated from spec.

Hits ``https://eodhd.com/api/v1.1/fundamentals/{ticker}`` via HTTP GET.
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


class V11FundamentalsQueryParams(QueryParams):
    """Query parameters for v1_1.fundamentals.

    Parameters
    ----------
    ticker : str
        The ticker symbol in the format SYMBOL.EXCHANGE, e.g., 'AAPL.US' for Apple Inc. on NASDAQ.
    filter : str, optional
        Filter parameter to specify data section and optional sub-sections, e.g., `Financials::Balance_Sheet::quarterly::2024-06-30`. Supported sections include General, Highlights, Valuation, SharesStats, Technicals, SplitsDividends, AnalystRatings, Holders, InsiderTransactions, ESGScores, outstandingShares, Earnings, and Financials. When omitted, returns all sections.
    historical : Literal[0, 1], optional
        Set to 1 to return historical data for certain sections (e.g., outstandingShares). Choices: 0, 1.
    from_ : str, optional
        Start date for historical data in 'YYYY-MM-DD' format.
    to : str, optional
        End date for historical data in 'YYYY-MM-DD' format.
    version : int, optional
        API version for response format.
    no_cache : Literal[0, 1], optional
        Set to 1 to bypass cache and get fresh data. Choices: 0, 1.
    """

    ticker: str = Field(
        description="The ticker symbol in the format SYMBOL.EXCHANGE, e.g., 'AAPL.US' for Apple Inc. on NASDAQ.",
    )
    filter: str | None = Field(
        default=None,
        description="Filter parameter to specify data section and optional sub-sections, e.g., `Financials::Balance_Sheet::quarterly::2024-06-30`. Supported sections include General, Highlights, Valuation, SharesStats, Technicals, SplitsDividends, AnalystRatings, Holders, InsiderTransactions, ESGScores, outstandingShares, Earnings, and Financials. When omitted, returns all sections.",
    )
    historical: Literal[0, 1] | None = Field(
        default=None,
        description="Set to 1 to return historical data for certain sections (e.g., outstandingShares). Choices: 0, 1.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for historical data in 'YYYY-MM-DD' format.",
    )
    to: str | None = Field(
        default=None,
        description="End date for historical data in 'YYYY-MM-DD' format.",
    )
    version: int | None = Field(
        default=None,
        description="API version for response format.",
    )
    no_cache: Literal[0, 1] | None = Field(
        default=None,
        description="Set to 1 to bypass cache and get fresh data. Choices: 0, 1.",
    )


class V11FundamentalsData(Data):
    """Response row for v1_1.fundamentals.

    Parameters
    ----------
    date : datetime.date, optional
    ownerName : str, optional
    transactionCode : str, optional
    transactionAmount : float, optional
    """

    date: datetime.date | None = Field(default=None, description="")
    ownerName: str | None = Field(default=None, description="")
    transactionCode: str | None = Field(default=None, description="")
    transactionAmount: float | None = Field(default=None, description="")


class V11FundamentalsFetcher(Fetcher[V11FundamentalsQueryParams, list[V11FundamentalsData]]):
    """Fetches various sections of fundamental data for a given stock symbol using API v1.1. This version differs from v1 in the Earnings Trend section, which is split into Quarterly and Annual sub-objects with an additional "quarter" field on quarterly items. Use filters to specify the data section and sub-sections, such as Financials::Balance_Sheet::quarterly::2024-06-30 for quarterly Balance Sheet data."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> V11FundamentalsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        V11FundamentalsQueryParams
            Validated query parameters.
        """
        return V11FundamentalsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: V11FundamentalsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/v1.1/fundamentals/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : V11FundamentalsQueryParams
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
        _path = f"/v1.1/fundamentals/{query.ticker}"

        _query_dict = query.model_dump(by_alias=True, exclude={"ticker"}, exclude_none=True)
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
        query: V11FundamentalsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[V11FundamentalsData] | AnnotatedResult[list[V11FundamentalsData]]:
        """Type the unpacked rows as V11FundamentalsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : V11FundamentalsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[V11FundamentalsData] | AnnotatedResult[list[V11FundamentalsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [V11FundamentalsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"date": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
