"""Fetcher for logo-svg — generated from spec.

Hits ``https://eodhd.com/api/logo-svg/{symbol}`` via HTTP GET.
"""

from typing import Any

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field

from ....utils import safe_json_loads, unpack_response


class LogoSvgQueryParams(QueryParams):
    """Query parameters for logo-svg.

    Parameters
    ----------
    symbol : str
        Ticker with exchange, e.g., AAPL.US.
    """

    symbol: str = Field(description="Ticker with exchange, e.g., AAPL.US.")


class LogoSvgData(Data):
    """Response row for logo-svg.

    Parameters
    ----------
    value : str
    """

    value: str = Field(description="")


class LogoSvgFetcher(Fetcher[LogoSvgQueryParams, list[LogoSvgData]]):
    """Returns an SVG logo for the given ticker symbol, formatted as {ticker}.{exchange} (e.g., AAPL.US)."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> LogoSvgQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        LogoSvgQueryParams
            Validated query parameters.
        """
        return LogoSvgQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: LogoSvgQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/logo-svg/{symbol} and split rows from metadata.

        Parameters
        ----------
        query : LogoSvgQueryParams
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
        _path = f"/logo-svg/{query.symbol}"

        _query_dict = query.model_dump(by_alias=True, exclude={"symbol"}, exclude_none=True)
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
        query: LogoSvgQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[LogoSvgData] | AnnotatedResult[list[LogoSvgData]]:
        """Type the unpacked rows as LogoSvgData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : LogoSvgQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[LogoSvgData] | AnnotatedResult[list[LogoSvgData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [LogoSvgData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
