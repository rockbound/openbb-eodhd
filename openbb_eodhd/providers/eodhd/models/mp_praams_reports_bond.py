"""Fetcher for mp.praams.reports.bond — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/reports/bond/{isin}`` via HTTP GET.
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


class MpPraamsReportsBondQueryParams(QueryParams):
    """Query parameters for mp.praams.reports.bond.

    Parameters
    ----------
    isin : str
        Bond ISIN code.
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    isin: str = Field(description="Bond ISIN code.")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpPraamsReportsBondDataRiskSummary(BaseModel):
    """MpPraamsReportsBondDataRiskSummary.

    Parameters
    ----------
    risk_score : float, optional
    risk_category : str, optional
    credit_risk : str, optional
    interest_rate_risk : str, optional
    """

    risk_score: float | None = Field(default=None, description="")
    risk_category: str | None = Field(default=None, description="")
    credit_risk: str | None = Field(default=None, description="")
    interest_rate_risk: str | None = Field(default=None, description="")


class MpPraamsReportsBondDataBondDetails(BaseModel):
    """MpPraamsReportsBondDataBondDetails.

    Parameters
    ----------
    coupon_rate : float, optional
    maturity_date : datetime.date, optional
    yield_to_maturity : float, optional
    duration : float, optional
    convexity : float, optional
    issuer : str, optional
    credit_rating : str, optional
    """

    coupon_rate: float | None = Field(default=None, description="")
    maturity_date: datetime.date | None = Field(default=None, description="")
    yield_to_maturity: float | None = Field(default=None, description="")
    duration: float | None = Field(default=None, description="")
    convexity: float | None = Field(default=None, description="")
    issuer: str | None = Field(default=None, description="")
    credit_rating: str | None = Field(default=None, description="")


class MpPraamsReportsBondData(Data):
    """Response row for mp.praams.reports.bond.

    Parameters
    ----------
    isin : str, optional
    name : str, optional
    report_date : datetime.date, optional
    risk_summary : MpPraamsReportsBondDataRiskSummary, optional
        Inner fields: risk_score (float), risk_category (str), credit_risk (str), interest_rate_risk (str).
    bond_details : MpPraamsReportsBondDataBondDetails, optional
        Inner fields: coupon_rate (float), maturity_date (date), yield_to_maturity (float), duration (float), convexity (float), issuer (str), credit_rating (str).
    """

    isin: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="")
    report_date: datetime.date | None = Field(default=None, description="")
    risk_summary: MpPraamsReportsBondDataRiskSummary | None = Field(
        default=None,
        description="Inner fields: risk_score (float), risk_category (str), credit_risk (str), interest_rate_risk (str).",
    )
    bond_details: MpPraamsReportsBondDataBondDetails | None = Field(
        default=None,
        description="Inner fields: coupon_rate (float), maturity_date (date), yield_to_maturity (float), duration (float), convexity (float), issuer (str), credit_rating (str).",
    )

    @field_validator("risk_summary", "bond_details", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class MpPraamsReportsBondFetcher(
    Fetcher[MpPraamsReportsBondQueryParams, list[MpPraamsReportsBondData]]
):
    """Returns a comprehensive PRAAMS report for a specific bond, including risk assessment and analytics."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsReportsBondQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsReportsBondQueryParams
            Validated query parameters.
        """
        return MpPraamsReportsBondQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsReportsBondQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/reports/bond/{isin} and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsReportsBondQueryParams
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
        _path = f"/mp/praams/reports/bond/{query.isin}"

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
        query: MpPraamsReportsBondQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpPraamsReportsBondData] | AnnotatedResult[list[MpPraamsReportsBondData]]:
        """Type the unpacked rows as MpPraamsReportsBondData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsReportsBondQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsReportsBondData] | AnnotatedResult[list[MpPraamsReportsBondData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsReportsBondData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"report_date": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
