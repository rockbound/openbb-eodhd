"""Root router for eodhd — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

from openbb_eodhd.routers.calendar import router as _calendar_router
from openbb_eodhd.routers.cboe import router as _cboe_router
from openbb_eodhd.routers.commodities import router as _commodities_router
from openbb_eodhd.routers.credit_risk import router as _credit_risk_router
from openbb_eodhd.routers.mp import router as _mp_router
from openbb_eodhd.routers.rates import router as _rates_router
from openbb_eodhd.routers.sanctions import router as _sanctions_router
from openbb_eodhd.routers.spreads import router as _spreads_router
from openbb_eodhd.routers.ust import router as _ust_router
from openbb_eodhd.routers.v1_1 import router as _v1_1_router
from openbb_eodhd.routers.v2 import router as _v2_router

router = Router(prefix="")

router.include_router(_calendar_router, prefix="/calendar")
router.include_router(_cboe_router, prefix="/cboe")
router.include_router(_commodities_router, prefix="/commodities")
router.include_router(_credit_risk_router, prefix="/credit_risk")
router.include_router(_mp_router, prefix="/mp")
router.include_router(_rates_router, prefix="/rates")
router.include_router(_sanctions_router, prefix="/sanctions")
router.include_router(_spreads_router, prefix="/spreads")
router.include_router(_ust_router, prefix="/ust")
router.include_router(_v1_1_router, prefix="/v1_1")
router.include_router(_v2_router, prefix="/v2")


@router.command(model="BulkFundamentals")
async def bulk_fundamentals(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches fundamental data in bulk for all symbols on a given exchange. Supports filtering by specific symbols and data sections (General, Highlights, Valuation, etc.)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Div")
async def div(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches historical dividend data for a specified stock symbol, including key dividend dates and values."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="EconomicEvents")
async def economic_events(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches economic events by date range, country, comparison type, and other optional parameters."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Eod")
async def eod(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve end-of-day historical data for a specific company by its ticker symbol, with optional filters for specific data points."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="EodBulkLastDay")
async def eod_bulk_last_day(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve bulk end-of-day data, splits, or dividends for an entire exchange or specific tickers, with an option for extended data."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="ExchangeDetails")
async def exchange_details(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve exchange details, trading hours, holidays, and active tickers for a specified exchange."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="ExchangeSymbolList")
async def exchange_symbol_list(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a list of active or delisted symbols for the specified exchange, with optional filters by ticker type."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="ExchangesList")
async def exchanges_list(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve the list of supported exchanges with their details."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Fundamentals")
async def fundamentals(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches various sections of fundamental data for a given stock symbol. Use filters to specify the data section and sub-sections, such as Financials::Balance_Sheet::quarterly::2024-06-30 for quarterly Balance Sheet data."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="HistoricalMarketCap")
async def historical_market_cap(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches historical market capitalization for a specified stock symbol with weekly frequency."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="IdMapping")
async def id_mapping(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Look up securities by various identifiers including symbol, exchange code, ISIN, FIGI, LEI, CUSIP, and CIK.


    **At least one of the following filter parameters is required**:
    `filter[symbol]`, `filter[isin]`, `filter[figi]`, `filter[lei]`, `filter[cusip]`, `filter[cik]`, or `filter[ex]`.
    A request without any of these will return HTTP 422.
    """
    return await OBBject.from_query(Query(**locals()))


@router.command(model="InsiderTransactions")
async def insider_transactions(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetch insider transaction data for US-listed companies. Covers insider buys and sells, providing transaction details such as date, shares, and price."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="InternalUser")
async def internal_user(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetch detailed internal account information for the authenticated user, including subscription type, usage statistics, and available data feeds. Requires a valid `api_token` as a query parameter."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Intraday")
async def intraday(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve intraday historical stock data for a specific ticker."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Logo")
async def logo(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a 200x200 PNG logo (transparent background) for the given ticker symbol, formatted as {ticker}.{exchange} (e.g., AAPL.US)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="LogoSvg")
async def logo_svg(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns an SVG logo for the given ticker symbol, formatted as {ticker}.{exchange} (e.g., AAPL.US)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MacroIndicator")
async def macro_indicator(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches macroeconomic data for a selected indicator, such as GDP or inflation, by country code."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="News")
async def news(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve financial news articles for a specific company ticker or topic."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="NewsWordWeights")
async def news_word_weights(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns the most relevant words from financial news for the given ticker and period, with weights (frequency ? significance)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="RealTime")
async def real_time(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve live (delayed) stock prices for specified ticker(s)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Screener")
async def screener(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieves stock data filtered by criteria such as market capitalization, exchange, sector, and more. Results can be sorted and paginated."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Search")
async def search(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Search for stocks, companies, or ISINs by a query (e.g., company name, stock symbol, or ISIN)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Sentiments")
async def sentiments(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve sentiment analysis for financial news related to specified tickers."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Splits")
async def splits(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches historical stock split data for a specified ticker, including split dates and ratios."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="SymbolChangeHistory")
async def symbol_change_history(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Retrieve the symbol change history within a specified date range. Only US exchanges are currently supported."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Technical")
async def technical(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches technical indicator data, such as moving averages and other analytics, based on specified parameters."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="Ticks")
async def ticks(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get historical stock tick data for US equities using UNIX time for filtering. Limited to US exchanges."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="UsQuoteDelayed")
async def us_quote_delayed(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns 15-minute delayed quote data for US equities. Supports multiple symbols in a single request."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="User")
async def user(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns details about the authenticated user, including subscription info and API usage."""
    return await OBBject.from_query(Query(**locals()))
