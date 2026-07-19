"""Router for cboe commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="CboeIndex")
async def index(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns historical end-of-day data for a specific CBOE index, including daily open, high, low, close values."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="CboeIndices")
async def indices(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns a list of all available CBOE indices with their latest values and metadata."""
    return await OBBject.from_query(Query(**locals()))
