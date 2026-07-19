"""Fetcher for screener — generated from spec.

Hits ``https://eodhd.com/api/screener`` via HTTP GET.
"""

import datetime
from typing import Any

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field

from ....utils import safe_json_loads, unpack_response


class ScreenerQueryParams(QueryParams):
    """Query parameters for screener.

    Parameters
    ----------
    filters : str, optional
        Filters to apply, structured as nested arrays (e.g., [["field", "operation", value], ...]).
    signals : str, optional
        Signals to filter tickers by pre-calculated fields (e.g., 200d_new_hi, bookvalue_pos).
    sort : str, optional
        Sorts results by a specified field in ascending or descending order (e.g., market_capitalization.desc).
    limit : int, optional
        Number of results per request. Minimum 1, maximum 500. Default is 50. (default: 50)
    offset : int, optional
        Data offset for paginating results. Minimum 0, maximum 999. Default is 0. (default: 0)
    """

    filters: str | None = Field(
        default=None,
        description='Filters to apply, structured as nested arrays (e.g., [["field", "operation", value], ...]).',
    )
    signals: str | None = Field(
        default=None,
        description="Signals to filter tickers by pre-calculated fields (e.g., 200d_new_hi, bookvalue_pos).",
    )
    sort: str | None = Field(
        default=None,
        description="Sorts results by a specified field in ascending or descending order (e.g., market_capitalization.desc).",
    )
    limit: int | None = Field(
        default=50,
        description="Number of results per request. Minimum 1, maximum 500. Default is 50.",
    )
    offset: int | None = Field(
        default=0,
        description="Data offset for paginating results. Minimum 0, maximum 999. Default is 0.",
    )


class ScreenerData(Data):
    """Response row for screener.

    Parameters
    ----------
    code : str, optional
        Ticker symbol.
    name : str, optional
        Company name.
    last_day_data_date : datetime.date, optional
        Date of the latest data.
    adjusted_close : float, optional
        Latest adjusted close price.
    refund_1d : float, optional
        Refund value for the last day.
    refund_1d_p : float, optional
        Refund percentage change for the last day.
    refund_5d : float, optional
        Refund value for the last 5 days.
    refund_5d_p : float, optional
        Refund percentage change for the last 5 days.
    exchange : str, optional
        Exchange code.
    currency_symbol : str, optional
        Currency symbol.
    market_capitalization : int, optional
        Market capitalization in USD.
    earnings_share : float, optional
        Earnings per share (EPS).
    dividend_yield : float, optional
        Dividend yield percentage.
    sector : str, optional
        Company sector.
    industry : str, optional
        Company industry.
    avgvol_1d : int, optional
        Average daily volume for the last day.
    avgvol_200d : float, optional
        Average daily volume over the last 200 days.
    """

    code: str | None = Field(default=None, description="Ticker symbol.")
    name: str | None = Field(default=None, description="Company name.")
    last_day_data_date: datetime.date | None = Field(
        default=None,
        description="Date of the latest data.",
    )
    adjusted_close: float | None = Field(
        default=None,
        description="Latest adjusted close price.",
    )
    refund_1d: float | None = Field(
        default=None,
        description="Refund value for the last day.",
    )
    refund_1d_p: float | None = Field(
        default=None,
        description="Refund percentage change for the last day.",
    )
    refund_5d: float | None = Field(
        default=None,
        description="Refund value for the last 5 days.",
    )
    refund_5d_p: float | None = Field(
        default=None,
        description="Refund percentage change for the last 5 days.",
    )
    exchange: str | None = Field(default=None, description="Exchange code.")
    currency_symbol: str | None = Field(default=None, description="Currency symbol.")
    market_capitalization: int | None = Field(
        default=None,
        description="Market capitalization in USD.",
    )
    earnings_share: float | None = Field(
        default=None,
        description="Earnings per share (EPS).",
    )
    dividend_yield: float | None = Field(
        default=None,
        description="Dividend yield percentage.",
    )
    sector: str | None = Field(default=None, description="Company sector.")
    industry: str | None = Field(default=None, description="Company industry.")
    avgvol_1d: int | None = Field(
        default=None,
        description="Average daily volume for the last day.",
    )
    avgvol_200d: float | None = Field(
        default=None,
        description="Average daily volume over the last 200 days.",
    )


class ScreenerFetcher(Fetcher[ScreenerQueryParams, list[ScreenerData]]):
    """Retrieves stock data filtered by criteria such as market capitalization, exchange, sector, and more. Results can be sorted and paginated."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> ScreenerQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        ScreenerQueryParams
            Validated query parameters.
        """
        return ScreenerQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: ScreenerQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/screener and split rows from metadata.

        Parameters
        ----------
        query : ScreenerQueryParams
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
        _path = "/screener"

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
        query: ScreenerQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[ScreenerData] | AnnotatedResult[list[ScreenerData]]:
        """Type the unpacked rows as ScreenerData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : ScreenerQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[ScreenerData] | AnnotatedResult[list[ScreenerData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [ScreenerData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker symbol."},
            "name": {"description": "Company name."},
            "last_day_data_date": {"description": "Date of the latest data.", "format": "date"},
            "adjusted_close": {"description": "Latest adjusted close price."},
            "refund_1d": {"description": "Refund value for the last day."},
            "refund_1d_p": {"description": "Refund percentage change for the last day."},
            "refund_5d": {"description": "Refund value for the last 5 days."},
            "refund_5d_p": {"description": "Refund percentage change for the last 5 days."},
            "exchange": {"description": "Exchange code."},
            "currency_symbol": {"description": "Currency symbol."},
            "market_capitalization": {"description": "Market capitalization in USD."},
            "earnings_share": {"description": "Earnings per share (EPS)."},
            "dividend_yield": {"description": "Dividend yield percentage."},
            "sector": {"description": "Company sector."},
            "industry": {"description": "Company industry."},
            "avgvol_1d": {"description": "Average daily volume for the last day."},
            "avgvol_200d": {"description": "Average daily volume over the last 200 days."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
