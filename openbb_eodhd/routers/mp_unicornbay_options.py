"""Router for mp.unicornbay.options commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="MpUnicornbayOptionsContracts")
async def contracts(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetch options contracts filtered by underlying symbol, expiration, strike, type, or contract name. Supports sorting, pagination, and field selection."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpUnicornbayOptionsEod")
async def eod(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns EOD trades/bid data for options, with the same filter set as contracts. Supports compact mode (`compact=1`) to return arrays instead of objects."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="MpUnicornbayOptionsUnderlyingSymbols")
async def underlying_symbols(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Returns the list of all supported stock symbols for which option contracts are available. May be paginated."""
    return await OBBject.from_query(Query(**locals()))
