"""Fetcher for mp.unicornbay.tickdata.ticks — generated from spec.

Hits ``https://eodhd.com/api/mp/unicornbay/tickdata/ticks`` via HTTP GET.
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


class MpUnicornbayTickdataTicksQueryParams(QueryParams):
    """Query parameters for mp.unicornbay.tickdata.ticks.

    Parameters
    ----------
    s : str
        Ticker symbol (e.g., 'AAPL' or 'AAPL.US').
    from_ : int, optional
        Start UNIX timestamp (UTC).
    to : int, optional
        End UNIX timestamp (UTC).
    limit : int, optional
        Maximum number of ticks to return.
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    s: str = Field(description="Ticker symbol (e.g., 'AAPL' or 'AAPL.US').")
    from_: int | None = Field(
        default=None,
        alias="from",
        description="Start UNIX timestamp (UTC).",
    )
    to: int | None = Field(default=None, description="End UNIX timestamp (UTC).")
    limit: int | None = Field(
        default=None,
        description="Maximum number of ticks to return.",
    )
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpUnicornbayTickdataTicksData(Data):
    """Response row for mp.unicornbay.tickdata.ticks.

    Parameters
    ----------
    timestamp : int, optional
        Trade timestamp in milliseconds since epoch.
    price : float, optional
        Trade price.
    volume : int, optional
        Number of shares traded.
    exchange : str, optional
        Exchange code where trade occurred.
    conditions : str, optional
        Trade condition codes.
    """

    timestamp: int | None = Field(
        default=None,
        description="Trade timestamp in milliseconds since epoch.",
    )
    price: float | None = Field(default=None, description="Trade price.")
    volume: int | None = Field(default=None, description="Number of shares traded.")
    exchange: str | None = Field(
        default=None,
        description="Exchange code where trade occurred.",
    )
    conditions: str | None = Field(default=None, description="Trade condition codes.")


class MpUnicornbayTickdataTicksFetcher(
    Fetcher[MpUnicornbayTickdataTicksQueryParams, list[MpUnicornbayTickdataTicksData]]
):
    """Get tick-level data via the UnicornBay marketplace data provider. Returns granular trade-by-trade data for supported symbols."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpUnicornbayTickdataTicksQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpUnicornbayTickdataTicksQueryParams
            Validated query parameters.
        """
        return MpUnicornbayTickdataTicksQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpUnicornbayTickdataTicksQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/unicornbay/tickdata/ticks and split rows from metadata.

        Parameters
        ----------
        query : MpUnicornbayTickdataTicksQueryParams
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
        _path = "/mp/unicornbay/tickdata/ticks"

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
        query: MpUnicornbayTickdataTicksQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpUnicornbayTickdataTicksData] | AnnotatedResult[list[MpUnicornbayTickdataTicksData]]:
        """Type the unpacked rows as MpUnicornbayTickdataTicksData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpUnicornbayTickdataTicksQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpUnicornbayTickdataTicksData] | AnnotatedResult[list[MpUnicornbayTickdataTicksData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpUnicornbayTickdataTicksData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "timestamp": {
                "description": "Trade timestamp in milliseconds since epoch.",
                "format": "int64",
            },
            "price": {"description": "Trade price."},
            "volume": {"description": "Number of shares traded."},
            "exchange": {"description": "Exchange code where trade occurred."},
            "conditions": {"description": "Trade condition codes."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
