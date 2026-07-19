"""Fetcher for id-mapping — generated from spec.

Hits ``https://eodhd.com/api/id-mapping`` via HTTP GET.
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


class IdMappingQueryParams(QueryParams):
    """Query parameters for id-mapping.

    Parameters
    ----------
    filter_symbol_ : str, optional
        Filter by ticker symbol (e.g., 'AAPL').
    filter_ex_ : str, optional
        Filter by exchange code (e.g., 'US').
    filter_isin_ : str, optional
        Filter by ISIN code (e.g., 'US0378331005').
    filter_figi_ : str, optional
        Filter by FIGI identifier.
    filter_lei_ : str, optional
        Filter by LEI code.
    filter_cusip_ : str, optional
        Filter by CUSIP identifier.
    filter_cik_ : str, optional
        Filter by CIK number.
    page_limit_ : int, optional
        Number of records per page.
    page_offset_ : int, optional
        Pagination offset.
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    filter_symbol_: str | None = Field(
        default=None,
        alias="filter[symbol]",
        description="Filter by ticker symbol (e.g., 'AAPL').",
    )
    filter_ex_: str | None = Field(
        default=None,
        alias="filter[ex]",
        description="Filter by exchange code (e.g., 'US').",
    )
    filter_isin_: str | None = Field(
        default=None,
        alias="filter[isin]",
        description="Filter by ISIN code (e.g., 'US0378331005').",
    )
    filter_figi_: str | None = Field(
        default=None,
        alias="filter[figi]",
        description="Filter by FIGI identifier.",
    )
    filter_lei_: str | None = Field(
        default=None,
        alias="filter[lei]",
        description="Filter by LEI code.",
    )
    filter_cusip_: str | None = Field(
        default=None,
        alias="filter[cusip]",
        description="Filter by CUSIP identifier.",
    )
    filter_cik_: str | None = Field(
        default=None,
        alias="filter[cik]",
        description="Filter by CIK number.",
    )
    page_limit_: int | None = Field(
        default=None,
        alias="page[limit]",
        description="Number of records per page.",
    )
    page_offset_: int | None = Field(
        default=None,
        alias="page[offset]",
        description="Pagination offset.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class IdMappingData(Data):
    """Response row for id-mapping.

    Parameters
    ----------
    Code : str, optional
        Ticker symbol.
    Exchange : str, optional
        Exchange code.
    Name : str, optional
        Company name.
    ISIN : str, optional
        ISIN code.
    FIGI : str, optional
        FIGI identifier.
    LEI : str, optional
        LEI code.
    CUSIP : str, optional
        CUSIP identifier.
    CIK : str, optional
        CIK number.
    """

    Code: str | None = Field(default=None, description="Ticker symbol.")
    Exchange: str | None = Field(default=None, description="Exchange code.")
    Name: str | None = Field(default=None, description="Company name.")
    ISIN: str | None = Field(default=None, description="ISIN code.")
    FIGI: str | None = Field(default=None, description="FIGI identifier.")
    LEI: str | None = Field(default=None, description="LEI code.")
    CUSIP: str | None = Field(default=None, description="CUSIP identifier.")
    CIK: str | None = Field(default=None, description="CIK number.")


class IdMappingFetcher(Fetcher[IdMappingQueryParams, list[IdMappingData]]):
    """Look up securities by various identifiers including symbol, exchange code, ISIN, FIGI, LEI, CUSIP, and CIK."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> IdMappingQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        IdMappingQueryParams
            Validated query parameters.
        """
        return IdMappingQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: IdMappingQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/id-mapping and split rows from metadata.

        Parameters
        ----------
        query : IdMappingQueryParams
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
        _path = "/id-mapping"

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
        query: IdMappingQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[IdMappingData] | AnnotatedResult[list[IdMappingData]]:
        """Type the unpacked rows as IdMappingData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : IdMappingQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[IdMappingData] | AnnotatedResult[list[IdMappingData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [IdMappingData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "Code": {"description": "Ticker symbol."},
            "Exchange": {"description": "Exchange code."},
            "Name": {"description": "Company name."},
            "ISIN": {"description": "ISIN code."},
            "FIGI": {"description": "FIGI identifier."},
            "LEI": {"description": "LEI code."},
            "CUSIP": {"description": "CUSIP identifier."},
            "CIK": {"description": "CIK number."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
