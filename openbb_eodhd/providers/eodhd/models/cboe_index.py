"""Fetcher for cboe.index — generated from spec.

Hits ``https://eodhd.com/api/cboe/index`` via HTTP GET.
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


class CboeIndexQueryParams(QueryParams):
    """Query parameters for cboe.index.

    Parameters
    ----------
    filter_index_code_ : str
        CBOE index code (e.g., 'VIX', 'SPX').
    filter_feed_type_ : str
        Feed type filter.
    filter_date_ : str
        Date filter in 'YYYY-MM-DD' format.
    filter_include_review_ : str, optional
        Include review data.
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    filter_index_code_: str = Field(
        alias="filter[index_code]",
        description="CBOE index code (e.g., 'VIX', 'SPX').",
    )
    filter_feed_type_: str = Field(
        alias="filter[feed_type]",
        description="Feed type filter.",
    )
    filter_date_: str = Field(
        alias="filter[date]",
        description="Date filter in 'YYYY-MM-DD' format.",
    )
    filter_include_review_: str | None = Field(
        default=None,
        alias="filter[include_review]",
        description="Include review data.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class CboeIndexData(Data):
    """Response row for cboe.index.

    Parameters
    ----------
    date : datetime.date, optional
        Trading date.
    open : float, optional
        Opening value.
    high : float, optional
        High value.
    low : float, optional
        Low value.
    close : float, optional
        Closing value.
    volume : float, optional
        Trading volume (if applicable).
    """

    date: datetime.date | None = Field(default=None, description="Trading date.")
    open: float | None = Field(default=None, description="Opening value.")
    high: float | None = Field(default=None, description="High value.")
    low: float | None = Field(default=None, description="Low value.")
    close: float | None = Field(default=None, description="Closing value.")
    volume: float | None = Field(
        default=None,
        description="Trading volume (if applicable).",
    )


class CboeIndexFetcher(Fetcher[CboeIndexQueryParams, list[CboeIndexData]]):
    """Returns historical end-of-day data for a specific CBOE index, including daily open, high, low, close values."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CboeIndexQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CboeIndexQueryParams
            Validated query parameters.
        """
        return CboeIndexQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CboeIndexQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/cboe/index and split rows from metadata.

        Parameters
        ----------
        query : CboeIndexQueryParams
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
        _path = "/cboe/index"

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
        query: CboeIndexQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CboeIndexData] | AnnotatedResult[list[CboeIndexData]]:
        """Type the unpacked rows as CboeIndexData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CboeIndexQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CboeIndexData] | AnnotatedResult[list[CboeIndexData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CboeIndexData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Trading date.", "format": "date"},
            "open": {"description": "Opening value."},
            "high": {"description": "High value."},
            "low": {"description": "Low value."},
            "close": {"description": "Closing value."},
            "volume": {"description": "Trading volume (if applicable)."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
