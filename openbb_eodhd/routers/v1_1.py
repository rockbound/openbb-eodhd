"""Router for v1_1 commands — generated from spec."""

from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import ExtraParams, ProviderChoices, StandardParams
from openbb_core.app.query import Query
from openbb_core.app.router import Router

router = Router(prefix="")


@router.command(model="V11BulkFundamentals")
async def bulk_fundamentals(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches fundamental data in bulk for all symbols on a given exchange using API v1.1. Supports filtering by specific symbols and data sections (General, Highlights, Valuation, etc.). In v1.1, the fmt parameter only supports json format."""
    return await OBBject.from_query(Query(**locals()))


@router.command(model="V11Fundamentals")
async def fundamentals(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject:
    """Fetches various sections of fundamental data for a given stock symbol using API v1.1. This version differs from v1 in the Earnings Trend section, which is split into Quarterly and Annual sub-objects with an additional "quarter" field on quarterly items. Use filters to specify the data section and sub-sections, such as Financials::Balance_Sheet::quarterly::2024-06-30 for quarterly Balance Sheet data."""
    return await OBBject.from_query(Query(**locals()))
