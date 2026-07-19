"""Router for ust commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="UstBillRates")
async def bill_rates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns daily US Treasury bill rates (discount rates for 4-week, 8-week, 13-week, 17-week, 26-week, and 52-week bills)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="UstLongTermRates")
async def long_term_rates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns US Treasury long-term average rates and extrapolation factors for maturities beyond 30 years."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="UstRealYieldRates")
async def real_yield_rates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns daily US Treasury real yield curve rates (TIPS-derived real yields for 5-year, 7-year, 10-year, 20-year, and 30-year maturities)."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="UstYieldRates")
async def yield_rates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns daily US Treasury yield curve rates (constant maturity rates for 1-month through 30-year maturities)."""
    return await OBBject.from_query(Query(**locals()))
