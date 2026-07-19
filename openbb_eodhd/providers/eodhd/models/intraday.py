"""Fetcher for intraday — generated from spec.

Hits ``https://eodhd.com/api/intraday/{ticker}`` via HTTP GET.
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


class IntradayQueryParams(QueryParams):
    """Query parameters for intraday.

    Parameters
    ----------
    ticker : str
        Ticker symbol with exchange code (e.g., 'AAPL.US').
    interval : Literal['1m', '5m', '15m', '30m', '1h']
        Interval for data points. Options are '1m' (1 minute), '5m' (5 minutes), '15m' (15 minutes), '30m' (30 minutes), and '1h' (1 hour). Choices: 1m, 5m, 15m, 30m, 1h.
    fmt : Literal['json', 'csv'], optional
        Response format. Defaults to CSV if not specified. Options are 'json' and 'csv'. Choices: json, csv. (default: 'json')
    from_ : int, optional
        Start datetime in Unix timestamp (UTC). For example, 1627896900 for '2021-08-02 09:35:00'.
    to : int, optional
        End datetime in Unix timestamp (UTC). For example, 1630575300 for '2021-09-02 09:35:00'.
    """

    ticker: str = Field(
        description="Ticker symbol with exchange code (e.g., 'AAPL.US').",
    )
    interval: Literal["1m", "5m", "15m", "30m", "1h"] = Field(
        description="Interval for data points. Options are '1m' (1 minute), '5m' (5 minutes), '15m' (15 minutes), '30m' (30 minutes), and '1h' (1 hour). Choices: 1m, 5m, 15m, 30m, 1h.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format. Defaults to CSV if not specified. Options are 'json' and 'csv'. Choices: json, csv.",
    )
    from_: int | None = Field(
        default=None,
        alias="from",
        description="Start datetime in Unix timestamp (UTC). For example, 1627896900 for '2021-08-02 09:35:00'.",
    )
    to: int | None = Field(
        default=None,
        description="End datetime in Unix timestamp (UTC). For example, 1630575300 for '2021-09-02 09:35:00'.",
    )


class IntradayData(Data):
    """Response row for intraday.

    Parameters
    ----------
    timestamp : int, optional
    gmtoffset : int, optional
    datetime : str, optional
    open : float, optional
    high : float, optional
    low : float, optional
    close : float, optional
    volume : int, optional
    """

    timestamp: int | None = Field(default=None, description="")
    gmtoffset: int | None = Field(default=None, description="")
    datetime: str | None = Field(default=None, description="")
    open: float | None = Field(default=None, description="")
    high: float | None = Field(default=None, description="")
    low: float | None = Field(default=None, description="")
    close: float | None = Field(default=None, description="")
    volume: int | None = Field(default=None, description="")


class IntradayFetcher(Fetcher[IntradayQueryParams, list[IntradayData]]):
    """Retrieve intraday historical stock data for a specific ticker."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> IntradayQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        IntradayQueryParams
            Validated query parameters.
        """
        return IntradayQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: IntradayQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/intraday/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : IntradayQueryParams
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
        _path = f"/intraday/{query.ticker}"

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
        query: IntradayQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[IntradayData] | AnnotatedResult[list[IntradayData]]:
        """Type the unpacked rows as IntradayData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : IntradayQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[IntradayData] | AnnotatedResult[list[IntradayData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [IntradayData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
