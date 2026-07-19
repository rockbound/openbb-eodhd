"""Router for mp commands — generated from spec."""

from openbb_core.app.router import Router

from openbb_eodhd.routers.mp_investverte import router as _investverte_router
from openbb_eodhd.routers.mp_praams import router as _praams_router
from openbb_eodhd.routers.mp_unicornbay import router as _unicornbay_router

router = Router(prefix="")

router.include_router(_investverte_router, prefix="/investverte")
router.include_router(_praams_router, prefix="/praams")
router.include_router(_unicornbay_router, prefix="/unicornbay")
