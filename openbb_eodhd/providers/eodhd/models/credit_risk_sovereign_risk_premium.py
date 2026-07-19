"""Fetcher for credit-risk.sovereign.risk-premium — generated from spec.

Hits ``https://eodhd.com/api/credit-risk/sovereign/risk-premium`` via HTTP GET.
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


class CreditRiskSovereignRiskPremiumQueryParams(QueryParams):
    """Query parameters for credit-risk.sovereign.risk-premium.

    Parameters
    ----------
    filter_country_ : str, optional
        Filter by country name or ISO Alpha-3 code (e.g., 'USA' or 'Germany').
    filter_region_ : str, optional
        Filter by region name.
    filter_as_of_ : str, optional
        Filter by the as-of date (YYYY-MM-DD).
    page_offset_ : int, optional
        Pagination offset (records to skip). (default: 0)
    page_limit_ : int, optional
        Number of records per page. Default 20, maximum 100. (default: 20)
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    filter_country_: str | None = Field(
        default=None,
        alias="filter[country]",
        description="Filter by country name or ISO Alpha-3 code (e.g., 'USA' or 'Germany').",
    )
    filter_region_: str | None = Field(
        default=None,
        alias="filter[region]",
        description="Filter by region name.",
    )
    filter_as_of_: str | None = Field(
        default=None,
        alias="filter[as_of]",
        description="Filter by the as-of date (YYYY-MM-DD).",
    )
    page_offset_: int | None = Field(
        default=0,
        alias="page[offset]",
        description="Pagination offset (records to skip).",
    )
    page_limit_: int | None = Field(
        default=20,
        alias="page[limit]",
        description="Number of records per page. Default 20, maximum 100.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class CreditRiskSovereignRiskPremiumData(Data):
    """Response row for credit-risk.sovereign.risk-premium.

    Parameters
    ----------
    country_iso3 : str, optional
        ISO Alpha-3 country code.
    country_name : str, optional
        Country name.
    as_of_date : datetime.datetime, optional
        As-of timestamp for the values.
    moodys_rating : str, optional
        Moody's sovereign credit rating.
    adj_default_spread : float, optional
        Adjusted default spread.
    country_risk_premium : float, optional
        Country risk premium.
    equity_risk_premium : float, optional
        Total equity risk premium.
    corporate_tax_rate : float, optional
        Corporate tax rate.
    sovereign_cds : float, optional
        Sovereign CDS spread, if available.
    source : str, optional
        Data source.
    """

    country_iso3: str | None = Field(
        default=None,
        description="ISO Alpha-3 country code.",
    )
    country_name: str | None = Field(default=None, description="Country name.")
    as_of_date: datetime.datetime | None = Field(
        default=None,
        description="As-of timestamp for the values.",
    )
    moodys_rating: str | None = Field(
        default=None,
        description="Moody's sovereign credit rating.",
    )
    adj_default_spread: float | None = Field(
        default=None,
        description="Adjusted default spread.",
    )
    country_risk_premium: float | None = Field(
        default=None,
        description="Country risk premium.",
    )
    equity_risk_premium: float | None = Field(
        default=None,
        description="Total equity risk premium.",
    )
    corporate_tax_rate: float | None = Field(
        default=None,
        description="Corporate tax rate.",
    )
    sovereign_cds: float | None = Field(
        default=None,
        description="Sovereign CDS spread, if available.",
    )
    source: str | None = Field(default=None, description="Data source.")


class CreditRiskSovereignRiskPremiumFetcher(
    Fetcher[CreditRiskSovereignRiskPremiumQueryParams, list[CreditRiskSovereignRiskPremiumData]]
):
    """Returns country-level default spreads, country risk premiums, equity risk premiums, corporate tax rates, and related sovereign credit metrics."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CreditRiskSovereignRiskPremiumQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CreditRiskSovereignRiskPremiumQueryParams
            Validated query parameters.
        """
        return CreditRiskSovereignRiskPremiumQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CreditRiskSovereignRiskPremiumQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/credit-risk/sovereign/risk-premium and split rows from metadata.

        Parameters
        ----------
        query : CreditRiskSovereignRiskPremiumQueryParams
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
        _path = "/credit-risk/sovereign/risk-premium"

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
        query: CreditRiskSovereignRiskPremiumQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> (
        list[CreditRiskSovereignRiskPremiumData]
        | AnnotatedResult[list[CreditRiskSovereignRiskPremiumData]]
    ):
        """Type the unpacked rows as CreditRiskSovereignRiskPremiumData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CreditRiskSovereignRiskPremiumQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CreditRiskSovereignRiskPremiumData] | AnnotatedResult[list[CreditRiskSovereignRiskPremiumData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CreditRiskSovereignRiskPremiumData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "country_iso3": {"description": "ISO Alpha-3 country code."},
            "country_name": {"description": "Country name."},
            "as_of_date": {"description": "As-of timestamp for the values.", "format": "date-time"},
            "moodys_rating": {"description": "Moody's sovereign credit rating."},
            "adj_default_spread": {"description": "Adjusted default spread."},
            "country_risk_premium": {"description": "Country risk premium."},
            "equity_risk_premium": {"description": "Total equity risk premium."},
            "corporate_tax_rate": {"description": "Corporate tax rate."},
            "sovereign_cds": {"description": "Sovereign CDS spread, if available."},
            "source": {"description": "Data source."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
