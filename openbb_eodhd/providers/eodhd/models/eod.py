"""Fetcher for eod — generated from spec.

Hits ``https://eodhd.com/api/eod/{ticker}`` via HTTP GET.
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


class EodQueryParams(QueryParams):
    """Query parameters for eod.

    Parameters
    ----------
    ticker : str
        Ticker symbol of the company.
    fmt : Literal['json', 'csv'], optional
        Response format (e.g., 'json'). Choices: json, csv. (default: 'json')
    from_ : str, optional
        Start date for historical data (YYYY-MM-DD).
    to : str, optional
        End date for historical data (YYYY-MM-DD).
    period : Literal['d', 'w', 'm'], optional
        Data period (e.g., 'd' for daily, 'w' for weekly, 'm' for monthly). Choices: d, w, m.
    filter : Literal['last_date', 'last_open', 'last_high', 'last_low', 'last_close', 'last_volume'], optional
        Filter for specific last known data points. Choices: last_date, last_open, last_high, last_low, last_close, last_volume.
    """

    ticker: str = Field(description="Ticker symbol of the company.")
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format (e.g., 'json'). Choices: json, csv.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for historical data (YYYY-MM-DD).",
    )
    to: str | None = Field(
        default=None,
        description="End date for historical data (YYYY-MM-DD).",
    )
    period: Literal["d", "w", "m"] | None = Field(
        default=None,
        description="Data period (e.g., 'd' for daily, 'w' for weekly, 'm' for monthly). Choices: d, w, m.",
    )
    filter: (
        Literal["last_date", "last_open", "last_high", "last_low", "last_close", "last_volume"]
        | None
    ) = Field(
        default=None,
        description="Filter for specific last known data points. Choices: last_date, last_open, last_high, last_low, last_close, last_volume.",
    )


class EodData(Data):
    """Response row for eod.

    Parameters
    ----------
    date : datetime.date, optional
    open : float, optional
    high : float, optional
    low : float, optional
    close : float, optional
    adjusted_close : float, optional
    volume : int, optional
    """

    date: datetime.date | None = Field(default=None, description="")
    open: float | None = Field(default=None, description="")
    high: float | None = Field(default=None, description="")
    low: float | None = Field(default=None, description="")
    close: float | None = Field(default=None, description="")
    adjusted_close: float | None = Field(default=None, description="")
    volume: int | None = Field(default=None, description="")


class EodFetcher(Fetcher[EodQueryParams, list[EodData]]):
    """Retrieve end-of-day historical data for a specific company by its ticker symbol, with optional filters for specific data points."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> EodQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        EodQueryParams
            Validated query parameters.
        """
        return EodQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: EodQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/eod/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : EodQueryParams
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
        _path = f"/eod/{query.ticker}"

        _query_dict = query.model_dump(by_alias=True, exclude={"ticker"}, exclude_none=True)
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
        query: EodQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[EodData] | AnnotatedResult[list[EodData]]:
        """Type the unpacked rows as EodData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : EodQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[EodData] | AnnotatedResult[list[EodData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [EodData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"date": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
