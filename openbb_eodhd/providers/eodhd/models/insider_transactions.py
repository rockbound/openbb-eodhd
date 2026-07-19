"""Fetcher for insider-transactions — generated from spec.

Hits ``https://eodhd.com/api/insider-transactions`` via HTTP GET.
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


class InsiderTransactionsQueryParams(QueryParams):
    """Query parameters for insider-transactions.

    Parameters
    ----------
    limit : int, optional
        Max number of entries per result, from 1 to 1000. Default is 100. (default: 100)
    from_ : str, optional
        Start date for transactions (format: YYYY-MM-DD). Defaults to one year before current date.
    to : str, optional
        End date for transactions (format: YYYY-MM-DD). Defaults to current date.
    code : str, optional
        Ticker symbol for filtering results (e.g., 'AAPL.US'). If omitted, returns data for all symbols.
    fmt : Literal['json'], optional
        Output format (only 'json' supported). Choices: json. (default: 'json')
    """

    limit: int | None = Field(
        default=100,
        description="Max number of entries per result, from 1 to 1000. Default is 100.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for transactions (format: YYYY-MM-DD). Defaults to one year before current date.",
    )
    to: str | None = Field(
        default=None,
        description="End date for transactions (format: YYYY-MM-DD). Defaults to current date.",
    )
    code: str | None = Field(
        default=None,
        description="Ticker symbol for filtering results (e.g., 'AAPL.US'). If omitted, returns data for all symbols.",
    )
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format (only 'json' supported). Choices: json.",
    )


class InsiderTransactionsData(Data):
    """Response row for insider-transactions.

    Parameters
    ----------
    code : str, optional
        Ticker symbol of the company.
    exchange : str, optional
        Exchange where the stock is listed.
    date : datetime.date, optional
        Report date of the transaction.
    reportDate : datetime.date, optional
        Date the transaction was reported to the SEC.
    ownerCik : str, optional
        Unique identifier for the owner in SEC filings.
    ownerName : str, optional
        Name of the insider who executed the transaction.
    ownerRelationship : str, optional
        Relationship of the owner to the company (e.g., Director).
    ownerTitle : str, optional
        Title or role of the insider in the company.
    transactionDate : datetime.date, optional
        Date when the transaction occurred.
    transactionCode : Literal['P', 'S'], optional
        Type of transaction: 'P' for Purchase, 'S' for Sale. Choices: P, S.
    transactionAmount : int, optional
        Number of shares involved in the transaction.
    transactionPrice : float, optional
        Price per share at the time of the transaction.
    transactionAcquiredDisposed : Literal['A', 'D'], optional
        Indicates whether securities were Acquired (A) or Disposed (D). Choices: A, D.
    postTransactionAmount : int, optional
        Total number of shares held by the insider post-transaction.
    link : str, optional
        Link to the original SEC filing document.
    """

    code: str | None = Field(default=None, description="Ticker symbol of the company.")
    exchange: str | None = Field(
        default=None,
        description="Exchange where the stock is listed.",
    )
    date: datetime.date | None = Field(
        default=None,
        description="Report date of the transaction.",
    )
    reportDate: datetime.date | None = Field(
        default=None,
        description="Date the transaction was reported to the SEC.",
    )
    ownerCik: str | None = Field(
        default=None,
        description="Unique identifier for the owner in SEC filings.",
    )
    ownerName: str | None = Field(
        default=None,
        description="Name of the insider who executed the transaction.",
    )
    ownerRelationship: str | None = Field(
        default=None,
        description="Relationship of the owner to the company (e.g., Director).",
    )
    ownerTitle: str | None = Field(
        default=None,
        description="Title or role of the insider in the company.",
    )
    transactionDate: datetime.date | None = Field(
        default=None,
        description="Date when the transaction occurred.",
    )
    transactionCode: Literal["P", "S"] | None = Field(
        default=None,
        description="Type of transaction: 'P' for Purchase, 'S' for Sale. Choices: P, S.",
    )
    transactionAmount: int | None = Field(
        default=None,
        description="Number of shares involved in the transaction.",
    )
    transactionPrice: float | None = Field(
        default=None,
        description="Price per share at the time of the transaction.",
    )
    transactionAcquiredDisposed: Literal["A", "D"] | None = Field(
        default=None,
        description="Indicates whether securities were Acquired (A) or Disposed (D). Choices: A, D.",
    )
    postTransactionAmount: int | None = Field(
        default=None,
        description="Total number of shares held by the insider post-transaction.",
    )
    link: str | None = Field(
        default=None,
        description="Link to the original SEC filing document.",
    )


class InsiderTransactionsFetcher(
    Fetcher[InsiderTransactionsQueryParams, list[InsiderTransactionsData]]
):
    """Fetch insider transaction data for US-listed companies. Covers insider buys and sells, providing transaction details such as date, shares, and price."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> InsiderTransactionsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        InsiderTransactionsQueryParams
            Validated query parameters.
        """
        return InsiderTransactionsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: InsiderTransactionsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/insider-transactions and split rows from metadata.

        Parameters
        ----------
        query : InsiderTransactionsQueryParams
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
        _path = "/insider-transactions"

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
        query: InsiderTransactionsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[InsiderTransactionsData] | AnnotatedResult[list[InsiderTransactionsData]]:
        """Type the unpacked rows as InsiderTransactionsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : InsiderTransactionsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[InsiderTransactionsData] | AnnotatedResult[list[InsiderTransactionsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [InsiderTransactionsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Ticker symbol of the company"},
            "exchange": {"description": "Exchange where the stock is listed"},
            "date": {"description": "Report date of the transaction", "format": "date"},
            "reportDate": {
                "description": "Date the transaction was reported to the SEC",
                "format": "date",
            },
            "ownerCik": {"description": "Unique identifier for the owner in SEC filings"},
            "ownerName": {"description": "Name of the insider who executed the transaction"},
            "ownerRelationship": {
                "description": "Relationship of the owner to the company (e.g., Director)"
            },
            "ownerTitle": {"description": "Title or role of the insider in the company"},
            "transactionDate": {
                "description": "Date when the transaction occurred",
                "format": "date",
            },
            "transactionCode": {
                "description": "Type of transaction: 'P' for Purchase, 'S' for Sale"
            },
            "transactionAmount": {"description": "Number of shares involved in the transaction"},
            "transactionPrice": {
                "description": "Price per share at the time of the transaction",
                "format": "float",
            },
            "transactionAcquiredDisposed": {
                "description": "Indicates whether securities were Acquired (A) or Disposed (D)"
            },
            "postTransactionAmount": {
                "description": "Total number of shares held by the insider post-transaction"
            },
            "link": {"description": "Link to the original SEC filing document", "format": "uri"},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
