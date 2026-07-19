"""Router for mp.unicornbay commands — generated from spec."""

from openbb_core.app.router import Router

from openbb_eodhd.routers.mp_unicornbay_options import router as _options_router
from openbb_eodhd.routers.mp_unicornbay_spglobal import router as _spglobal_router
from openbb_eodhd.routers.mp_unicornbay_tickdata import router as _tickdata_router

router = Router(prefix="")

router.include_router(_options_router, prefix="/options")
router.include_router(_spglobal_router, prefix="/spglobal")
router.include_router(_tickdata_router, prefix="/tickdata")
