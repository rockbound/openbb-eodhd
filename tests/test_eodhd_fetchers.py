"""Auto-generated unit tests for the eodhd provider."""

import pytest
from openbb_core.app.service.user_service import UserService

from openbb_eodhd.providers.eodhd.models.calendar_dividends import CalendarDividendsFetcher
from openbb_eodhd.providers.eodhd.models.calendar_earnings import CalendarEarningsFetcher
from openbb_eodhd.providers.eodhd.models.calendar_ipos import CalendarIposFetcher
from openbb_eodhd.providers.eodhd.models.calendar_splits import CalendarSplitsFetcher
from openbb_eodhd.providers.eodhd.models.cboe_indices import CboeIndicesFetcher
from openbb_eodhd.providers.eodhd.models.credit_risk_cds_market_aggregates import (
    CreditRiskCdsMarketAggregatesFetcher,
)
from openbb_eodhd.providers.eodhd.models.credit_risk_corporate_cmdi import (
    CreditRiskCorporateCmdiFetcher,
)
from openbb_eodhd.providers.eodhd.models.credit_risk_corporate_hqm_yields import (
    CreditRiskCorporateHqmYieldsFetcher,
)
from openbb_eodhd.providers.eodhd.models.credit_risk_sovereign_cds_spreads import (
    CreditRiskSovereignCdsSpreadsFetcher,
)
from openbb_eodhd.providers.eodhd.models.credit_risk_sovereign_credit_ratings import (
    CreditRiskSovereignCreditRatingsFetcher,
)
from openbb_eodhd.providers.eodhd.models.credit_risk_sovereign_default_spreads import (
    CreditRiskSovereignDefaultSpreadsFetcher,
)
from openbb_eodhd.providers.eodhd.models.credit_risk_sovereign_risk_premium import (
    CreditRiskSovereignRiskPremiumFetcher,
)
from openbb_eodhd.providers.eodhd.models.economic_events import EconomicEventsFetcher
from openbb_eodhd.providers.eodhd.models.exchanges_list import ExchangesListFetcher
from openbb_eodhd.providers.eodhd.models.id_mapping import IdMappingFetcher
from openbb_eodhd.providers.eodhd.models.insider_transactions import InsiderTransactionsFetcher
from openbb_eodhd.providers.eodhd.models.internal_user import InternalUserFetcher
from openbb_eodhd.providers.eodhd.models.logo import LogoFetcher
from openbb_eodhd.providers.eodhd.models.logo_svg import LogoSvgFetcher
from openbb_eodhd.providers.eodhd.models.mp_investverte_companies import (
    MpInvestverteCompaniesFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_investverte_countries import (
    MpInvestverteCountriesFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_investverte_sectors import MpInvestverteSectorsFetcher
from openbb_eodhd.providers.eodhd.models.mp_praams_explore_bond import MpPraamsExploreBondFetcher
from openbb_eodhd.providers.eodhd.models.mp_praams_explore_equity import (
    MpPraamsExploreEquityFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_options_contracts import (
    MpUnicornbayOptionsContractsFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_options_eod import (
    MpUnicornbayOptionsEodFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_options_underlying_symbols import (
    MpUnicornbayOptionsUnderlyingSymbolsFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_spglobal_list import (
    MpUnicornbaySpglobalListFetcher,
)
from openbb_eodhd.providers.eodhd.models.news import NewsFetcher
from openbb_eodhd.providers.eodhd.models.rates_policy_rates import RatesPolicyRatesFetcher
from openbb_eodhd.providers.eodhd.models.rates_reference_rates import RatesReferenceRatesFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_entities import SanctionsEntitiesFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_programs import SanctionsProgramsFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_sources import SanctionsSourcesFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_vessels import SanctionsVesselsFetcher
from openbb_eodhd.providers.eodhd.models.screener import ScreenerFetcher
from openbb_eodhd.providers.eodhd.models.spreads_funding_stress import SpreadsFundingStressFetcher
from openbb_eodhd.providers.eodhd.models.user import UserFetcher
from openbb_eodhd.providers.eodhd.models.ust_bill_rates import UstBillRatesFetcher
from openbb_eodhd.providers.eodhd.models.ust_long_term_rates import UstLongTermRatesFetcher
from openbb_eodhd.providers.eodhd.models.ust_real_yield_rates import UstRealYieldRatesFetcher
from openbb_eodhd.providers.eodhd.models.ust_yield_rates import UstYieldRatesFetcher
from openbb_eodhd.providers.eodhd.models.v2_exchange_details import V2ExchangeDetailsFetcher

test_credentials = UserService().default_user_settings.credentials.model_dump(mode="json")


@pytest.fixture(scope="module")
def vcr_config():
    """Scrub credential fields from recorded cassettes."""
    return {
        "filter_headers": [
            ("Authorization", "Bearer MOCK_TOKEN"),
            ("Cookie", "MOCK_COOKIE"),
            ("Set-Cookie", "MOCK_COOKIE"),
            ("User-Agent", None),
            ("X-API-Key", "MOCK_API_KEY"),
            ("X-Access-Token", "MOCK_TOKEN"),
            ("X-Api-Key", "MOCK_API_KEY"),
            ("X-Auth-Token", "MOCK_TOKEN"),
            ("api-key", "MOCK_API_KEY"),
            ("apikey", "MOCK_API_KEY"),
        ],
        "filter_query_parameters": [
            ("access_token", "MOCK_TOKEN"),
            ("api-key", "MOCK_API_KEY"),
            ("api_key", "MOCK_API_KEY"),
            ("api_token", "MOCK_TOKEN"),
            ("apikey", "MOCK_API_KEY"),
            ("app_id", "MOCK_APP_ID"),
            ("app_key", "MOCK_APP_KEY"),
            ("app_token", "MOCK_TOKEN"),
            ("appid", "MOCK_APP_ID"),
            ("auth_token", "MOCK_TOKEN"),
            ("bearer_token", "MOCK_TOKEN"),
            ("client_id", "MOCK_CLIENT_ID"),
            ("client_secret", "MOCK_CLIENT_SECRET"),
            ("client_token", "MOCK_TOKEN"),
            ("consumer_key", "MOCK_API_KEY"),
            ("consumer_secret", "MOCK_SECRET"),
            ("key", "MOCK_API_KEY"),
            ("ocp_apim_subscription_key", "MOCK_API_KEY"),
            ("private_key", "MOCK_SECRET"),
            ("secret", "MOCK_SECRET"),
            ("secret_key", "MOCK_SECRET"),
            ("session_token", "MOCK_TOKEN"),
            ("subscription_key", "MOCK_API_KEY"),
            ("token", "MOCK_TOKEN"),
        ],
    }


@pytest.mark.skip(reason="HTTP 403: requires EODHD Corporate Events Package")
@pytest.mark.record_http
def test_calendar_dividends_fetcher(credentials=test_credentials):
    params = {
        "filter_date_eq_": "2026-07-19",
        "filter_date_from_": "2026-07-19",
        "filter_date_to_": "2026-07-19",
    }
    fetcher = CalendarDividendsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Corporate Events Package")
@pytest.mark.record_http
def test_calendar_earnings_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = CalendarEarningsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Corporate Events Package")
@pytest.mark.record_http
def test_calendar_ipos_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = CalendarIposFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Corporate Events Package")
@pytest.mark.record_http
def test_calendar_splits_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = CalendarSplitsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD CBOE Europe Indices subscription")
@pytest.mark.record_http
def test_cboe_indices_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CboeIndicesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_cds_market_aggregates_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskCdsMarketAggregatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_corporate_cmdi_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskCorporateCmdiFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_corporate_hqm_yields_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskCorporateHqmYieldsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_sovereign_cds_spreads_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskSovereignCdsSpreadsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_sovereign_credit_ratings_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskSovereignCreditRatingsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_sovereign_default_spreads_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskSovereignDefaultSpreadsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_credit_risk_sovereign_risk_premium_fetcher(credentials=test_credentials):
    params = {}
    fetcher = CreditRiskSovereignRiskPremiumFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_economic_events_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = EconomicEventsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_exchanges_list_fetcher(credentials=test_credentials):
    params = {}
    fetcher = ExchangesListFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_id_mapping_fetcher(credentials=test_credentials):
    params = {"filter_symbol_": "AAPL.US"}
    fetcher = IdMappingFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Fundamentals Data Package")
@pytest.mark.record_http
def test_insider_transactions_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = InsiderTransactionsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_internal_user_fetcher(credentials=test_credentials):
    params = {}
    fetcher = InternalUserFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Logos PNG Package")
@pytest.mark.record_http
def test_logo_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL.US"}
    fetcher = LogoFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Logos SVG Package")
@pytest.mark.record_http
def test_logo_svg_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL.US"}
    fetcher = LogoSvgFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD ESG Data Package")
@pytest.mark.record_http
def test_mp_investverte_companies_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpInvestverteCompaniesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD ESG Data Package")
@pytest.mark.record_http
def test_mp_investverte_countries_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpInvestverteCountriesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD ESG Data Package")
@pytest.mark.record_http
def test_mp_investverte_sectors_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpInvestverteSectorsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Smart Screener Package")
@pytest.mark.record_http
def test_mp_praams_explore_bond_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpPraamsExploreBondFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Smart Screener Package")
@pytest.mark.record_http
def test_mp_praams_explore_equity_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpPraamsExploreEquityFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Stock Options Package")
@pytest.mark.record_http
def test_mp_unicornbay_options_contracts_fetcher(credentials=test_credentials):
    params = {
        "filter_underlying_symbol_": "AAPL.US",
        "filter_exp_date_from_": "2026-07-19",
        "filter_exp_date_to_": "2026-10-19",
    }
    fetcher = MpUnicornbayOptionsContractsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Stock Options Package")
@pytest.mark.record_http
def test_mp_unicornbay_options_eod_fetcher(credentials=test_credentials):
    params = {
        "filter_underlying_symbol_": "AAPL.US",
        "filter_exp_date_from_": "2026-07-19",
        "filter_exp_date_to_": "2026-10-19",
    }
    fetcher = MpUnicornbayOptionsEodFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Stock Options Package")
@pytest.mark.record_http
def test_mp_unicornbay_options_underlying_symbols_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpUnicornbayOptionsUnderlyingSymbolsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Indices Historical Constituents Package")
@pytest.mark.record_http
def test_mp_unicornbay_spglobal_list_fetcher(credentials=test_credentials):
    params = {}
    fetcher = MpUnicornbaySpglobalListFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_news_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = NewsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_rates_policy_rates_fetcher(credentials=test_credentials):
    params = {}
    fetcher = RatesPolicyRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_rates_reference_rates_fetcher(credentials=test_credentials):
    params = {}
    fetcher = RatesReferenceRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD All-In-One plan")
@pytest.mark.record_http
def test_sanctions_entities_fetcher(credentials=test_credentials):
    params = {}
    fetcher = SanctionsEntitiesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD All-In-One plan")
@pytest.mark.record_http
def test_sanctions_programs_fetcher(credentials=test_credentials):
    params = {}
    fetcher = SanctionsProgramsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD All-In-One plan")
@pytest.mark.record_http
def test_sanctions_sources_fetcher(credentials=test_credentials):
    params = {}
    fetcher = SanctionsSourcesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD All-In-One plan")
@pytest.mark.record_http
def test_sanctions_vessels_fetcher(credentials=test_credentials):
    params = {}
    fetcher = SanctionsVesselsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD All World Extended or All-In-One plan")
@pytest.mark.record_http
def test_screener_fetcher(credentials=test_credentials):
    params = {}
    fetcher = ScreenerFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_spreads_funding_stress_fetcher(credentials=test_credentials):
    params = {}
    fetcher = SpreadsFundingStressFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_user_fetcher(credentials=test_credentials):
    params = {}
    fetcher = UserFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_ust_bill_rates_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = UstBillRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_ust_long_term_rates_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = UstLongTermRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_ust_real_yield_rates_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = UstRealYieldRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_ust_yield_rates_fetcher(credentials=test_credentials):
    params = {"from_": "2026-06-19", "to": "2026-07-19"}
    fetcher = UstYieldRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.skip(reason="HTTP 403: requires EODHD Trading Hours Package")
@pytest.mark.record_http
def test_v2_exchange_details_fetcher(credentials=test_credentials):
    params = {}
    fetcher = V2ExchangeDetailsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None
