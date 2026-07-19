"""Fetcher for mp.praams.explore.equity — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/explore/equity`` via HTTP GET.
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


class MpPraamsExploreEquityQueryParams(QueryParams):
    """Query parameters for mp.praams.explore.equity.

    Parameters
    ----------
    risk_category : str, optional
        Filter by risk category (e.g., 'Low', 'Medium', 'High').
    sector : str, optional
        Filter by sector.
    country : str, optional
        Filter by country code.
    min_market_cap : float, optional
        Minimum market capitalization filter.
    offset : int, optional
        Pagination offset. (default: 0)
    limit : int, optional
        Maximum results to return. (default: 50)
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    risk_category: str | None = Field(
        default=None,
        description="Filter by risk category (e.g., 'Low', 'Medium', 'High').",
    )
    sector: str | None = Field(default=None, description="Filter by sector.")
    country: str | None = Field(default=None, description="Filter by country code.")
    min_market_cap: float | None = Field(
        default=None,
        description="Minimum market capitalization filter.",
    )
    offset: int | None = Field(default=0, description="Pagination offset.")
    limit: int | None = Field(default=50, description="Maximum results to return.")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpPraamsExploreEquityData(Data):
    """Response row for mp.praams.explore.equity.

    Parameters
    ----------
    ticker : str, optional
    isin : str, optional
    name : str, optional
    risk_score : float, optional
    risk_category : str, optional
    sector : str, optional
    country : str, optional
    market_cap : float, optional
    beta : float, optional
    """

    ticker: str | None = Field(default=None, description="")
    isin: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="")
    risk_score: float | None = Field(default=None, description="")
    risk_category: str | None = Field(default=None, description="")
    sector: str | None = Field(default=None, description="")
    country: str | None = Field(default=None, description="")
    market_cap: float | None = Field(default=None, description="")
    beta: float | None = Field(default=None, description="")


class MpPraamsExploreEquityFetcher(
    Fetcher[MpPraamsExploreEquityQueryParams, list[MpPraamsExploreEquityData]]
):
    """Search and filter equities using PRAAMS analytics. Returns a list of equities matching the specified criteria with risk scores."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsExploreEquityQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsExploreEquityQueryParams
            Validated query parameters.
        """
        return MpPraamsExploreEquityQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsExploreEquityQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/explore/equity and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsExploreEquityQueryParams
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
        _path = "/mp/praams/explore/equity"

        _query_dict = query.model_dump(by_alias=True, exclude_none=True)
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
        query: MpPraamsExploreEquityQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpPraamsExploreEquityData] | AnnotatedResult[list[MpPraamsExploreEquityData]]:
        """Type the unpacked rows as MpPraamsExploreEquityData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsExploreEquityQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsExploreEquityData] | AnnotatedResult[list[MpPraamsExploreEquityData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsExploreEquityData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
