"""Fetcher for mp.praams.analyse.bond — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/analyse/bond/{isin}`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field

from ....utils import safe_json_loads, unpack_response


class MpPraamsAnalyseBondQueryParams(QueryParams):
    """Query parameters for mp.praams.analyse.bond.

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


class MpPraamsAnalyseBondData(Data):
    """Response row for mp.praams.analyse.bond.

    Parameters
    ----------
    isin : str, optional
    name : str, optional
        Bond name.
    risk_score : float, optional
        PRAAMS risk score.
    risk_category : str, optional
        Risk category (e.g., 'Low', 'Medium', 'High').
    yield_to_maturity : float, optional
    duration : float, optional
        Modified duration.
    convexity : float, optional
    credit_rating : str, optional
    coupon_rate : float, optional
    maturity_date : datetime.date, optional
    issuer : str, optional
    """

    isin: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="Bond name.")
    risk_score: float | None = Field(default=None, description="PRAAMS risk score.")
    risk_category: str | None = Field(
        default=None,
        description="Risk category (e.g., 'Low', 'Medium', 'High').",
    )
    yield_to_maturity: float | None = Field(default=None, description="")
    duration: float | None = Field(default=None, description="Modified duration.")
    convexity: float | None = Field(default=None, description="")
    credit_rating: str | None = Field(default=None, description="")
    coupon_rate: float | None = Field(default=None, description="")
    maturity_date: datetime.date | None = Field(default=None, description="")
    issuer: str | None = Field(default=None, description="")


class MpPraamsAnalyseBondFetcher(
    Fetcher[MpPraamsAnalyseBondQueryParams, list[MpPraamsAnalyseBondData]]
):
    """Returns PRAAMS risk scoring and analysis for a specific bond identified by ISIN."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsAnalyseBondQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsAnalyseBondQueryParams
            Validated query parameters.
        """
        return MpPraamsAnalyseBondQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsAnalyseBondQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/analyse/bond/{isin} and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsAnalyseBondQueryParams
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
        _path = f"/mp/praams/analyse/bond/{query.isin}"

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
        query: MpPraamsAnalyseBondQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpPraamsAnalyseBondData] | AnnotatedResult[list[MpPraamsAnalyseBondData]]:
        """Type the unpacked rows as MpPraamsAnalyseBondData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsAnalyseBondQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsAnalyseBondData] | AnnotatedResult[list[MpPraamsAnalyseBondData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsAnalyseBondData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "name": {"description": "Bond name."},
            "risk_score": {"description": "PRAAMS risk score."},
            "risk_category": {"description": "Risk category (e.g., 'Low', 'Medium', 'High')."},
            "duration": {"description": "Modified duration."},
            "maturity_date": {"format": "date"},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
