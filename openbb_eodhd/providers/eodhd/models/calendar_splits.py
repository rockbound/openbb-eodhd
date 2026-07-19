"""Fetcher for calendar.splits — generated from spec.

Hits ``https://eodhd.com/api/calendar/splits`` via HTTP GET.
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


class CalendarSplitsQueryParams(QueryParams):
    """Query parameters for calendar.splits.

    Parameters
    ----------
    from_ : str, optional
        Start date for split data in 'YYYY-MM-DD' format. Defaults to today if not provided.
    to : str, optional
        End date for split data in 'YYYY-MM-DD' format. Defaults to 7 days from today if not provided.
    fmt : Literal['csv', 'json'], optional
        Output format, either 'csv' or 'json'. Default is 'csv'. Choices: csv, json. (default: 'json')
    """

    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for split data in 'YYYY-MM-DD' format. Defaults to today if not provided.",
    )
    to: str | None = Field(
        default=None,
        description="End date for split data in 'YYYY-MM-DD' format. Defaults to 7 days from today if not provided.",
    )
    fmt: Literal["csv", "json"] | None = Field(
        default="json",
        description="Output format, either 'csv' or 'json'. Default is 'csv'. Choices: csv, json.",
    )


class CalendarSplitsData(Data):
    """Response row for calendar.splits.

    Parameters
    ----------
    code : str
        Ticker symbol of the stock undergoing the split.
    split_date : datetime.date
        The date when the stock split takes effect.
    optionable : Literal['Y', 'N'], optional
        Indicates if the stock is optionable ('Y' for yes, 'N' for no). Choices: Y, N.
    old_shares : int
        The number of shares before the split.
    new_shares : int
        The number of shares after the split.
    """

    code: str = Field(description="Ticker symbol of the stock undergoing the split.")
    split_date: datetime.date = Field(
        description="The date when the stock split takes effect.",
    )
    optionable: Literal["Y", "N"] | None = Field(
        default=None,
        description="Indicates if the stock is optionable ('Y' for yes, 'N' for no). Choices: Y, N.",
    )
    old_shares: int = Field(description="The number of shares before the split.")
    new_shares: int = Field(description="The number of shares after the split.")


class CalendarSplitsFetcher(Fetcher[CalendarSplitsQueryParams, list[CalendarSplitsData]]):
    """Fetches information on stock splits for specified date ranges."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CalendarSplitsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CalendarSplitsQueryParams
            Validated query parameters.
        """
        return CalendarSplitsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CalendarSplitsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/calendar/splits and split rows from metadata.

        Parameters
        ----------
        query : CalendarSplitsQueryParams
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
        _path = "/calendar/splits"

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
        query: CalendarSplitsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CalendarSplitsData] | AnnotatedResult[list[CalendarSplitsData]]:
        """Type the unpacked rows as CalendarSplitsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CalendarSplitsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CalendarSplitsData] | AnnotatedResult[list[CalendarSplitsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CalendarSplitsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker symbol of the stock undergoing the split."},
            "split_date": {
                "description": "The date when the stock split takes effect.",
                "format": "date",
            },
            "optionable": {
                "description": "Indicates if the stock is optionable ('Y' for yes, 'N' for no)."
            },
            "old_shares": {"description": "The number of shares before the split."},
            "new_shares": {"description": "The number of shares after the split."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
