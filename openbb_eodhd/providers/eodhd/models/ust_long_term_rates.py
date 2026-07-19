"""Fetcher for ust.long-term-rates — generated from spec.

Hits ``https://eodhd.com/api/ust/long-term-rates`` via HTTP GET.
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


class UstLongTermRatesQueryParams(QueryParams):
    """Query parameters for ust.long-term-rates.

    Parameters
    ----------
    from_ : str, optional
        Start date in 'YYYY-MM-DD' format.
    to : str, optional
        End date in 'YYYY-MM-DD' format.
    filter_year_ : int, optional
        Filter by year (e.g., 2024).
    page_limit_ : int, optional
        Number of records per page.
    page_offset_ : int, optional
        Pagination offset.
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date in 'YYYY-MM-DD' format.",
    )
    to: str | None = Field(default=None, description="End date in 'YYYY-MM-DD' format.")
    filter_year_: int | None = Field(
        default=None,
        alias="filter[year]",
        description="Filter by year (e.g., 2024).",
    )
    page_limit_: int | None = Field(
        default=None,
        alias="page[limit]",
        description="Number of records per page.",
    )
    page_offset_: int | None = Field(
        default=None,
        alias="page[offset]",
        description="Pagination offset.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class UstLongTermRatesData(Data):
    """Response row for ust.long-term-rates.

    Parameters
    ----------
    date : datetime.date, optional
        Date of the rate.
    lt_composite_gt_10 : float, optional
        Long-term composite rate (over 10 years).
    treasury_20_year_cmt : float, optional
        Treasury 20-year constant maturity rate.
    extrapolation_factor : float, optional
        Extrapolation factor.
    """

    date: datetime.date | None = Field(default=None, description="Date of the rate.")
    lt_composite_gt_10: float | None = Field(
        default=None,
        description="Long-term composite rate (over 10 years).",
    )
    treasury_20_year_cmt: float | None = Field(
        default=None,
        description="Treasury 20-year constant maturity rate.",
    )
    extrapolation_factor: float | None = Field(
        default=None,
        description="Extrapolation factor.",
    )


class UstLongTermRatesFetcher(Fetcher[UstLongTermRatesQueryParams, list[UstLongTermRatesData]]):
    """Returns US Treasury long-term average rates and extrapolation factors for maturities beyond 30 years."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> UstLongTermRatesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        UstLongTermRatesQueryParams
            Validated query parameters.
        """
        return UstLongTermRatesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UstLongTermRatesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/ust/long-term-rates and split rows from metadata.

        Parameters
        ----------
        query : UstLongTermRatesQueryParams
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
        _path = "/ust/long-term-rates"

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
        query: UstLongTermRatesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[UstLongTermRatesData] | AnnotatedResult[list[UstLongTermRatesData]]:
        """Type the unpacked rows as UstLongTermRatesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : UstLongTermRatesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[UstLongTermRatesData] | AnnotatedResult[list[UstLongTermRatesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [UstLongTermRatesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Date of the rate.", "format": "date"},
            "lt_composite_gt_10": {"description": "Long-term composite rate (over 10 years)."},
            "treasury_20_year_cmt": {"description": "Treasury 20-year constant maturity rate."},
            "extrapolation_factor": {"description": "Extrapolation factor."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
