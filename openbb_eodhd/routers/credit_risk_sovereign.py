"""Router for credit-risk.sovereign commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="CreditRiskSovereignCdsSpreads")
async def cds_spreads(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns sovereign credit default swap (CDS) spreads by country, including spreads net of Switzerland."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CreditRiskSovereignCreditRatings")
async def credit_ratings(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns sovereign credit ratings by country from Moody's, S&P, and Fitch."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CreditRiskSovereignDefaultSpreads")
async def default_spreads(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns default spreads mapped to credit rating buckets."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CreditRiskSovereignRiskPremium")
async def risk_premium(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns country-level default spreads, country risk premiums, equity risk premiums, corporate tax rates, and related sovereign credit metrics."""
    return await OBBject.from_query(Query(**locals()))
