"""Provider registration for eodhd — generated from spec."""

from openbb_core.provider.abstract.provider import Provider

from openbb_eodhd.providers.eodhd.models.bulk_fundamentals import BulkFundamentalsFetcher
from openbb_eodhd.providers.eodhd.models.calendar_dividends import CalendarDividendsFetcher
from openbb_eodhd.providers.eodhd.models.calendar_earnings import CalendarEarningsFetcher
from openbb_eodhd.providers.eodhd.models.calendar_ipos import CalendarIposFetcher
from openbb_eodhd.providers.eodhd.models.calendar_splits import CalendarSplitsFetcher
from openbb_eodhd.providers.eodhd.models.calendar_trends import CalendarTrendsFetcher
from openbb_eodhd.providers.eodhd.models.cboe_index import CboeIndexFetcher
from openbb_eodhd.providers.eodhd.models.cboe_indices import CboeIndicesFetcher
from openbb_eodhd.providers.eodhd.models.commodities_historical import CommoditiesHistoricalFetcher
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
from openbb_eodhd.providers.eodhd.models.div import DivFetcher
from openbb_eodhd.providers.eodhd.models.economic_events import EconomicEventsFetcher
from openbb_eodhd.providers.eodhd.models.eod import EodFetcher
from openbb_eodhd.providers.eodhd.models.eod_bulk_last_day import EodBulkLastDayFetcher
from openbb_eodhd.providers.eodhd.models.exchange_details import ExchangeDetailsFetcher
from openbb_eodhd.providers.eodhd.models.exchange_symbol_list import ExchangeSymbolListFetcher
from openbb_eodhd.providers.eodhd.models.exchanges_list import ExchangesListFetcher
from openbb_eodhd.providers.eodhd.models.fundamentals import FundamentalsFetcher
from openbb_eodhd.providers.eodhd.models.historical_market_cap import HistoricalMarketCapFetcher
from openbb_eodhd.providers.eodhd.models.id_mapping import IdMappingFetcher
from openbb_eodhd.providers.eodhd.models.insider_transactions import InsiderTransactionsFetcher
from openbb_eodhd.providers.eodhd.models.internal_user import InternalUserFetcher
from openbb_eodhd.providers.eodhd.models.intraday import IntradayFetcher
from openbb_eodhd.providers.eodhd.models.logo import LogoFetcher
from openbb_eodhd.providers.eodhd.models.logo_svg import LogoSvgFetcher
from openbb_eodhd.providers.eodhd.models.macro_indicator import MacroIndicatorFetcher
from openbb_eodhd.providers.eodhd.models.mp_investverte_companies import (
    MpInvestverteCompaniesFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_investverte_countries import (
    MpInvestverteCountriesFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_investverte_country import MpInvestverteCountryFetcher
from openbb_eodhd.providers.eodhd.models.mp_investverte_esg import MpInvestverteEsgFetcher
from openbb_eodhd.providers.eodhd.models.mp_investverte_sector import MpInvestverteSectorFetcher
from openbb_eodhd.providers.eodhd.models.mp_investverte_sectors import MpInvestverteSectorsFetcher
from openbb_eodhd.providers.eodhd.models.mp_praams_analyse_bond import MpPraamsAnalyseBondFetcher
from openbb_eodhd.providers.eodhd.models.mp_praams_analyse_equity_isin import (
    MpPraamsAnalyseEquityIsinFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_analyse_equity_ticker import (
    MpPraamsAnalyseEquityTickerFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_bank_balance_sheet_isin import (
    MpPraamsBankBalanceSheetIsinFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_bank_balance_sheet_ticker import (
    MpPraamsBankBalanceSheetTickerFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_bank_income_statement_isin import (
    MpPraamsBankIncomeStatementIsinFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_bank_income_statement_ticker import (
    MpPraamsBankIncomeStatementTickerFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_explore_bond import MpPraamsExploreBondFetcher
from openbb_eodhd.providers.eodhd.models.mp_praams_explore_equity import (
    MpPraamsExploreEquityFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_reports_bond import MpPraamsReportsBondFetcher
from openbb_eodhd.providers.eodhd.models.mp_praams_reports_equity_isin import (
    MpPraamsReportsEquityIsinFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_praams_reports_equity_ticker import (
    MpPraamsReportsEquityTickerFetcher,
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
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_spglobal_comp import (
    MpUnicornbaySpglobalCompFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_spglobal_list import (
    MpUnicornbaySpglobalListFetcher,
)
from openbb_eodhd.providers.eodhd.models.mp_unicornbay_tickdata_ticks import (
    MpUnicornbayTickdataTicksFetcher,
)
from openbb_eodhd.providers.eodhd.models.news import NewsFetcher
from openbb_eodhd.providers.eodhd.models.news_word_weights import NewsWordWeightsFetcher
from openbb_eodhd.providers.eodhd.models.rates_policy_rates import RatesPolicyRatesFetcher
from openbb_eodhd.providers.eodhd.models.rates_reference_rates import RatesReferenceRatesFetcher
from openbb_eodhd.providers.eodhd.models.real_time import RealTimeFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_entities import SanctionsEntitiesFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_programs import SanctionsProgramsFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_sources import SanctionsSourcesFetcher
from openbb_eodhd.providers.eodhd.models.sanctions_vessels import SanctionsVesselsFetcher
from openbb_eodhd.providers.eodhd.models.screener import ScreenerFetcher
from openbb_eodhd.providers.eodhd.models.search import SearchFetcher
from openbb_eodhd.providers.eodhd.models.sentiments import SentimentsFetcher
from openbb_eodhd.providers.eodhd.models.splits import SplitsFetcher
from openbb_eodhd.providers.eodhd.models.spreads_funding_stress import SpreadsFundingStressFetcher
from openbb_eodhd.providers.eodhd.models.symbol_change_history import SymbolChangeHistoryFetcher
from openbb_eodhd.providers.eodhd.models.technical import TechnicalFetcher
from openbb_eodhd.providers.eodhd.models.ticks import TicksFetcher
from openbb_eodhd.providers.eodhd.models.us_quote_delayed import UsQuoteDelayedFetcher
from openbb_eodhd.providers.eodhd.models.user import UserFetcher
from openbb_eodhd.providers.eodhd.models.ust_bill_rates import UstBillRatesFetcher
from openbb_eodhd.providers.eodhd.models.ust_long_term_rates import UstLongTermRatesFetcher
from openbb_eodhd.providers.eodhd.models.ust_real_yield_rates import UstRealYieldRatesFetcher
from openbb_eodhd.providers.eodhd.models.ust_yield_rates import UstYieldRatesFetcher
from openbb_eodhd.providers.eodhd.models.v1_1_bulk_fundamentals import V11BulkFundamentalsFetcher
from openbb_eodhd.providers.eodhd.models.v1_1_fundamentals import V11FundamentalsFetcher
from openbb_eodhd.providers.eodhd.models.v2_exchange_details import V2ExchangeDetailsFetcher

eodhd_provider = Provider(
    name="eodhd",
    description="eodhd provider proxied through https://eodhd.com/api.",
    credentials=[
        "api_token",
    ],
    website="https://eodhd.com/api",
    fetcher_dict={
        "BulkFundamentals": BulkFundamentalsFetcher,
        "CalendarDividends": CalendarDividendsFetcher,
        "CalendarEarnings": CalendarEarningsFetcher,
        "CalendarIpos": CalendarIposFetcher,
        "CalendarSplits": CalendarSplitsFetcher,
        "CalendarTrends": CalendarTrendsFetcher,
        "CommoditiesHistorical": CommoditiesHistoricalFetcher,
        "CreditRiskSovereignRiskPremium": CreditRiskSovereignRiskPremiumFetcher,
        "CreditRiskSovereignCreditRatings": CreditRiskSovereignCreditRatingsFetcher,
        "CreditRiskSovereignCdsSpreads": CreditRiskSovereignCdsSpreadsFetcher,
        "CreditRiskSovereignDefaultSpreads": CreditRiskSovereignDefaultSpreadsFetcher,
        "CreditRiskCorporateCmdi": CreditRiskCorporateCmdiFetcher,
        "CreditRiskCorporateHqmYields": CreditRiskCorporateHqmYieldsFetcher,
        "CreditRiskCdsMarketAggregates": CreditRiskCdsMarketAggregatesFetcher,
        "CboeIndex": CboeIndexFetcher,
        "CboeIndices": CboeIndicesFetcher,
        "Div": DivFetcher,
        "EconomicEvents": EconomicEventsFetcher,
        "Eod": EodFetcher,
        "EodBulkLastDay": EodBulkLastDayFetcher,
        "ExchangeDetails": ExchangeDetailsFetcher,
        "ExchangeSymbolList": ExchangeSymbolListFetcher,
        "ExchangesList": ExchangesListFetcher,
        "Fundamentals": FundamentalsFetcher,
        "IdMapping": IdMappingFetcher,
        "HistoricalMarketCap": HistoricalMarketCapFetcher,
        "InsiderTransactions": InsiderTransactionsFetcher,
        "InternalUser": InternalUserFetcher,
        "Intraday": IntradayFetcher,
        "Logo": LogoFetcher,
        "LogoSvg": LogoSvgFetcher,
        "MacroIndicator": MacroIndicatorFetcher,
        "MpInvestverteCompanies": MpInvestverteCompaniesFetcher,
        "MpInvestverteCountries": MpInvestverteCountriesFetcher,
        "MpInvestverteCountry": MpInvestverteCountryFetcher,
        "MpInvestverteEsg": MpInvestverteEsgFetcher,
        "MpInvestverteSector": MpInvestverteSectorFetcher,
        "MpInvestverteSectors": MpInvestverteSectorsFetcher,
        "MpPraamsAnalyseBond": MpPraamsAnalyseBondFetcher,
        "MpPraamsAnalyseEquityIsin": MpPraamsAnalyseEquityIsinFetcher,
        "MpPraamsAnalyseEquityTicker": MpPraamsAnalyseEquityTickerFetcher,
        "MpPraamsBankBalanceSheetIsin": MpPraamsBankBalanceSheetIsinFetcher,
        "MpPraamsBankBalanceSheetTicker": MpPraamsBankBalanceSheetTickerFetcher,
        "MpPraamsBankIncomeStatementIsin": MpPraamsBankIncomeStatementIsinFetcher,
        "MpPraamsBankIncomeStatementTicker": MpPraamsBankIncomeStatementTickerFetcher,
        "MpPraamsExploreBond": MpPraamsExploreBondFetcher,
        "MpPraamsExploreEquity": MpPraamsExploreEquityFetcher,
        "MpPraamsReportsBond": MpPraamsReportsBondFetcher,
        "MpPraamsReportsEquityIsin": MpPraamsReportsEquityIsinFetcher,
        "MpPraamsReportsEquityTicker": MpPraamsReportsEquityTickerFetcher,
        "MpUnicornbayOptionsContracts": MpUnicornbayOptionsContractsFetcher,
        "MpUnicornbayOptionsEod": MpUnicornbayOptionsEodFetcher,
        "MpUnicornbayOptionsUnderlyingSymbols": MpUnicornbayOptionsUnderlyingSymbolsFetcher,
        "MpUnicornbaySpglobalComp": MpUnicornbaySpglobalCompFetcher,
        "MpUnicornbaySpglobalList": MpUnicornbaySpglobalListFetcher,
        "MpUnicornbayTickdataTicks": MpUnicornbayTickdataTicksFetcher,
        "News": NewsFetcher,
        "NewsWordWeights": NewsWordWeightsFetcher,
        "RatesReferenceRates": RatesReferenceRatesFetcher,
        "RatesPolicyRates": RatesPolicyRatesFetcher,
        "RealTime": RealTimeFetcher,
        "SanctionsEntities": SanctionsEntitiesFetcher,
        "SanctionsVessels": SanctionsVesselsFetcher,
        "SanctionsPrograms": SanctionsProgramsFetcher,
        "SanctionsSources": SanctionsSourcesFetcher,
        "SpreadsFundingStress": SpreadsFundingStressFetcher,
        "Screener": ScreenerFetcher,
        "Search": SearchFetcher,
        "Sentiments": SentimentsFetcher,
        "Splits": SplitsFetcher,
        "SymbolChangeHistory": SymbolChangeHistoryFetcher,
        "Technical": TechnicalFetcher,
        "Ticks": TicksFetcher,
        "User": UserFetcher,
        "UsQuoteDelayed": UsQuoteDelayedFetcher,
        "UstBillRates": UstBillRatesFetcher,
        "UstLongTermRates": UstLongTermRatesFetcher,
        "UstRealYieldRates": UstRealYieldRatesFetcher,
        "UstYieldRates": UstYieldRatesFetcher,
        "V11BulkFundamentals": V11BulkFundamentalsFetcher,
        "V11Fundamentals": V11FundamentalsFetcher,
        "V2ExchangeDetails": V2ExchangeDetailsFetcher,
    },
)
