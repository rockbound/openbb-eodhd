"""Fetcher for economic-events — generated from spec.

Hits ``https://eodhd.com/api/economic-events`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field

from ....utils import safe_json_loads, unpack_response


class EconomicEventsQueryParams(QueryParams):
    """Query parameters for economic-events.

    Parameters
    ----------
    from_ : str, optional
        Start date for data retrieval in 'YYYY-MM-DD' format.
    to : str, optional
        End date for data retrieval in 'YYYY-MM-DD' format.
    country : str, optional
        Country code in ISO 3166-1 alpha-2 format, e.g., 'US' for the United States.
    comparison : Literal['mom', 'qoq', 'yoy'], optional
        Comparison type, e.g., 'mom' for month-over-month, 'qoq' for quarter-over-quarter, 'yoy' for year-over-year. Choices: mom, qoq, yoy.
    offset : int, optional
        Data offset, from 0 to 1000. Default is 0. (default: 0)
    limit : int, optional
        Number of results to return, from 0 to 1000. Default is 50. (default: 50)
    """

    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for data retrieval in 'YYYY-MM-DD' format.",
    )
    to: str | None = Field(
        default=None,
        description="End date for data retrieval in 'YYYY-MM-DD' format.",
    )
    country: str | None = Field(
        default=None,
        description="Country code in ISO 3166-1 alpha-2 format, e.g., 'US' for the United States.",
    )
    comparison: Literal["mom", "qoq", "yoy"] | None = Field(
        default=None,
        description="Comparison type, e.g., 'mom' for month-over-month, 'qoq' for quarter-over-quarter, 'yoy' for year-over-year. Choices: mom, qoq, yoy.",
    )
    offset: int | None = Field(
        default=0,
        description="Data offset, from 0 to 1000. Default is 0.",
    )
    limit: int | None = Field(
        default=50,
        description="Number of results to return, from 0 to 1000. Default is 50.",
    )


class EconomicEventsData(Data):
    """Response row for economic-events.

    Parameters
    ----------
    type : str, optional
        Type of economic event, e.g., 'Nonfarm Payrolls'.
    comparison : str, optional
        Comparison type (e.g., 'mom', 'qoq', 'yoy').
    period : str, optional
        Period associated with the data, e.g., 'May'.
    country : str, optional
        Country code in ISO 3166 format.
    date : str, optional
        Date and time of the event in 'YYYY-MM-DD HH:MM:SS' format.
    actual : float, optional
        Actual reported value for the event.
    previous : float, optional
        Previous value for the event.
    estimate : float, optional
        Estimated value for the event.
    change : float, optional
        Change in value from previous.
    change_percentage : float, optional
        Percentage change in value from previous.
    """

    type: str | None = Field(
        default=None,
        description="Type of economic event, e.g., 'Nonfarm Payrolls'.",
    )
    comparison: str | None = Field(
        default=None,
        description="Comparison type (e.g., 'mom', 'qoq', 'yoy').",
    )
    period: str | None = Field(
        default=None,
        description="Period associated with the data, e.g., 'May'.",
    )
    country: str | None = Field(
        default=None,
        description="Country code in ISO 3166 format.",
    )
    date: str | None = Field(
        default=None,
        description="Date and time of the event in 'YYYY-MM-DD HH:MM:SS' format.",
    )
    actual: float | None = Field(
        default=None,
        description="Actual reported value for the event.",
    )
    previous: float | None = Field(
        default=None,
        description="Previous value for the event.",
    )
    estimate: float | None = Field(
        default=None,
        description="Estimated value for the event.",
    )
    change: float | None = Field(
        default=None,
        description="Change in value from previous.",
    )
    change_percentage: float | None = Field(
        default=None,
        description="Percentage change in value from previous.",
    )


class EconomicEventsFetcher(Fetcher[EconomicEventsQueryParams, list[EconomicEventsData]]):
    """Fetches economic events by date range, country, comparison type, and other optional parameters."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> EconomicEventsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        EconomicEventsQueryParams
            Validated query parameters.
        """
        return EconomicEventsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: EconomicEventsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/economic-events and split rows from metadata.

        Parameters
        ----------
        query : EconomicEventsQueryParams
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
        _path = "/economic-events"

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
        query: EconomicEventsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[EconomicEventsData] | AnnotatedResult[list[EconomicEventsData]]:
        """Type the unpacked rows as EconomicEventsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : EconomicEventsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[EconomicEventsData] | AnnotatedResult[list[EconomicEventsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [EconomicEventsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "type": {"description": "Type of economic event, e.g., 'Nonfarm Payrolls'."},
            "comparison": {"description": "Comparison type (e.g., 'mom', 'qoq', 'yoy')."},
            "period": {"description": "Period associated with the data, e.g., 'May'."},
            "country": {"description": "Country code in ISO 3166 format."},
            "date": {"description": "Date and time of the event in 'YYYY-MM-DD HH:MM:SS' format."},
            "actual": {"description": "Actual reported value for the event."},
            "previous": {"description": "Previous value for the event."},
            "estimate": {"description": "Estimated value for the event."},
            "change": {"description": "Change in value from previous."},
            "change_percentage": {"description": "Percentage change in value from previous."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
