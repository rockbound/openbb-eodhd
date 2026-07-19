"""Fetcher for calendar.ipos — generated from spec.

Hits ``https://eodhd.com/api/calendar/ipos`` via HTTP GET.
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


class CalendarIposQueryParams(QueryParams):
    """Query parameters for calendar.ipos.

    Parameters
    ----------
    from_ : str, optional
        Start date for IPO data in 'YYYY-MM-DD' format. Defaults to today if not provided.
    to : str, optional
        End date for IPO data in 'YYYY-MM-DD' format. Defaults to 7 days from today if not provided.
    fmt : Literal['csv', 'json'], optional
        Output format. Possible values: 'csv' for CSV and 'json' for JSON. Defaults to 'csv'. Choices: csv, json. (default: 'json')
    """

    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for IPO data in 'YYYY-MM-DD' format. Defaults to today if not provided.",
    )
    to: str | None = Field(
        default=None,
        description="End date for IPO data in 'YYYY-MM-DD' format. Defaults to 7 days from today if not provided.",
    )
    fmt: Literal["csv", "json"] | None = Field(
        default="json",
        description="Output format. Possible values: 'csv' for CSV and 'json' for JSON. Defaults to 'csv'. Choices: csv, json.",
    )


class CalendarIposData(Data):
    """Response row for calendar.ipos.

    Parameters
    ----------
    code : str, optional
        Ticker symbol of the IPO if available.
    name : str
        Name of the company going public.
    exchange : str
        Exchange where the IPO will be listed.
    currency : str
        Currency used for the IPO pricing.
    start_date : datetime.date, optional
        Expected start date for trading.
    filing_date : datetime.date, optional
        Date when the IPO was filed.
    amended_date : datetime.date, optional
        Date when the IPO filing was amended.
    price_from : float, optional
        Lower end of the price range.
    price_to : float, optional
        Upper end of the price range.
    offer_price : float, optional
        Final offer price.
    shares : int, optional
        Number of shares being offered.
    deal_type : str
        Status of the IPO, e.g., 'Filed', 'Priced', 'Expected', or 'Amended'.
    """

    code: str | None = Field(
        default=None,
        description="Ticker symbol of the IPO if available.",
    )
    name: str = Field(description="Name of the company going public.")
    exchange: str = Field(description="Exchange where the IPO will be listed.")
    currency: str = Field(description="Currency used for the IPO pricing.")
    start_date: datetime.date | None = Field(
        default=None,
        description="Expected start date for trading.",
    )
    filing_date: datetime.date | None = Field(
        default=None,
        description="Date when the IPO was filed.",
    )
    amended_date: datetime.date | None = Field(
        default=None,
        description="Date when the IPO filing was amended.",
    )
    price_from: float | None = Field(
        default=None,
        description="Lower end of the price range.",
    )
    price_to: float | None = Field(
        default=None,
        description="Upper end of the price range.",
    )
    offer_price: float | None = Field(default=None, description="Final offer price.")
    shares: int | None = Field(
        default=None,
        description="Number of shares being offered.",
    )
    deal_type: str = Field(
        description="Status of the IPO, e.g., 'Filed', 'Priced', 'Expected', or 'Amended'.",
    )


class CalendarIposFetcher(Fetcher[CalendarIposQueryParams, list[CalendarIposData]]):
    """Fetches historical and upcoming IPOs for specified date ranges."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CalendarIposQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CalendarIposQueryParams
            Validated query parameters.
        """
        return CalendarIposQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CalendarIposQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/calendar/ipos and split rows from metadata.

        Parameters
        ----------
        query : CalendarIposQueryParams
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
        _path = "/calendar/ipos"

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
        query: CalendarIposQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CalendarIposData] | AnnotatedResult[list[CalendarIposData]]:
        """Type the unpacked rows as CalendarIposData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CalendarIposQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CalendarIposData] | AnnotatedResult[list[CalendarIposData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CalendarIposData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker symbol of the IPO if available."},
            "name": {"description": "Name of the company going public."},
            "exchange": {"description": "Exchange where the IPO will be listed."},
            "currency": {"description": "Currency used for the IPO pricing."},
            "start_date": {"description": "Expected start date for trading.", "format": "date"},
            "filing_date": {"description": "Date when the IPO was filed.", "format": "date"},
            "amended_date": {
                "description": "Date when the IPO filing was amended.",
                "format": "date",
            },
            "price_from": {"description": "Lower end of the price range.", "format": "float"},
            "price_to": {"description": "Upper end of the price range.", "format": "float"},
            "offer_price": {"description": "Final offer price.", "format": "float"},
            "shares": {"description": "Number of shares being offered."},
            "deal_type": {
                "description": "Status of the IPO, e.g., 'Filed', 'Priced', 'Expected', or 'Amended'."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
