"""Router for credit-risk.corporate commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="CreditRiskCorporateCmdi")
async def cmdi(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns the Corporate Market Debt Index series, including overall market, investment-grade, and high-yield sub-indices."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CreditRiskCorporateHqmYields")
async def hqm_yields(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns High Quality Market corporate bond yield curve values (par and spot) across standard tenors."""
    return await OBBject.from_query(Query(**locals()))
