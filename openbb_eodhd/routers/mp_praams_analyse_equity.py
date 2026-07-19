"""Router for mp.praams.analyse.equity commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpPraamsAnalyseEquityIsin")
async def isin(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns PRAAMS risk scoring and analysis for a specific equity identified by ISIN."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpPraamsAnalyseEquityTicker")
async def ticker(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns PRAAMS risk scoring and analysis for a specific equity identified by ticker."""
    return await OBBject.from_query(Query(**locals()))
