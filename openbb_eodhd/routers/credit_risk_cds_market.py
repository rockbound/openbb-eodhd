"""Router for credit-risk.cds-market commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="CreditRiskCdsMarketAggregates")
async def aggregates(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns aggregated CDS market statistics (e.g., gross notional) broken down by dimensions such as grade or cleared status."""
    return await OBBject.from_query(Query(**locals()))
