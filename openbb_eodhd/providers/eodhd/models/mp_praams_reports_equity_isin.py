"""Fetcher for mp.praams.reports.equity.isin — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/reports/equity/isin/{isin}`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field, field_validator

from ....utils import safe_json_loads, unpack_response


class MpPraamsReportsEquityIsinQueryParams(QueryParams):
    """Query parameters for mp.praams.reports.equity.isin.

    Parameters
    ----------
    isin : str
        Equity ISIN code.
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    isin: str = Field(description="Equity ISIN code.")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpPraamsReportsEquityIsinDataRiskSummary(BaseModel):
    """MpPraamsReportsEquityIsinDataRiskSummary.

    Parameters
    ----------
    risk_score : float, optional
    risk_category : str, optional
    volatility_risk : str, optional
    market_risk : str, optional
    """

    risk_score: float | None = Field(default=None, description="")
    risk_category: str | None = Field(default=None, description="")
    volatility_risk: str | None = Field(default=None, description="")
    market_risk: str | None = Field(default=None, description="")


class MpPraamsReportsEquityIsinDataEquityDetails(BaseModel):
    """MpPraamsReportsEquityIsinDataEquityDetails.

    Parameters
    ----------
    sector : str, optional
    market_cap : float, optional
    beta : float, optional
    pe_ratio : float, optional
    dividend_yield : float, optional
    """

    sector: str | None = Field(default=None, description="")
    market_cap: float | None = Field(default=None, description="")
    beta: float | None = Field(default=None, description="")
    pe_ratio: float | None = Field(default=None, description="")
    dividend_yield: float | None = Field(default=None, description="")


class MpPraamsReportsEquityIsinDataPerformance(BaseModel):
    """MpPraamsReportsEquityIsinDataPerformance.

    Parameters
    ----------
    return_1y : float, optional
    return_3y : float, optional
    sharpe_ratio : float, optional
    max_drawdown : float, optional
    """

    return_1y: float | None = Field(default=None, description="")
    return_3y: float | None = Field(default=None, description="")
    sharpe_ratio: float | None = Field(default=None, description="")
    max_drawdown: float | None = Field(default=None, description="")


class MpPraamsReportsEquityIsinData(Data):
    """Response row for mp.praams.reports.equity.isin.

    Parameters
    ----------
    isin : str, optional
    name : str, optional
    report_date : datetime.date, optional
    risk_summary : MpPraamsReportsEquityIsinDataRiskSummary, optional
        Inner fields: risk_score (float), risk_category (str), volatility_risk (str), market_risk (str).
    equity_details : MpPraamsReportsEquityIsinDataEquityDetails, optional
        Inner fields: sector (str), market_cap (float), beta (float), pe_ratio (float), dividend_yield (float).
    performance : MpPraamsReportsEquityIsinDataPerformance, optional
        Inner fields: return_1y (float), return_3y (float), sharpe_ratio (float), max_drawdown (float).
    """

    isin: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="")
    report_date: datetime.date | None = Field(default=None, description="")
    risk_summary: MpPraamsReportsEquityIsinDataRiskSummary | None = Field(
        default=None,
        description="Inner fields: risk_score (float), risk_category (str), volatility_risk (str), market_risk (str).",
    )
    equity_details: MpPraamsReportsEquityIsinDataEquityDetails | None = Field(
        default=None,
        description="Inner fields: sector (str), market_cap (float), beta (float), pe_ratio (float), dividend_yield (float).",
    )
    performance: MpPraamsReportsEquityIsinDataPerformance | None = Field(
        default=None,
        description="Inner fields: return_1y (float), return_3y (float), sharpe_ratio (float), max_drawdown (float).",
    )

    @field_validator("risk_summary", "equity_details", "performance", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class MpPraamsReportsEquityIsinFetcher(
    Fetcher[MpPraamsReportsEquityIsinQueryParams, list[MpPraamsReportsEquityIsinData]]
):
    """Returns a comprehensive PRAAMS report for a specific equity identified by ISIN."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsReportsEquityIsinQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsReportsEquityIsinQueryParams
            Validated query parameters.
        """
        return MpPraamsReportsEquityIsinQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsReportsEquityIsinQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/reports/equity/isin/{isin} and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsReportsEquityIsinQueryParams
            Validated query parameters.
        credentials : dict[str, str] | None
            Provider credentials registered on the ``Provider`` instance.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        dict[str, Any]
            ``{'rows': [...], 'metadata': {...}}`` — single-element list and single-key envelope wrappers are stripped at the response boundary, scalar fields beside the data array become metadata.
        """
        _creds = credentials or {}
        _cred_api_token = _creds.get("eodhd_api_token", "")
        _path = f"/mp/praams/reports/equity/isin/{query.isin}"

        _query_dict = query.model_dump(by_alias=True, exclude={"isin"}, exclude_none=True)
        if _cred_api_token:
            _query_dict["api_token"] = _cred_api_token
        _query_string = get_querystring(_query_dict, [])
        _url = f"https://eodhd.com/api{_path}" + ("?" + _query_string if _query_string else "")

        _headers: dict[str, str] = {}

        _method = "GET"
        _request_kwargs: dict[str, Any] = {}
        async with await get_async_requests_session() as _session:
            async with await _session.request(
                _method, _url, headers=_headers, **_request_kwargs
            ) as _resp:
                _ct = (_resp.headers.get("Content-Type") or "").lower()
                _text = await _resp.text()
                if _resp.status >= 400:
                    raise OpenBBError(f"HTTP {_resp.status} from {_url}: {_text[:500]}")
                if "json" in _ct or _text.lstrip().startswith(("{", "[")):
                    try:
                        _payload = safe_json_loads(_text)
                    except ValueError as _exc:
                        raise OpenBBError(
                            f"Upstream {_url} returned malformed JSON: {_exc}"
                        ) from _exc
                else:
                    return {"rows": [{"content": _text, "content_type": _ct}], "metadata": {}}
        _rows, _metadata = unpack_response(_payload)
        return {"rows": _rows, "metadata": _metadata}

    @staticmethod
    def transform_data(
        query: MpPraamsReportsEquityIsinQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpPraamsReportsEquityIsinData] | AnnotatedResult[list[MpPraamsReportsEquityIsinData]]:
        """Type the unpacked rows as MpPraamsReportsEquityIsinData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsReportsEquityIsinQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsReportsEquityIsinData] | AnnotatedResult[list[MpPraamsReportsEquityIsinData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsReportsEquityIsinData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"report_date": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
