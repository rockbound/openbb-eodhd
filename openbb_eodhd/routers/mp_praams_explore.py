"""Router for mp.praams.explore commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpPraamsExploreBond")
async def bond(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Search and filter bonds using PRAAMS analytics. Returns a list of bonds matching the specified criteria with risk scores."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpPraamsExploreEquity")
async def equity(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Search and filter equities using PRAAMS analytics. Returns a list of equities matching the specified criteria with risk scores."""
    return await OBBject.from_query(Query(**locals()))
