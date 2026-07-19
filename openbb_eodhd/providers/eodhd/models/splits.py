"""Fetcher for splits — generated from spec.

Hits ``https://eodhd.com/api/splits/{ticker}`` via HTTP GET.
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


class SplitsQueryParams(QueryParams):
    """Query parameters for splits.

    Parameters
    ----------
    ticker : str
        Ticker symbol of the stock in the format {SYMBOL_NAME}.{EXCHANGE_ID} (e.g., 'AAPL.US' for NASDAQ or 'AAPL.MX' for the Mexican Stock Exchange).
    from_ : str, optional
        Start date for data retrieval in 'YYYY-MM-DD' format. Defaults to earliest available data if not provided.
    to : str, optional
        End date for data retrieval in 'YYYY-MM-DD' format. Defaults to latest available data if not provided.
    fmt : Literal['json', 'csv'], optional
        Output format, either 'json' or 'csv'. Defaults to 'json'. Choices: json, csv. (default: 'json')
    """

    ticker: str = Field(
        description="Ticker symbol of the stock in the format {SYMBOL_NAME}.{EXCHANGE_ID} (e.g., 'AAPL.US' for NASDAQ or 'AAPL.MX' for the Mexican Stock Exchange).",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for data retrieval in 'YYYY-MM-DD' format. Defaults to earliest available data if not provided.",
    )
    to: str | None = Field(
        default=None,
        description="End date for data retrieval in 'YYYY-MM-DD' format. Defaults to latest available data if not provided.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format, either 'json' or 'csv'. Defaults to 'json'. Choices: json, csv.",
    )


class SplitsData(Data):
    """Response row for splits.

    Parameters
    ----------
    date : datetime.date
        Date of the stock split.
    split : str
        Split ratio represented as '{new shares}/{old shares}' (e.g., '2.000000/1.000000').
    """

    date: datetime.date = Field(description="Date of the stock split.")
    split: str = Field(
        description="Split ratio represented as '{new shares}/{old shares}' (e.g., '2.000000/1.000000').",
    )


class SplitsFetcher(Fetcher[SplitsQueryParams, list[SplitsData]]):
    """Fetches historical stock split data for a specified ticker, including split dates and ratios."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SplitsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SplitsQueryParams
            Validated query parameters.
        """
        return SplitsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SplitsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/splits/{ticker} and split rows from metadata.

        Parameters
        ----------
        query : SplitsQueryParams
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
        _path = f"/splits/{query.ticker}"

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
        query: SplitsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SplitsData] | AnnotatedResult[list[SplitsData]]:
        """Type the unpacked rows as SplitsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SplitsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SplitsData] | AnnotatedResult[list[SplitsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SplitsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Date of the stock split.", "format": "date"},
            "split": {
                "description": "Split ratio represented as '{new shares}/{old shares}' (e.g., '2.000000/1.000000')."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
