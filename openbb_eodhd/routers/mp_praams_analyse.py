"""Router for mp.praams.analyse commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

from openbb_eodhd.routers.mp_praams_analyse_equity import router as _equity_router

router = Router(prefix="")

router.include_router(_equity_router, prefix="/equity")


@router.command(model="MpPraamsAnalyseBond")
async def bond(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns PRAAMS risk scoring and analysis for a specific bond identified by ISIN."""
    return await OBBject.from_query(Query(**locals()))
