"""Router for v2 commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="V2ExchangeDetails")
async def exchange_details(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns trading hours, extended sessions (pre-market, after-hours), lunch breaks, and the full holiday calendar for the requested exchange. Covers 73 exchanges with verified data. The code parameter is case-insensitive."""
    return await OBBject.from_query(Query(**locals()))
