"""Fetcher for exchange-symbol-list — generated from spec.

Hits ``https://eodhd.com/api/exchange-symbol-list/{exchangeCode}`` via HTTP GET.
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


class ExchangeSymbolListQueryParams(QueryParams):
    """Query parameters for exchange-symbol-list.

    Parameters
    ----------
    exchangeCode : str
        Exchange code, e.g., 'PSE' for the Philippines Stock Exchange or 'US' for combined US exchanges.
    fmt : Literal['json', 'csv'], optional
        Response format. Options: 'json' (default) or 'csv'. Choices: json, csv. (default: 'json')
    delisted : Literal[0, 1], optional
        Include delisted (inactive) tickers. Set to '1' to include. Choices: 0, 1. (default: 0)
    type : Literal['common_stock', 'preferred_stock', 'stock', 'etf', 'fund'], optional
        Filter by ticker type. Options: 'common_stock', 'preferred_stock', 'stock', 'etf', 'fund'. Choices: common_stock, preferred_stock, stock, etf, fund.
    """

    exchangeCode: str = Field(
        description="Exchange code, e.g., 'PSE' for the Philippines Stock Exchange or 'US' for combined US exchanges.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format. Options: 'json' (default) or 'csv'. Choices: json, csv.",
    )
    delisted: Literal[0, 1] | None = Field(
        default=0,
        description="Include delisted (inactive) tickers. Set to '1' to include. Choices: 0, 1.",
    )
    type: Literal["common_stock", "preferred_stock", "stock", "etf", "fund"] | None = Field(
        default=None,
        description="Filter by ticker type. Options: 'common_stock', 'preferred_stock', 'stock', 'etf', 'fund'. Choices: common_stock, preferred_stock, stock, etf, fund.",
    )


class ExchangeSymbolListData(Data):
    """Response row for exchange-symbol-list.

    Parameters
    ----------
    Code : str, optional
        Ticker symbol code.
    Name : str, optional
        Company name associated with the ticker.
    Country : str, optional
        Country of the exchange.
    Exchange : str, optional
        Exchange code.
    Currency : str, optional
        Currency code in which the stock is traded.
    Type : str, optional
        Type of ticker (e.g., Common Stock, ETF).
    Isin : str, optional
        ISIN code if available.
    """

    Code: str | None = Field(default=None, description="Ticker symbol code.")
    Name: str | None = Field(
        default=None,
        description="Company name associated with the ticker.",
    )
    Country: str | None = Field(default=None, description="Country of the exchange.")
    Exchange: str | None = Field(default=None, description="Exchange code.")
    Currency: str | None = Field(
        default=None,
        description="Currency code in which the stock is traded.",
    )
    Type: str | None = Field(
        default=None,
        description="Type of ticker (e.g., Common Stock, ETF).",
    )
    Isin: str | None = Field(default=None, description="ISIN code if available.")


class ExchangeSymbolListFetcher(
    Fetcher[ExchangeSymbolListQueryParams, list[ExchangeSymbolListData]]
):
    """Returns a list of active or delisted symbols for the specified exchange, with optional filters by ticker type."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> ExchangeSymbolListQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        ExchangeSymbolListQueryParams
            Validated query parameters.
        """
        return ExchangeSymbolListQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: ExchangeSymbolListQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/exchange-symbol-list/{exchangeCode} and split rows from metadata.

        Parameters
        ----------
        query : ExchangeSymbolListQueryParams
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
        _path = f"/exchange-symbol-list/{query.exchangeCode}"

        _query_dict = query.model_dump(by_alias=True, exclude={"exchangeCode"}, exclude_none=True)
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
        query: ExchangeSymbolListQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[ExchangeSymbolListData] | AnnotatedResult[list[ExchangeSymbolListData]]:
        """Type the unpacked rows as ExchangeSymbolListData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : ExchangeSymbolListQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[ExchangeSymbolListData] | AnnotatedResult[list[ExchangeSymbolListData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [ExchangeSymbolListData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "Code": {"description": "Ticker symbol code."},
            "Name": {"description": "Company name associated with the ticker."},
            "Country": {"description": "Country of the exchange."},
            "Exchange": {"description": "Exchange code."},
            "Currency": {"description": "Currency code in which the stock is traded."},
            "Type": {"description": "Type of ticker (e.g., Common Stock, ETF)."},
            "Isin": {"description": "ISIN code if available."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
