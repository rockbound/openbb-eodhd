"""Router for mp.investverte commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpInvestverteCompanies")
async def companies(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a list of all companies with ESG ratings available from Investverte."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpInvestverteCountries")
async def countries(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a list of all countries with their aggregate ESG scores from Investverte."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpInvestverteCountry")
async def country(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns detailed ESG scores and metrics for a specific country from Investverte."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpInvestverteEsg")
async def esg(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns detailed ESG ratings and scores for a specific company from Investverte."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpInvestverteSector")
async def sector(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns detailed ESG scores and metrics for a specific sector from Investverte."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpInvestverteSectors")
async def sectors(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a list of all sectors with their aggregate ESG scores from Investverte."""
    return await OBBject.from_query(Query(**locals()))
