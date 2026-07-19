"""Router for mp.praams.reports.equity commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpPraamsReportsEquityIsin")
async def isin(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a comprehensive PRAAMS report for a specific equity identified by ISIN."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpPraamsReportsEquityTicker")
async def ticker(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a comprehensive PRAAMS report for a specific equity, including risk assessment and analytics."""
    return await OBBject.from_query(Query(**locals()))
