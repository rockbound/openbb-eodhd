"""Fetcher for eod-bulk-last-day — generated from spec.

Hits ``https://eodhd.com/api/eod-bulk-last-day/{exchange}`` via HTTP GET.
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


class EodBulkLastDayQueryParams(QueryParams):
    """Query parameters for eod-bulk-last-day.

    Parameters
    ----------
    exchange : str
        Exchange symbol (e.g., 'VI' for Vienna or 'US' for the U.S.).
    fmt : Literal['json', 'csv'], optional
        Response format ('json' or 'csv'). Choices: json, csv. (default: 'json')
    type : Literal['eod', 'splits', 'dividends'], optional
        Data type ('eod' for end-of-day data, 'splits' for stock splits, 'dividends' for dividend information). Choices: eod, splits, dividends. (default: 'eod')
    date : str, optional
        Specific date for historical data (YYYY-MM-DD). Defaults to the last trading day.
    symbols : str, optional
        Comma-separated list of specific tickers to retrieve data for (e.g., 'MSFT,AAPL'). Only available for EOD data.
    filter : Literal['extended'], optional
        Extended filter for additional data such as company name, EMA, etc. Only available in JSON format. Choices: extended.
    """

    exchange: str = Field(
        description="Exchange symbol (e.g., 'VI' for Vienna or 'US' for the U.S.).",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format ('json' or 'csv'). Choices: json, csv.",
    )
    type: Literal["eod", "splits", "dividends"] | None = Field(
        default="eod",
        description="Data type ('eod' for end-of-day data, 'splits' for stock splits, 'dividends' for dividend information). Choices: eod, splits, dividends.",
    )
    date: str | None = Field(
        default=None,
        description="Specific date for historical data (YYYY-MM-DD). Defaults to the last trading day.",
    )
    symbols: str | None = Field(
        default=None,
        description="Comma-separated list of specific tickers to retrieve data for (e.g., 'MSFT,AAPL'). Only available for EOD data.",
    )
    filter: Literal["extended"] | None = Field(
        default=None,
        description="Extended filter for additional data such as company name, EMA, etc. Only available in JSON format. Choices: extended.",
    )


class EodBulkLastDayData(Data):
    """Response row for eod-bulk-last-day.

    Parameters
    ----------
    code : str, optional
        Ticker code.
    exchange_short_name : str
        Exchange symbol.
    date : datetime.date, optional
        Data date.
    open : float, optional
        Open price.
    high : float, optional
        High price.
    low : float, optional
        Low price.
    close : float, optional
        Close price.
    adjusted_close : float, optional
        Adjusted close price.
    volume : int, optional
        Trading volume.
    """

    code: str | None = Field(default=None, description="Ticker code.")
    exchange_short_name: str = Field(description="Exchange symbol.")
    date: datetime.date | None = Field(default=None, description="Data date.")
    open: float | None = Field(default=None, description="Open price.")
    high: float | None = Field(default=None, description="High price.")
    low: float | None = Field(default=None, description="Low price.")
    close: float | None = Field(default=None, description="Close price.")
    adjusted_close: float | None = Field(
        default=None,
        description="Adjusted close price.",
    )
    volume: int | None = Field(default=None, description="Trading volume.")


class EodBulkLastDayFetcher(Fetcher[EodBulkLastDayQueryParams, list[EodBulkLastDayData]]):
    """Retrieve bulk end-of-day data, splits, or dividends for an entire exchange or specific tickers, with an option for extended data."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> EodBulkLastDayQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        EodBulkLastDayQueryParams
            Validated query parameters.
        """
        return EodBulkLastDayQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: EodBulkLastDayQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/eod-bulk-last-day/{exchange} and split rows from metadata.

        Parameters
        ----------
        query : EodBulkLastDayQueryParams
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
        _path = f"/eod-bulk-last-day/{query.exchange}"

        _query_dict = query.model_dump(by_alias=True, exclude={"exchange"}, exclude_none=True)
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
        query: EodBulkLastDayQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[EodBulkLastDayData] | AnnotatedResult[list[EodBulkLastDayData]]:
        """Type the unpacked rows as EodBulkLastDayData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : EodBulkLastDayQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[EodBulkLastDayData] | AnnotatedResult[list[EodBulkLastDayData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [EodBulkLastDayData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker code."},
            "exchange_short_name": {"description": "Exchange symbol."},
            "date": {"description": "Data date.", "format": "date"},
            "open": {"description": "Open price."},
            "high": {"description": "High price."},
            "low": {"description": "Low price."},
            "close": {"description": "Close price."},
            "adjusted_close": {"description": "Adjusted close price."},
            "volume": {"description": "Trading volume."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
