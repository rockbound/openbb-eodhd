"""Router for mp.praams commands — generated from spec."""

from openbb_core.app.router import Router

from openbb_eodhd.routers.mp_praams_analyse import router as _analyse_router
from openbb_eodhd.routers.mp_praams_bank import router as _bank_router
from openbb_eodhd.routers.mp_praams_explore import router as _explore_router
from openbb_eodhd.routers.mp_praams_reports import router as _reports_router

router = Router(prefix="")

router.include_router(_analyse_router, prefix="/analyse")
router.include_router(_bank_router, prefix="/bank")
router.include_router(_explore_router, prefix="/explore")
router.include_router(_reports_router, prefix="/reports")
