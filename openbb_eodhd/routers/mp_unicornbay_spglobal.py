"""Router for mp.unicornbay.spglobal commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpUnicornbaySpglobalComp")
async def comp(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns the current components and historical changes for an index symbol."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpUnicornbaySpglobalList")
async def list(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns essential EOD details for 100+ S&P & Dow Jones indices."""
    return await OBBject.from_query(Query(**locals()))
