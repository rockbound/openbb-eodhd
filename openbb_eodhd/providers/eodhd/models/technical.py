"""Fetcher for technical — generated from spec.

Hits ``https://eodhd.com/api/technical/{ticker}`` via HTTP GET.
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


class TechnicalQueryParams(QueryParams):
    """Query parameters for technical.

    Parameters
    ----------
    ticker : str
        Symbol in the format {SYMBOL_NAME}.{EXCHANGE_ID}, e.g., AAPL.US for Apple Inc.
    function : Literal['sma', 'ema', 'wma', 'volatility', 'stochastic', 'rsi', 'stddev', 'stochrsi', 'slope', 'dmi', 'adx', 'macd', 'atr', 'cci', 'sar', 'beta', 'bbands', 'splitadjusted', 'avgvol', 'avgvolccy']
        The function to calculate the technical indicator (e.g., 'sma' for Simple Moving Average). Choices: sma, ema, wma, volatility, stochastic, rsi, stddev, stochrsi, slope, dmi, adx, macd, atr, cci, sar, beta, bbands, splitadjusted, avgvol, avgvolccy.
    period : int, optional
        Number of data points used to calculate the indicator. Default is 50. (default: 50)
    from_ : str, optional
        Start date for data retrieval in 'YYYY-MM-DD' format.
    to : str, optional
        End date for data retrieval in 'YYYY-MM-DD' format.
    order : Literal['a', 'd'], optional
        Sort order of dates: 'a' for ascending, 'd' for descending. Default is ascending. Choices: a, d. (default: 'a')
    fmt : Literal['json', 'csv'], optional
        Output format, either 'json' or 'csv'. Default is 'json'. Choices: json, csv. (default: 'json')
    splitadjusted_only : Literal[0, 1], optional
        For select functions, adjust data only for splits by setting to '1'. Default is '0'. Choices: 0, 1. (default: 0)
    filter : str, optional
        Retrieve only the last value by specifying 'last_ema' or 'last_volume' as the filter.
    """

    ticker: str = Field(
        description="Symbol in the format {SYMBOL_NAME}.{EXCHANGE_ID}, e.g., AAPL.US for Apple Inc.",
    )
    function: Literal[
        "sma",
        "ema",
        "wma",
        "volatility",
        "stochastic",
        "rsi",
        "stddev",
        "stochrsi",
        "slope",
        "dmi",
        "adx",
        "macd",
        "atr",
        "cci",
        "sar",
        "beta",
        "bbands",
        "splitadjusted",
        "avgvol",
        "avgvolccy",
    ] = Field(
        description="The function to calculate the technical indicator (e.g., 'sma' for Simple Moving Average). Choices: sma, ema, wma, volatility, stochastic, rsi, stddev, stochrsi, slope, dmi, adx, macd, atr, cci, sar, beta, bbands, splitadjusted, avgvol, avgvolccy.",
    )
    period: int | None = Field(
        default=50,
        description="Number of data points used to calculate the indicator. Default is 50.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for data retrieval in 'YYYY-MM-DD' format.",
    )
    to: str | None = Field(
        default=None,
        description="End date for data retrieval in 'YYYY-MM-DD' format.",
    )
    order: Literal["a", "d"] | None = Field(
        default="a",
        description="Sort order of dates: 'a' for ascending, 'd' for descending. Default is ascending. Choices: a, d.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format, either 'json' or 'csv'. Default is 'json'. Choices: json, csv.",
    )
    splitadjusted_only: Literal[0, 1] | None = Field(
        default=0,
        description="For select functions, adjust data only for splits by setting to '1'. Default is '0'. Choices: 0, 1.",
    )
    filter: str | None = Field(
        default=None,
        description="Retrieve only the last value by specifying 'last_ema' or 'last_volume' as the filter.",
    )


class TechnicalData(Data):
    """Response row for technical.

    Parameters
    ----------
    date : datetime.date, optional
        Date of the data point.
    sma : float, optional
        Simple Moving Average value (specific to the chosen function).
    """

    date: datetime.date | None = Field(
        default=None,
        description="Date of the data point.",
    )
    sma: float | None = Field(
        default=None,
        description="Simple Moving Average value (specific to the chosen function).",
    )


class TechnicalFetcher(Fetcher[TechnicalQueryParams, list[TechnicalData]]):
    """Fetches technical indicator data, such as moving averages and other analytics, based on specified parameters."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> TechnicalQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        TechnicalQueryParams
            Validated query parameters.
        """
        return TechnicalQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: TechnicalQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/technical/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : TechnicalQueryParams
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
        _path = f"/technical/{query.ticker}"

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
        query: TechnicalQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[TechnicalData] | AnnotatedResult[list[TechnicalData]]:
        """Type the unpacked rows as TechnicalData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : TechnicalQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[TechnicalData] | AnnotatedResult[list[TechnicalData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [TechnicalData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Date of the data point.", "format": "date"},
            "sma": {
                "description": "Simple Moving Average value (specific to the chosen function)."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
