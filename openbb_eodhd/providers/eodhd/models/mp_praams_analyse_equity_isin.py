"""Fetcher for mp.praams.analyse.equity.isin — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/analyse/equity/isin/{isin}`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field

from ....utils import safe_json_loads, unpack_response


class MpPraamsAnalyseEquityIsinQueryParams(QueryParams):
    """Query parameters for mp.praams.analyse.equity.isin.

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


class MpPraamsAnalyseEquityIsinData(Data):
    """Response row for mp.praams.analyse.equity.isin.

    Parameters
    ----------
    isin : str, optional
    name : str, optional
    risk_score : float, optional
    risk_category : str, optional
    volatility : float, optional
    beta : float, optional
    sharpe_ratio : float, optional
    max_drawdown : float, optional
    sector : str, optional
    market_cap : float, optional
    """

    isin: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="")
    risk_score: float | None = Field(default=None, description="")
    risk_category: str | None = Field(default=None, description="")
    volatility: float | None = Field(default=None, description="")
    beta: float | None = Field(default=None, description="")
    sharpe_ratio: float | None = Field(default=None, description="")
    max_drawdown: float | None = Field(default=None, description="")
    sector: str | None = Field(default=None, description="")
    market_cap: float | None = Field(default=None, description="")


class MpPraamsAnalyseEquityIsinFetcher(
    Fetcher[MpPraamsAnalyseEquityIsinQueryParams, list[MpPraamsAnalyseEquityIsinData]]
):
    """Returns PRAAMS risk scoring and analysis for a specific equity identified by ISIN."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsAnalyseEquityIsinQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsAnalyseEquityIsinQueryParams
            Validated query parameters.
        """
        return MpPraamsAnalyseEquityIsinQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsAnalyseEquityIsinQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/analyse/equity/isin/{isin} and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsAnalyseEquityIsinQueryParams
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
        _path = f"/mp/praams/analyse/equity/isin/{query.isin}"

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
        query: MpPraamsAnalyseEquityIsinQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpPraamsAnalyseEquityIsinData] | AnnotatedResult[list[MpPraamsAnalyseEquityIsinData]]:
        """Type the unpacked rows as MpPraamsAnalyseEquityIsinData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsAnalyseEquityIsinQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsAnalyseEquityIsinData] | AnnotatedResult[list[MpPraamsAnalyseEquityIsinData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsAnalyseEquityIsinData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
