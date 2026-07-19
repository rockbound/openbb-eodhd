"""Fetcher for us-quote-delayed — generated from spec.

Hits ``https://eodhd.com/api/us-quote-delayed`` via HTTP GET.
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


class UsQuoteDelayedQueryParams(QueryParams):
    """Query parameters for us-quote-delayed.

    Parameters
    ----------
    s : str
        Comma-separated ticker symbols (e.g., 'AAPL,MSFT,GOOGL').
    fields : str, optional
        Comma-separated list of fields to return (e.g., 'close,volume,change_p').
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    s: str = Field(
        description="Comma-separated ticker symbols (e.g., 'AAPL,MSFT,GOOGL').",
    )
    fields: str | None = Field(
        default=None,
        description="Comma-separated list of fields to return (e.g., 'close,volume,change_p').",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class UsQuoteDelayedData(Data):
    """Response row for us-quote-delayed.

    Parameters
    ----------
    code : str, optional
        Ticker symbol.
    timestamp : int, optional
        UNIX timestamp of the quote.
    gmtoffset : int, optional
        GMT offset in seconds.
    open : float, optional
        Opening price.
    high : float, optional
        High price.
    low : float, optional
        Low price.
    close : float, optional
        Last traded price.
    volume : int, optional
        Trading volume.
    previousClose : float, optional
        Previous day closing price.
    change : float, optional
        Price change.
    change_p : float, optional
        Percentage price change.
    """

    code: str | None = Field(default=None, description="Ticker symbol.")
    timestamp: int | None = Field(
        default=None,
        description="UNIX timestamp of the quote.",
    )
    gmtoffset: int | None = Field(default=None, description="GMT offset in seconds.")
    open: float | None = Field(default=None, description="Opening price.")
    high: float | None = Field(default=None, description="High price.")
    low: float | None = Field(default=None, description="Low price.")
    close: float | None = Field(default=None, description="Last traded price.")
    volume: int | None = Field(default=None, description="Trading volume.")
    previousClose: float | None = Field(
        default=None,
        description="Previous day closing price.",
    )
    change: float | None = Field(default=None, description="Price change.")
    change_p: float | None = Field(default=None, description="Percentage price change.")


class UsQuoteDelayedFetcher(Fetcher[UsQuoteDelayedQueryParams, list[UsQuoteDelayedData]]):
    """Returns 15-minute delayed quote data for US equities. Supports multiple symbols in a single request."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> UsQuoteDelayedQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        UsQuoteDelayedQueryParams
            Validated query parameters.
        """
        return UsQuoteDelayedQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UsQuoteDelayedQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/us-quote-delayed and split rows from metadata.

        Parameters
        ----------
        query : UsQuoteDelayedQueryParams
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
        _path = "/us-quote-delayed"

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
        query: UsQuoteDelayedQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[UsQuoteDelayedData] | AnnotatedResult[list[UsQuoteDelayedData]]:
        """Type the unpacked rows as UsQuoteDelayedData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : UsQuoteDelayedQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[UsQuoteDelayedData] | AnnotatedResult[list[UsQuoteDelayedData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [UsQuoteDelayedData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker symbol."},
            "timestamp": {"description": "UNIX timestamp of the quote.", "format": "int64"},
            "gmtoffset": {"description": "GMT offset in seconds."},
            "open": {"description": "Opening price."},
            "high": {"description": "High price."},
            "low": {"description": "Low price."},
            "close": {"description": "Last traded price."},
            "volume": {"description": "Trading volume."},
            "previousClose": {"description": "Previous day closing price."},
            "change": {"description": "Price change."},
            "change_p": {"description": "Percentage price change."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
