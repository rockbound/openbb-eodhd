"""Router for mp.praams.bank.balance_sheet commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpPraamsBankBalanceSheetIsin")
async def isin(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns bank-specific balance sheet analysis for the specified ISIN from PRAAMS."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpPraamsBankBalanceSheetTicker")
async def ticker(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns bank-specific balance sheet analysis for the specified ticker from PRAAMS."""
    return await OBBject.from_query(Query(**locals()))
