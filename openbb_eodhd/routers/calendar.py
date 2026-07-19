"""Router for calendar commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="CalendarDividends")
async def dividends(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Look up upcoming and historical dividend events.


    Uses the JSON:API filter/page convention. **At least one of `filter[date_eq]` or `filter[symbol]` is required** — a request without either will return HTTP 422.
    """
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CalendarEarnings")
async def earnings(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches upcoming earnings data, with optional parameters for date ranges and specific symbols."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CalendarIpos")
async def ipos(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches historical and upcoming IPOs for specified date ranges."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CalendarSplits")
async def splits(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches information on stock splits for specified date ranges."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CalendarTrends")
async def trends(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches historical and upcoming earnings trends, including EPS and revenue estimates, trends, and revisions for specific stock symbols."""
    return await OBBject.from_query(Query(**locals()))
