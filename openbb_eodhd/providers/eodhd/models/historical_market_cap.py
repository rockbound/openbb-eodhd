"""Fetcher for historical-market-cap — generated from spec.

Hits ``https://eodhd.com/api/historical-market-cap/{ticker}`` via HTTP GET.
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


class HistoricalMarketCapQueryParams(QueryParams):
    """Query parameters for historical-market-cap.

    Parameters
    ----------
    ticker : str
        The ticker symbol of the stock, e.g., 'AAPL.US' or simply 'AAPL'.
    from_ : str, optional
        Start date for data retrieval in 'YYYY-MM-DD' format.
    to : str, optional
        End date for data retrieval in 'YYYY-MM-DD' format.
    reverse : Literal['true', 'false'], optional
        Set to 'true' to reverse sort order (newest first). Choices: true, false.
    fmt : Literal['json', 'csv'], optional
        Output format, either 'json' or 'csv'. Defaults to 'json'. Choices: json, csv. (default: 'json')
    """

    ticker: str = Field(
        description="The ticker symbol of the stock, e.g., 'AAPL.US' or simply 'AAPL'.",
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
    reverse: Literal["true", "false"] | None = Field(
        default=None,
        description="Set to 'true' to reverse sort order (newest first). Choices: true, false.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format, either 'json' or 'csv'. Defaults to 'json'. Choices: json, csv.",
    )


class HistoricalMarketCapData(Data):
    """Response row for historical-market-cap."""

    pass


class HistoricalMarketCapFetcher(
    Fetcher[HistoricalMarketCapQueryParams, list[HistoricalMarketCapData]]
):
    """Fetches historical market capitalization for a specified stock symbol with weekly frequency."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> HistoricalMarketCapQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        HistoricalMarketCapQueryParams
            Validated query parameters.
        """
        return HistoricalMarketCapQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: HistoricalMarketCapQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/historical-market-cap/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : HistoricalMarketCapQueryParams
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
        _path = f"/historical-market-cap/{query.ticker}"

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
        query: HistoricalMarketCapQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[HistoricalMarketCapData] | AnnotatedResult[list[HistoricalMarketCapData]]:
        """Type the unpacked rows as HistoricalMarketCapData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : HistoricalMarketCapQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[HistoricalMarketCapData] | AnnotatedResult[list[HistoricalMarketCapData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [HistoricalMarketCapData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
