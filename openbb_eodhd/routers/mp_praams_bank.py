"""Router for mp.praams.bank commands — generated from spec."""

from openbb_core.app.router import Router

from openbb_eodhd.routers.mp_praams_bank_balance_sheet import router as _balance_sheet_router
from openbb_eodhd.routers.mp_praams_bank_income_statement import router as _income_statement_router

router = Router(prefix="")

router.include_router(_balance_sheet_router, prefix="/balance_sheet")
router.include_router(_income_statement_router, prefix="/income_statement")
