"""Fetcher for calendar.earnings — generated from spec.

Hits ``https://eodhd.com/api/calendar/earnings`` via HTTP GET.
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


class CalendarEarningsQueryParams(QueryParams):
    """Query parameters for calendar.earnings.

    Parameters
    ----------
    from_ : str, optional
        Start date for earnings data, in 'YYYY-MM-DD' format. Defaults to today if not provided.
    to : str, optional
        End date for earnings data, in 'YYYY-MM-DD' format. Defaults to 7 days from today if not provided.
    symbols : str, optional
        Specific symbols to retrieve earnings data for, separated by commas (e.g., 'AAPL.US,MSFT.US'). Overrides the 'from' and 'to' parameters if used.
    fmt : Literal['csv', 'json'], optional
        Output format, either 'csv' or 'json'. Defaults to 'csv'. Choices: csv, json. (default: 'json')
    """

    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for earnings data, in 'YYYY-MM-DD' format. Defaults to today if not provided.",
    )
    to: str | None = Field(
        default=None,
        description="End date for earnings data, in 'YYYY-MM-DD' format. Defaults to 7 days from today if not provided.",
    )
    symbols: str | None = Field(
        default=None,
        description="Specific symbols to retrieve earnings data for, separated by commas (e.g., 'AAPL.US,MSFT.US'). Overrides the 'from' and 'to' parameters if used.",
    )
    fmt: Literal["csv", "json"] | None = Field(
        default="json",
        description="Output format, either 'csv' or 'json'. Defaults to 'csv'. Choices: csv, json.",
    )


class CalendarEarningsData(Data):
    """Response row for calendar.earnings.

    Parameters
    ----------
    code : str
        Ticker symbol of the company.
    report_date : datetime.date
        Date the earnings report was released.
    date : datetime.date
        End date of the fiscal period.
    before_after_market : str, optional
        Indicates whether the earnings report was released 'BeforeMarket' or 'AfterMarket'.
    currency : str
        Currency of the earnings values.
    actual : float, optional
        Actual reported earnings per share or other metric.
    estimate : float, optional
        Estimated earnings per share or other metric.
    difference : float, optional
        Difference between actual and estimated values.
    percent : float, optional
        Percentage difference between actual and estimated values.
    """

    code: str = Field(description="Ticker symbol of the company.")
    report_date: datetime.date = Field(
        description="Date the earnings report was released.",
    )
    date: datetime.date = Field(description="End date of the fiscal period.")
    before_after_market: str | None = Field(
        default=None,
        description="Indicates whether the earnings report was released 'BeforeMarket' or 'AfterMarket'.",
    )
    currency: str = Field(description="Currency of the earnings values.")
    actual: float | None = Field(
        default=None,
        description="Actual reported earnings per share or other metric.",
    )
    estimate: float | None = Field(
        default=None,
        description="Estimated earnings per share or other metric.",
    )
    difference: float | None = Field(
        default=None,
        description="Difference between actual and estimated values.",
    )
    percent: float | None = Field(
        default=None,
        description="Percentage difference between actual and estimated values.",
    )


class CalendarEarningsFetcher(Fetcher[CalendarEarningsQueryParams, list[CalendarEarningsData]]):
    """Fetches upcoming earnings data, with optional parameters for date ranges and specific symbols."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CalendarEarningsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CalendarEarningsQueryParams
            Validated query parameters.
        """
        return CalendarEarningsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CalendarEarningsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/calendar/earnings and split rows from metadata.

        Parameters
        ----------
        query : CalendarEarningsQueryParams
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
        _path = "/calendar/earnings"

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
        query: CalendarEarningsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CalendarEarningsData] | AnnotatedResult[list[CalendarEarningsData]]:
        """Type the unpacked rows as CalendarEarningsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CalendarEarningsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CalendarEarningsData] | AnnotatedResult[list[CalendarEarningsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CalendarEarningsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker symbol of the company."},
            "report_date": {
                "description": "Date the earnings report was released.",
                "format": "date",
            },
            "date": {"description": "End date of the fiscal period.", "format": "date"},
            "before_after_market": {
                "description": "Indicates whether the earnings report was released 'BeforeMarket' or 'AfterMarket'."
            },
            "currency": {"description": "Currency of the earnings values."},
            "actual": {"description": "Actual reported earnings per share or other metric."},
            "estimate": {"description": "Estimated earnings per share or other metric."},
            "difference": {"description": "Difference between actual and estimated values."},
            "percent": {
                "description": "Percentage difference between actual and estimated values."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
