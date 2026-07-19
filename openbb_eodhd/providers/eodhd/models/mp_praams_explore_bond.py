"""Fetcher for mp.praams.explore.bond — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/explore/bond`` via HTTP GET.
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


class MpPraamsExploreBondQueryParams(QueryParams):
    """Query parameters for mp.praams.explore.bond.

    Parameters
    ----------
    risk_category : str, optional
        Filter by risk category (e.g., 'Low', 'Medium', 'High').
    min_yield : float, optional
        Minimum yield to maturity filter.
    max_yield : float, optional
        Maximum yield to maturity filter.
    currency : str, optional
        Filter by currency (e.g., 'USD', 'EUR').
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
    min_yield: float | None = Field(
        default=None,
        description="Minimum yield to maturity filter.",
    )
    max_yield: float | None = Field(
        default=None,
        description="Maximum yield to maturity filter.",
    )
    currency: str | None = Field(
        default=None,
        description="Filter by currency (e.g., 'USD', 'EUR').",
    )
    offset: int | None = Field(default=0, description="Pagination offset.")
    limit: int | None = Field(default=50, description="Maximum results to return.")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpPraamsExploreBondData(Data):
    """Response row for mp.praams.explore.bond.

    Parameters
    ----------
    isin : str, optional
    name : str, optional
    risk_score : float, optional
    risk_category : str, optional
    yield_to_maturity : float, optional
    coupon_rate : float, optional
    maturity_date : datetime.date, optional
    currency : str, optional
    credit_rating : str, optional
    """

    isin: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="")
    risk_score: float | None = Field(default=None, description="")
    risk_category: str | None = Field(default=None, description="")
    yield_to_maturity: float | None = Field(default=None, description="")
    coupon_rate: float | None = Field(default=None, description="")
    maturity_date: datetime.date | None = Field(default=None, description="")
    currency: str | None = Field(default=None, description="")
    credit_rating: str | None = Field(default=None, description="")


class MpPraamsExploreBondFetcher(
    Fetcher[MpPraamsExploreBondQueryParams, list[MpPraamsExploreBondData]]
):
    """Search and filter bonds using PRAAMS analytics. Returns a list of bonds matching the specified criteria with risk scores."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsExploreBondQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsExploreBondQueryParams
            Validated query parameters.
        """
        return MpPraamsExploreBondQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsExploreBondQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/explore/bond and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsExploreBondQueryParams
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
        _path = "/mp/praams/explore/bond"

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
        query: MpPraamsExploreBondQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpPraamsExploreBondData] | AnnotatedResult[list[MpPraamsExploreBondData]]:
        """Type the unpacked rows as MpPraamsExploreBondData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsExploreBondQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsExploreBondData] | AnnotatedResult[list[MpPraamsExploreBondData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsExploreBondData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"maturity_date": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
