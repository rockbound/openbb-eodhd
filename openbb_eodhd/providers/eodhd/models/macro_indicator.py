"""Fetcher for macro-indicator — generated from spec.

Hits ``https://eodhd.com/api/macro-indicator/{country}`` via HTTP GET.
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


class MacroIndicatorQueryParams(QueryParams):
    """Query parameters for macro-indicator.

    Parameters
    ----------
    country : str
        Country code in ISO Alpha-3 format (e.g., 'USA' for United States, 'FRA' for France).
    indicator : Literal['real_interest_rate', 'population_total', 'population_growth_annual', 'inflation_consumer_prices_annual', 'consumer_price_index', 'gdp_current_usd', 'gdp_per_capita_usd', 'gdp_growth_annual', 'debt_percent_gdp', 'net_trades_goods_services', 'inflation_gdp_deflator_annual', 'agriculture_value_added_percent_gdp', 'industry_value_added_percent_gdp', 'services_value_added_percent_gdp', 'exports_of_goods_services_percent_gdp', 'imports_of_goods_services_percent_gdp', 'gross_capital_formation_percent_gdp', 'net_migration', 'gni_usd', 'gni_per_capita_usd', 'gni_ppp_usd', 'gni_per_capita_ppp_usd', 'income_share_lowest_twenty', 'life_expectancy', 'fertility_rate', 'prevalence_hiv_total', 'co2_emissions_tons_per_capita', 'surface_area_km', 'poverty_poverty_lines_percent_population', 'revenue_excluding_grants_percent_gdp', 'cash_surplus_deficit_percent_gdp', 'startup_procedures_register', 'market_cap_domestic_companies_percent_gdp', 'mobile_subscriptions_per_hundred', 'internet_users_per_hundred', 'high_technology_exports_percent_total', 'merchandise_trade_percent_gdp', 'total_debt_service_percent_gni', 'unemployment_total_percent'], optional
        The macroeconomic indicator to retrieve. Default is 'gdp_current_usd'. Choices: real_interest_rate, population_total, population_growth_annual, inflation_consumer_prices_annual, consumer_price_index, gdp_current_usd, gdp_per_capita_usd, gdp_growth_annual, debt_percent_gdp, net_trades_goods_services, inflation_gdp_deflator_annual, agriculture_value_added_percent_gdp, industry_value_added_percent_gdp, services_value_added_percent_gdp, exports_of_goods_services_percent_gdp, imports_of_goods_services_percent_gdp, gross_capital_formation_percent_gdp, net_migration, gni_usd, gni_per_capita_usd, gni_ppp_usd, gni_per_capita_ppp_usd, income_share_lowest_twenty, life_expectancy, fertility_rate, prevalence_hiv_total, co2_emissions_tons_per_capita, surface_area_km, poverty_poverty_lines_percent_population, revenue_excluding_grants_percent_gdp, cash_surplus_deficit_percent_gdp, startup_procedures_register, market_cap_domestic_companies_percent_gdp, mobile_subscriptions_per_hundred, internet_users_per_hundred, high_technology_exports_percent_total, merchandise_trade_percent_gdp, total_debt_service_percent_gni, unemployment_total_percent. (default: 'gdp_current_usd')
    fmt : Literal['json', 'csv'], optional
        Output format: 'json' or 'csv'. Default is 'json'. Choices: json, csv. (default: 'json')
    """

    country: str = Field(
        description="Country code in ISO Alpha-3 format (e.g., 'USA' for United States, 'FRA' for France).",
    )
    indicator: (
        Literal[
            "real_interest_rate",
            "population_total",
            "population_growth_annual",
            "inflation_consumer_prices_annual",
            "consumer_price_index",
            "gdp_current_usd",
            "gdp_per_capita_usd",
            "gdp_growth_annual",
            "debt_percent_gdp",
            "net_trades_goods_services",
            "inflation_gdp_deflator_annual",
            "agriculture_value_added_percent_gdp",
            "industry_value_added_percent_gdp",
            "services_value_added_percent_gdp",
            "exports_of_goods_services_percent_gdp",
            "imports_of_goods_services_percent_gdp",
            "gross_capital_formation_percent_gdp",
            "net_migration",
            "gni_usd",
            "gni_per_capita_usd",
            "gni_ppp_usd",
            "gni_per_capita_ppp_usd",
            "income_share_lowest_twenty",
            "life_expectancy",
            "fertility_rate",
            "prevalence_hiv_total",
            "co2_emissions_tons_per_capita",
            "surface_area_km",
            "poverty_poverty_lines_percent_population",
            "revenue_excluding_grants_percent_gdp",
            "cash_surplus_deficit_percent_gdp",
            "startup_procedures_register",
            "market_cap_domestic_companies_percent_gdp",
            "mobile_subscriptions_per_hundred",
            "internet_users_per_hundred",
            "high_technology_exports_percent_total",
            "merchandise_trade_percent_gdp",
            "total_debt_service_percent_gni",
            "unemployment_total_percent",
        ]
        | None
    ) = Field(
        default="gdp_current_usd",
        description="The macroeconomic indicator to retrieve. Default is 'gdp_current_usd'. Choices: real_interest_rate, population_total, population_growth_annual, inflation_consumer_prices_annual, consumer_price_index, gdp_current_usd, gdp_per_capita_usd, gdp_growth_annual, debt_percent_gdp, net_trades_goods_services, inflation_gdp_deflator_annual, agriculture_value_added_percent_gdp, industry_value_added_percent_gdp, services_value_added_percent_gdp, exports_of_goods_services_percent_gdp, imports_of_goods_services_percent_gdp, gross_capital_formation_percent_gdp, net_migration, gni_usd, gni_per_capita_usd, gni_ppp_usd, gni_per_capita_ppp_usd, income_share_lowest_twenty, life_expectancy, fertility_rate, prevalence_hiv_total, co2_emissions_tons_per_capita, surface_area_km, poverty_poverty_lines_percent_population, revenue_excluding_grants_percent_gdp, cash_surplus_deficit_percent_gdp, startup_procedures_register, market_cap_domestic_companies_percent_gdp, mobile_subscriptions_per_hundred, internet_users_per_hundred, high_technology_exports_percent_total, merchandise_trade_percent_gdp, total_debt_service_percent_gni, unemployment_total_percent.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format: 'json' or 'csv'. Default is 'json'. Choices: json, csv.",
    )


class MacroIndicatorData(Data):
    """Response row for macro-indicator.

    Parameters
    ----------
    CountryCode : str, optional
        ISO Alpha-3 country code, e.g., 'USA' for United States.
    CountryName : str, optional
        Country name, e.g., 'United States'.
    Indicator : str, optional
        Indicator name, e.g., 'Inflation, consumer prices (annual %)'.
    Date : datetime.date, optional
        Date of the recorded value.
    Period : str, optional
        Period of the data, e.g., 'Annual'.
    Value : float, optional
        Recorded value of the indicator.
    """

    CountryCode: str | None = Field(
        default=None,
        description="ISO Alpha-3 country code, e.g., 'USA' for United States.",
    )
    CountryName: str | None = Field(
        default=None,
        description="Country name, e.g., 'United States'.",
    )
    Indicator: str | None = Field(
        default=None,
        description="Indicator name, e.g., 'Inflation, consumer prices (annual %)'.",
    )
    Date: datetime.date | None = Field(
        default=None,
        description="Date of the recorded value.",
    )
    Period: str | None = Field(
        default=None,
        description="Period of the data, e.g., 'Annual'.",
    )
    Value: float | None = Field(
        default=None,
        description="Recorded value of the indicator.",
    )


class MacroIndicatorFetcher(Fetcher[MacroIndicatorQueryParams, list[MacroIndicatorData]]):
    """Fetches macroeconomic data for a selected indicator, such as GDP or inflation, by country code."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MacroIndicatorQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MacroIndicatorQueryParams
            Validated query parameters.
        """
        return MacroIndicatorQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MacroIndicatorQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/macro-indicator/{country} and split rows from metadata.

        Parameters
        ----------
        query : MacroIndicatorQueryParams
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
        _path = f"/macro-indicator/{query.country}"

        _query_dict = query.model_dump(by_alias=True, exclude={"country"}, exclude_none=True)
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
        query: MacroIndicatorQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MacroIndicatorData] | AnnotatedResult[list[MacroIndicatorData]]:
        """Type the unpacked rows as MacroIndicatorData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MacroIndicatorQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MacroIndicatorData] | AnnotatedResult[list[MacroIndicatorData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MacroIndicatorData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "CountryCode": {
                "description": "ISO Alpha-3 country code, e.g., 'USA' for United States."
            },
            "CountryName": {"description": "Country name, e.g., 'United States'."},
            "Indicator": {
                "description": "Indicator name, e.g., 'Inflation, consumer prices (annual %)'."
            },
            "Date": {"description": "Date of the recorded value.", "format": "date"},
            "Period": {"description": "Period of the data, e.g., 'Annual'."},
            "Value": {"description": "Recorded value of the indicator."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
