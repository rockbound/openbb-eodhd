"""Fetcher for ust.yield-rates — generated from spec.

Hits ``https://eodhd.com/api/ust/yield-rates`` via HTTP GET.
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


class UstYieldRatesQueryParams(QueryParams):
    """Query parameters for ust.yield-rates.

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


class UstYieldRatesData(Data):
    """Response row for ust.yield-rates.

    Parameters
    ----------
    date : datetime.date, optional
        Date of the rate.
    f_1_month : float, optional
        1-month constant maturity rate.
    f_2_months : float, optional
        2-month constant maturity rate.
    f_3_months : float, optional
        3-month constant maturity rate.
    f_4_months : float, optional
        4-month constant maturity rate.
    f_6_months : float, optional
        6-month constant maturity rate.
    f_1_year : float, optional
        1-year constant maturity rate.
    f_2_years : float, optional
        2-year constant maturity rate.
    f_3_years : float, optional
        3-year constant maturity rate.
    f_5_years : float, optional
        5-year constant maturity rate.
    f_7_years : float, optional
        7-year constant maturity rate.
    f_10_years : float, optional
        10-year constant maturity rate.
    f_20_years : float, optional
        20-year constant maturity rate.
    f_30_years : float, optional
        30-year constant maturity rate.
    """

    date: datetime.date | None = Field(default=None, description="Date of the rate.")
    f_1_month: float | None = Field(
        default=None,
        alias="1_month",
        description="1-month constant maturity rate.",
    )
    f_2_months: float | None = Field(
        default=None,
        alias="2_months",
        description="2-month constant maturity rate.",
    )
    f_3_months: float | None = Field(
        default=None,
        alias="3_months",
        description="3-month constant maturity rate.",
    )
    f_4_months: float | None = Field(
        default=None,
        alias="4_months",
        description="4-month constant maturity rate.",
    )
    f_6_months: float | None = Field(
        default=None,
        alias="6_months",
        description="6-month constant maturity rate.",
    )
    f_1_year: float | None = Field(
        default=None,
        alias="1_year",
        description="1-year constant maturity rate.",
    )
    f_2_years: float | None = Field(
        default=None,
        alias="2_years",
        description="2-year constant maturity rate.",
    )
    f_3_years: float | None = Field(
        default=None,
        alias="3_years",
        description="3-year constant maturity rate.",
    )
    f_5_years: float | None = Field(
        default=None,
        alias="5_years",
        description="5-year constant maturity rate.",
    )
    f_7_years: float | None = Field(
        default=None,
        alias="7_years",
        description="7-year constant maturity rate.",
    )
    f_10_years: float | None = Field(
        default=None,
        alias="10_years",
        description="10-year constant maturity rate.",
    )
    f_20_years: float | None = Field(
        default=None,
        alias="20_years",
        description="20-year constant maturity rate.",
    )
    f_30_years: float | None = Field(
        default=None,
        alias="30_years",
        description="30-year constant maturity rate.",
    )


class UstYieldRatesFetcher(Fetcher[UstYieldRatesQueryParams, list[UstYieldRatesData]]):
    """Returns daily US Treasury yield curve rates (constant maturity rates for 1-month through 30-year maturities)."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> UstYieldRatesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        UstYieldRatesQueryParams
            Validated query parameters.
        """
        return UstYieldRatesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UstYieldRatesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/ust/yield-rates and split rows from metadata.

        Parameters
        ----------
        query : UstYieldRatesQueryParams
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
        _path = "/ust/yield-rates"

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
        query: UstYieldRatesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[UstYieldRatesData] | AnnotatedResult[list[UstYieldRatesData]]:
        """Type the unpacked rows as UstYieldRatesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : UstYieldRatesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[UstYieldRatesData] | AnnotatedResult[list[UstYieldRatesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [UstYieldRatesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Date of the rate.", "format": "date"},
            "1_month": {"description": "1-month constant maturity rate."},
            "2_months": {"description": "2-month constant maturity rate."},
            "3_months": {"description": "3-month constant maturity rate."},
            "4_months": {"description": "4-month constant maturity rate."},
            "6_months": {"description": "6-month constant maturity rate."},
            "1_year": {"description": "1-year constant maturity rate."},
            "2_years": {"description": "2-year constant maturity rate."},
            "3_years": {"description": "3-year constant maturity rate."},
            "5_years": {"description": "5-year constant maturity rate."},
            "7_years": {"description": "7-year constant maturity rate."},
            "10_years": {"description": "10-year constant maturity rate."},
            "20_years": {"description": "20-year constant maturity rate."},
            "30_years": {"description": "30-year constant maturity rate."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
