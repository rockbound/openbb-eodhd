"""Fetcher for symbol-change-history — generated from spec.

Hits ``https://eodhd.com/api/symbol-change-history`` via HTTP GET.
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


class SymbolChangeHistoryQueryParams(QueryParams):
    """Query parameters for symbol-change-history.

    Parameters
    ----------
    from_ : str
        Start date for symbol change history in 'YYYY-MM-DD' format.
    to : str
        End date for symbol change history in 'YYYY-MM-DD' format.
    ex : str, optional
        Exchange code filter (e.g., 'US').
    fmt : Literal['json', 'csv'], optional
        Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv. (default: 'json')
    """

    from_: str = Field(
        alias="from",
        description="Start date for symbol change history in 'YYYY-MM-DD' format.",
    )
    to: str = Field(
        description="End date for symbol change history in 'YYYY-MM-DD' format.",
    )
    ex: str | None = Field(
        default=None,
        description="Exchange code filter (e.g., 'US').",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv.",
    )


class SymbolChangeHistoryData(Data):
    """Response row for symbol-change-history.

    Parameters
    ----------
    exchange : str, optional
    old_symbol : str, optional
    new_symbol : str, optional
    company_name : str, optional
    effective : datetime.date, optional
    """

    exchange: str | None = Field(default=None, description="")
    old_symbol: str | None = Field(default=None, description="")
    new_symbol: str | None = Field(default=None, description="")
    company_name: str | None = Field(default=None, description="")
    effective: datetime.date | None = Field(default=None, description="")


class SymbolChangeHistoryFetcher(
    Fetcher[SymbolChangeHistoryQueryParams, list[SymbolChangeHistoryData]]
):
    """Retrieve the symbol change history within a specified date range. Only US exchanges are currently supported."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SymbolChangeHistoryQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SymbolChangeHistoryQueryParams
            Validated query parameters.
        """
        return SymbolChangeHistoryQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SymbolChangeHistoryQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/symbol-change-history and split rows from metadata.

        Parameters
        ----------
        query : SymbolChangeHistoryQueryParams
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
        _path = "/symbol-change-history"

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
        query: SymbolChangeHistoryQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SymbolChangeHistoryData] | AnnotatedResult[list[SymbolChangeHistoryData]]:
        """Type the unpacked rows as SymbolChangeHistoryData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SymbolChangeHistoryQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SymbolChangeHistoryData] | AnnotatedResult[list[SymbolChangeHistoryData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SymbolChangeHistoryData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"effective": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
