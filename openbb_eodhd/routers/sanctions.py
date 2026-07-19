"""Router for sanctions commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="SanctionsEntities")
async def entities(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns sanctioned entities (individuals and organizations) aggregated from OFAC and other sanctions sources, including programs, aliases, and identifiers."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="SanctionsPrograms")
async def programs(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns the list of sanctions programs with the count of listed entities per program."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="SanctionsSources")
async def sources(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns the list of sanctions data sources available in the dataset."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="SanctionsVessels")
async def vessels(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns sanctioned vessels aggregated from OFAC and other sanctions sources, including IMO/MMSI identifiers, flag, and linked sanctioned entity."""
    return await OBBject.from_query(Query(**locals()))
