"""Fetcher for ticks — generated from spec.

Hits ``https://eodhd.com/api/ticks`` via HTTP GET.
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


class TicksQueryParams(QueryParams):
    """Query parameters for ticks.

    Parameters
    ----------
    s : str
        Ticker symbol (e.g., 'AAPL' or 'AAPL.US' for US-listed stocks).
    from_ : int, optional
        Start UNIX timestamp (UTC) for filtering data.
    to : int, optional
        End UNIX timestamp (UTC) for filtering data.
    limit : int, optional
        Maximum number of ticks to return.
    fmt : Literal['json'], optional
        Output format (only 'json' supported). Choices: json. (default: 'json')
    """

    s: str = Field(
        description="Ticker symbol (e.g., 'AAPL' or 'AAPL.US' for US-listed stocks).",
    )
    from_: int | None = Field(
        default=None,
        alias="from",
        description="Start UNIX timestamp (UTC) for filtering data.",
    )
    to: int | None = Field(
        default=None,
        description="End UNIX timestamp (UTC) for filtering data.",
    )
    limit: int | None = Field(
        default=None,
        description="Maximum number of ticks to return.",
    )
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format (only 'json' supported). Choices: json.",
    )


class TicksData(Data):
    """Response row for ticks.

    Parameters
    ----------
    ex : list[str], optional
        List of exchanges where transactions took place.
    mkt : list[str], optional
        Market where trade took place.
    price : list[float], optional
        Price of the transaction.
    seq : list[int], optional
        Trade sequence number.
    shares : list[int], optional
        Number of shares in the transaction.
    sl : list[str], optional
        Sales condition codes for the trades.
    sub_mkt : list[str], optional
        Sub-market where trade took place.
    ts : list[int], optional
        Timestamp of each transaction in milliseconds since epoch.
    """

    ex: list[str] | None = Field(
        default=None,
        description="List of exchanges where transactions took place.",
    )
    mkt: list[str] | None = Field(
        default=None,
        description="Market where trade took place.",
    )
    price: list[float] | None = Field(
        default=None,
        description="Price of the transaction.",
    )
    seq: list[int] | None = Field(default=None, description="Trade sequence number.")
    shares: list[int] | None = Field(
        default=None,
        description="Number of shares in the transaction.",
    )
    sl: list[str] | None = Field(
        default=None,
        description="Sales condition codes for the trades.",
    )
    sub_mkt: list[str] | None = Field(
        default=None,
        description="Sub-market where trade took place.",
    )
    ts: list[int] | None = Field(
        default=None,
        description="Timestamp of each transaction in milliseconds since epoch.",
    )


class TicksFetcher(Fetcher[TicksQueryParams, list[TicksData]]):
    """Get historical stock tick data for US equities using UNIX time for filtering. Limited to US exchanges."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> TicksQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        TicksQueryParams
            Validated query parameters.
        """
        return TicksQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: TicksQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/ticks and split rows from metadata.

        Parameters
        ----------
        query : TicksQueryParams
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
        _path = "/ticks"

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
        query: TicksQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[TicksData] | AnnotatedResult[list[TicksData]]:
        """Type the unpacked rows as TicksData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : TicksQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[TicksData] | AnnotatedResult[list[TicksData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [TicksData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "ex": {"description": "List of exchanges where transactions took place."},
            "mkt": {"description": "Market where trade took place."},
            "price": {"description": "Price of the transaction."},
            "seq": {"description": "Trade sequence number."},
            "shares": {"description": "Number of shares in the transaction."},
            "sl": {"description": "Sales condition codes for the trades."},
            "sub_mkt": {"description": "Sub-market where trade took place."},
            "ts": {"description": "Timestamp of each transaction in milliseconds since epoch."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
