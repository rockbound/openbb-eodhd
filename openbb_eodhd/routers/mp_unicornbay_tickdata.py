"""Router for mp.unicornbay.tickdata commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpUnicornbayTickdataTicks")
async def ticks(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Get tick-level data via the UnicornBay marketplace data provider. Returns granular trade-by-trade data for supported symbols."""
    return await OBBject.from_query(Query(**locals()))
