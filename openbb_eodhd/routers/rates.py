"""Router for rates commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="RatesPolicyRates")
async def policy_rates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns central bank policy (target) interest rates by code, country, and central bank."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="RatesReferenceRates")
async def reference_rates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns benchmark reference interest rates (e.g., SOFR, SONIA, ESTR) by code and currency."""
    return await OBBject.from_query(Query(**locals()))
