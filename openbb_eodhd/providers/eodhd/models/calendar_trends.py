"""Fetcher for calendar.trends — generated from spec.

Hits ``https://eodhd.com/api/calendar/trends`` via HTTP GET.
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


class CalendarTrendsQueryParams(QueryParams):
    """Query parameters for calendar.trends.

    Parameters
    ----------
    symbols : str
        Comma-separated list of stock symbols to retrieve trends data for (e.g., 'AAPL.US,MSFT.US').
    fmt : Literal['json'], optional
        Output format. Currently supports only 'json'. Choices: json. (default: 'json')
    """

    symbols: str = Field(
        description="Comma-separated list of stock symbols to retrieve trends data for (e.g., 'AAPL.US,MSFT.US').",
    )
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Currently supports only 'json'. Choices: json.",
    )


class CalendarTrendsData(Data):
    """Response row for calendar.trends.

    Parameters
    ----------
    code : str
        Stock symbol for which trend data is returned.
    date : datetime.date
        Period end date for the trend data.
    period : str
        Period for the earnings trend (e.g., '+1y', '0y', '+1q', '0q').
    growth : str, optional
        Expected EPS growth as a decimal.
    earningsEstimateAvg : str
        Average EPS estimate from analysts.
    earningsEstimateLow : str, optional
        Lowest EPS estimate from analysts.
    earningsEstimateHigh : str, optional
        Highest EPS estimate from analysts.
    earningsEstimateYearAgoEps : str, optional
        EPS estimate from the previous year.
    earningsEstimateNumberOfAnalysts : str, optional
        Number of analysts contributing to the EPS estimate.
    earningsEstimateGrowth : str, optional
        Expected EPS growth, same as 'growth'.
    revenueEstimateAvg : str, optional
        Average revenue estimate from analysts.
    revenueEstimateLow : str, optional
        Lowest revenue estimate from analysts.
    revenueEstimateHigh : str, optional
        Highest revenue estimate from analysts.
    revenueEstimateYearAgoEps : str, optional
        Revenue estimate from the previous year.
    revenueEstimateNumberOfAnalysts : str, optional
        Number of analysts contributing to the revenue estimate.
    revenueEstimateGrowth : str, optional
        Expected growth in revenue.
    epsTrendCurrent : str, optional
        Current EPS estimate.
    epsTrend7daysAgo : str, optional
        EPS estimate 7 days ago.
    epsTrend30daysAgo : str, optional
        EPS estimate 30 days ago.
    epsTrend60daysAgo : str, optional
        EPS estimate 60 days ago.
    epsTrend90daysAgo : str, optional
        EPS estimate 90 days ago.
    epsRevisionsUpLast7days : str, optional
        Number of upward EPS revisions in the last 7 days.
    epsRevisionsUpLast30days : str, optional
        Number of upward EPS revisions in the last 30 days.
    epsRevisionsDownLast7days : str, optional
        Number of downward EPS revisions in the last 7 days.
    epsRevisionsDownLast30days : str, optional
        Number of downward EPS revisions in the last 30 days.
    """

    code: str = Field(description="Stock symbol for which trend data is returned.")
    date: datetime.date = Field(description="Period end date for the trend data.")
    period: str = Field(
        description="Period for the earnings trend (e.g., '+1y', '0y', '+1q', '0q').",
    )
    growth: str | None = Field(
        default=None,
        description="Expected EPS growth as a decimal.",
    )
    earningsEstimateAvg: str = Field(description="Average EPS estimate from analysts.")
    earningsEstimateLow: str | None = Field(
        default=None,
        description="Lowest EPS estimate from analysts.",
    )
    earningsEstimateHigh: str | None = Field(
        default=None,
        description="Highest EPS estimate from analysts.",
    )
    earningsEstimateYearAgoEps: str | None = Field(
        default=None,
        description="EPS estimate from the previous year.",
    )
    earningsEstimateNumberOfAnalysts: str | None = Field(
        default=None,
        description="Number of analysts contributing to the EPS estimate.",
    )
    earningsEstimateGrowth: str | None = Field(
        default=None,
        description="Expected EPS growth, same as 'growth'.",
    )
    revenueEstimateAvg: str | None = Field(
        default=None,
        description="Average revenue estimate from analysts.",
    )
    revenueEstimateLow: str | None = Field(
        default=None,
        description="Lowest revenue estimate from analysts.",
    )
    revenueEstimateHigh: str | None = Field(
        default=None,
        description="Highest revenue estimate from analysts.",
    )
    revenueEstimateYearAgoEps: str | None = Field(
        default=None,
        description="Revenue estimate from the previous year.",
    )
    revenueEstimateNumberOfAnalysts: str | None = Field(
        default=None,
        description="Number of analysts contributing to the revenue estimate.",
    )
    revenueEstimateGrowth: str | None = Field(
        default=None,
        description="Expected growth in revenue.",
    )
    epsTrendCurrent: str | None = Field(
        default=None,
        description="Current EPS estimate.",
    )
    epsTrend7daysAgo: str | None = Field(
        default=None,
        description="EPS estimate 7 days ago.",
    )
    epsTrend30daysAgo: str | None = Field(
        default=None,
        description="EPS estimate 30 days ago.",
    )
    epsTrend60daysAgo: str | None = Field(
        default=None,
        description="EPS estimate 60 days ago.",
    )
    epsTrend90daysAgo: str | None = Field(
        default=None,
        description="EPS estimate 90 days ago.",
    )
    epsRevisionsUpLast7days: str | None = Field(
        default=None,
        description="Number of upward EPS revisions in the last 7 days.",
    )
    epsRevisionsUpLast30days: str | None = Field(
        default=None,
        description="Number of upward EPS revisions in the last 30 days.",
    )
    epsRevisionsDownLast7days: str | None = Field(
        default=None,
        description="Number of downward EPS revisions in the last 7 days.",
    )
    epsRevisionsDownLast30days: str | None = Field(
        default=None,
        description="Number of downward EPS revisions in the last 30 days.",
    )


class CalendarTrendsFetcher(Fetcher[CalendarTrendsQueryParams, list[CalendarTrendsData]]):
    """Fetches historical and upcoming earnings trends, including EPS and revenue estimates, trends, and revisions for specific stock symbols."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CalendarTrendsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CalendarTrendsQueryParams
            Validated query parameters.
        """
        return CalendarTrendsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CalendarTrendsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/calendar/trends and split rows from metadata.

        Parameters
        ----------
        query : CalendarTrendsQueryParams
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
        _path = "/calendar/trends"

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
        query: CalendarTrendsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CalendarTrendsData] | AnnotatedResult[list[CalendarTrendsData]]:
        """Type the unpacked rows as CalendarTrendsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CalendarTrendsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CalendarTrendsData] | AnnotatedResult[list[CalendarTrendsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CalendarTrendsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Stock symbol for which trend data is returned."},
            "date": {"description": "Period end date for the trend data.", "format": "date"},
            "period": {
                "description": "Period for the earnings trend (e.g., '+1y', '0y', '+1q', '0q')."
            },
            "growth": {"description": "Expected EPS growth as a decimal."},
            "earningsEstimateAvg": {"description": "Average EPS estimate from analysts."},
            "earningsEstimateLow": {"description": "Lowest EPS estimate from analysts."},
            "earningsEstimateHigh": {"description": "Highest EPS estimate from analysts."},
            "earningsEstimateYearAgoEps": {"description": "EPS estimate from the previous year."},
            "earningsEstimateNumberOfAnalysts": {
                "description": "Number of analysts contributing to the EPS estimate."
            },
            "earningsEstimateGrowth": {"description": "Expected EPS growth, same as 'growth'."},
            "revenueEstimateAvg": {"description": "Average revenue estimate from analysts."},
            "revenueEstimateLow": {"description": "Lowest revenue estimate from analysts."},
            "revenueEstimateHigh": {"description": "Highest revenue estimate from analysts."},
            "revenueEstimateYearAgoEps": {
                "description": "Revenue estimate from the previous year."
            },
            "revenueEstimateNumberOfAnalysts": {
                "description": "Number of analysts contributing to the revenue estimate."
            },
            "revenueEstimateGrowth": {"description": "Expected growth in revenue."},
            "epsTrendCurrent": {"description": "Current EPS estimate."},
            "epsTrend7daysAgo": {"description": "EPS estimate 7 days ago."},
            "epsTrend30daysAgo": {"description": "EPS estimate 30 days ago."},
            "epsTrend60daysAgo": {"description": "EPS estimate 60 days ago."},
            "epsTrend90daysAgo": {"description": "EPS estimate 90 days ago."},
            "epsRevisionsUpLast7days": {
                "description": "Number of upward EPS revisions in the last 7 days."
            },
            "epsRevisionsUpLast30days": {
                "description": "Number of upward EPS revisions in the last 30 days."
            },
            "epsRevisionsDownLast7days": {
                "description": "Number of downward EPS revisions in the last 7 days."
            },
            "epsRevisionsDownLast30days": {
                "description": "Number of downward EPS revisions in the last 30 days."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
