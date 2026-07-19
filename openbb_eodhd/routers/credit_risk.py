"""Router for credit-risk commands — generated from spec."""

from openbb_core.app.router import Router

from openbb_eodhd.routers.credit_risk_cds_market import router as _cds_market_router
from openbb_eodhd.routers.credit_risk_corporate import router as _corporate_router
from openbb_eodhd.routers.credit_risk_sovereign import router as _sovereign_router

router = Router(prefix="")

router.include_router(_cds_market_router, prefix="/cds_market")
router.include_router(_corporate_router, prefix="/corporate")
router.include_router(_sovereign_router, prefix="/sovereign")
