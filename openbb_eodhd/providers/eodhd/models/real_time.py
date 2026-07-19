"""Fetcher for real-time — generated from spec.

Hits ``https://eodhd.com/api/real-time/{ticker}`` via HTTP GET.
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


class RealTimeQueryParams(QueryParams):
    """Query parameters for real-time.

    Parameters
    ----------
    ticker : str
        Ticker symbol with exchange code (e.g., 'AAPL.US').
    s : str, optional
        Comma-separated list of additional ticker symbols for multiple requests in a single call (e.g., 'VTI,EUR.FOREX').
    ex : str, optional
        Exchange code filter (e.g., 'US').
    fmt : Literal['json', 'csv'], optional
        Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv. (default: 'json')
    """

    ticker: str = Field(
        description="Ticker symbol with exchange code (e.g., 'AAPL.US').",
    )
    s: str | None = Field(
        default=None,
        description="Comma-separated list of additional ticker symbols for multiple requests in a single call (e.g., 'VTI,EUR.FOREX').",
    )
    ex: str | None = Field(
        default=None,
        description="Exchange code filter (e.g., 'US').",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv.",
    )


class RealTimeData(Data):
    """Response row for real-time.

    Parameters
    ----------
    code : str, optional
    timestamp : int, optional
    gmtoffset : int, optional
    open : float, optional
    high : float, optional
    low : float, optional
    close : float, optional
    volume : int, optional
    previousClose : float, optional
    change : float, optional
    change_p : float, optional
    """

    code: str | None = Field(default=None, description="")
    timestamp: int | None = Field(default=None, description="")
    gmtoffset: int | None = Field(default=None, description="")
    open: float | None = Field(default=None, description="")
    high: float | None = Field(default=None, description="")
    low: float | None = Field(default=None, description="")
    close: float | None = Field(default=None, description="")
    volume: int | None = Field(default=None, description="")
    previousClose: float | None = Field(default=None, description="")
    change: float | None = Field(default=None, description="")
    change_p: float | None = Field(default=None, description="")


class RealTimeFetcher(Fetcher[RealTimeQueryParams, list[RealTimeData]]):
    """Retrieve live (delayed) stock prices for specified ticker(s)."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> RealTimeQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        RealTimeQueryParams
            Validated query parameters.
        """
        return RealTimeQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: RealTimeQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/real-time/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : RealTimeQueryParams
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
        _path = f"/real-time/{query.ticker}"

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
        query: RealTimeQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[RealTimeData] | AnnotatedResult[list[RealTimeData]]:
        """Type the unpacked rows as RealTimeData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : RealTimeQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[RealTimeData] | AnnotatedResult[list[RealTimeData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [RealTimeData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
