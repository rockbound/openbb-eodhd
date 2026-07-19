"""Fetcher for calendar.dividends — generated from spec.

Hits ``https://eodhd.com/api/calendar/dividends`` via HTTP GET.
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


class CalendarDividendsQueryParams(QueryParams):
    """Query parameters for calendar.dividends.

    Parameters
    ----------
    filter_date_eq_ : str, optional
        Exact date in 'YYYY-MM-DD' format. Required if `filter[symbol]` is not present.
    filter_date_from_ : str, optional
        Start date in 'YYYY-MM-DD' format.
    filter_date_to_ : str, optional
        End date in 'YYYY-MM-DD' format.
    filter_symbol_ : str, optional
        Ticker symbol (e.g., 'AAPL.US'). When provided, `filter[date_eq]` may be omitted.
    page_limit_ : int, optional
        Number of records per page (1-10000).
    page_offset_ : int, optional
        Pagination offset (0-1000000).
    fmt : Literal['csv', 'json'], optional
        Output format. Defaults to 'json'. Choices: csv, json. (default: 'json')
    """

    filter_date_eq_: str | None = Field(
        default=None,
        alias="filter[date_eq]",
        description="Exact date in 'YYYY-MM-DD' format. Required if `filter[symbol]` is not present.",
    )
    filter_date_from_: str | None = Field(
        default=None,
        alias="filter[date_from]",
        description="Start date in 'YYYY-MM-DD' format.",
    )
    filter_date_to_: str | None = Field(
        default=None,
        alias="filter[date_to]",
        description="End date in 'YYYY-MM-DD' format.",
    )
    filter_symbol_: str | None = Field(
        default=None,
        alias="filter[symbol]",
        description="Ticker symbol (e.g., 'AAPL.US'). When provided, `filter[date_eq]` may be omitted.",
    )
    page_limit_: int | None = Field(
        default=None,
        alias="page[limit]",
        description="Number of records per page (1-10000).",
    )
    page_offset_: int | None = Field(
        default=None,
        alias="page[offset]",
        description="Pagination offset (0-1000000).",
    )
    fmt: Literal["csv", "json"] | None = Field(
        default="json",
        description="Output format. Defaults to 'json'. Choices: csv, json.",
    )


class CalendarDividendsData(Data):
    """Response row for calendar.dividends.

    Parameters
    ----------
    date : datetime.date
        Dividend ex-date.
    symbol : str
        Ticker symbol.
    """

    date: datetime.date = Field(description="Dividend ex-date.")
    symbol: str = Field(description="Ticker symbol.")


class CalendarDividendsFetcher(Fetcher[CalendarDividendsQueryParams, list[CalendarDividendsData]]):
    """Look up upcoming and historical dividend events."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CalendarDividendsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CalendarDividendsQueryParams
            Validated query parameters.
        """
        return CalendarDividendsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CalendarDividendsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/calendar/dividends and split rows from metadata.

        Parameters
        ----------
        query : CalendarDividendsQueryParams
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
        _path = "/calendar/dividends"

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
        query: CalendarDividendsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CalendarDividendsData] | AnnotatedResult[list[CalendarDividendsData]]:
        """Type the unpacked rows as CalendarDividendsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CalendarDividendsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CalendarDividendsData] | AnnotatedResult[list[CalendarDividendsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CalendarDividendsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Dividend ex-date.", "format": "date"},
            "symbol": {"description": "Ticker symbol."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
