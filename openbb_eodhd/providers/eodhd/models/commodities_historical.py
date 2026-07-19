"""Fetcher for commodities.historical — generated from spec.

Hits ``https://eodhd.com/api/commodities/historical/{code}`` via HTTP GET.
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


class CommoditiesHistoricalQueryParams(QueryParams):
    """Query parameters for commodities.historical.

    Parameters
    ----------
    code : str
        Commodity code (e.g., 'WTI', 'BRENT', 'NATURAL_GAS', 'GOLD', 'SILVER', 'COPPER', 'PLATINUM', 'PALLADIUM', 'WHEAT', 'CORN', 'SOYBEANS', 'RICE', 'SUGAR', 'COFFEE', 'COTTON', 'COCOA', 'OATS', 'LUMBER', 'RUBBER', 'ETHANOL', 'PROPANE', 'URANIUM', 'COAL').
    interval : Literal['daily', 'weekly', 'monthly'], optional
        Data interval — 'daily' (default), 'weekly', or 'monthly'. Choices: daily, weekly, monthly. (default: 'daily')
    from_ : str, optional
        Start date in 'YYYY-MM-DD' format.
    to : str, optional
        End date in 'YYYY-MM-DD' format.
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    code: str = Field(
        description="Commodity code (e.g., 'WTI', 'BRENT', 'NATURAL_GAS', 'GOLD', 'SILVER', 'COPPER', 'PLATINUM', 'PALLADIUM', 'WHEAT', 'CORN', 'SOYBEANS', 'RICE', 'SUGAR', 'COFFEE', 'COTTON', 'COCOA', 'OATS', 'LUMBER', 'RUBBER', 'ETHANOL', 'PROPANE', 'URANIUM', 'COAL').",
    )
    interval: Literal["daily", "weekly", "monthly"] | None = Field(
        default="daily",
        description="Data interval — 'daily' (default), 'weekly', or 'monthly'. Choices: daily, weekly, monthly.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date in 'YYYY-MM-DD' format.",
    )
    to: str | None = Field(default=None, description="End date in 'YYYY-MM-DD' format.")
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class CommoditiesHistoricalData(Data):
    """Response row for commodities.historical.

    Parameters
    ----------
    date : datetime.date, optional
        Data date.
    open : float, optional
        Opening price.
    high : float, optional
        High price.
    low : float, optional
        Low price.
    close : float, optional
        Closing price.
    adjusted_close : float, optional
        Adjusted closing price.
    volume : float, optional
        Trading volume.
    """

    date: datetime.date | None = Field(default=None, description="Data date.")
    open: float | None = Field(default=None, description="Opening price.")
    high: float | None = Field(default=None, description="High price.")
    low: float | None = Field(default=None, description="Low price.")
    close: float | None = Field(default=None, description="Closing price.")
    adjusted_close: float | None = Field(
        default=None,
        description="Adjusted closing price.",
    )
    volume: float | None = Field(default=None, description="Trading volume.")


class CommoditiesHistoricalFetcher(
    Fetcher[CommoditiesHistoricalQueryParams, list[CommoditiesHistoricalData]]
):
    """Returns historical price data for a specific commodity by its code (e.g., WTI, BRENT, NATURAL_GAS)."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CommoditiesHistoricalQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CommoditiesHistoricalQueryParams
            Validated query parameters.
        """
        return CommoditiesHistoricalQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CommoditiesHistoricalQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/commodities/historical/{code} and split rows from metadata.

        Parameters
        ----------
        query : CommoditiesHistoricalQueryParams
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
        _path = f"/commodities/historical/{query.code}"

        _query_dict = query.model_dump(by_alias=True, exclude={"code"}, exclude_none=True)
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
        query: CommoditiesHistoricalQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CommoditiesHistoricalData] | AnnotatedResult[list[CommoditiesHistoricalData]]:
        """Type the unpacked rows as CommoditiesHistoricalData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CommoditiesHistoricalQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CommoditiesHistoricalData] | AnnotatedResult[list[CommoditiesHistoricalData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CommoditiesHistoricalData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Data date.", "format": "date"},
            "open": {"description": "Opening price."},
            "high": {"description": "High price."},
            "low": {"description": "Low price."},
            "close": {"description": "Closing price."},
            "adjusted_close": {"description": "Adjusted closing price."},
            "volume": {"description": "Trading volume."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
