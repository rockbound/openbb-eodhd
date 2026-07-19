"""Fetcher for v1_1.bulk-fundamentals — generated from spec.

Hits ``https://eodhd.com/api/v1.1/bulk-fundamentals/{EXCHANGE}`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field, field_validator

from ....utils import safe_json_loads, unpack_response


class V11BulkFundamentalsQueryParams(QueryParams):
    """Query parameters for v1_1.bulk-fundamentals.

    Parameters
    ----------
    EXCHANGE : str
        Exchange code (e.g., 'US', 'LSE', 'TO').
    symbols : str, optional
        Comma-separated list of symbols to filter (e.g., 'AAPL,MSFT,GOOGL').
    offset : int, optional
        Offset for pagination (number of records to skip). (default: 0)
    limit : int, optional
        Maximum number of records to return (max 500). (default: 500)
    version : int, optional
        API version for response format.
    fmt : Literal['json'], optional
        Output format. In v1.1, only json format is supported. Choices: json. (default: 'json')
    """

    EXCHANGE: str = Field(description="Exchange code (e.g., 'US', 'LSE', 'TO').")
    symbols: str | None = Field(
        default=None,
        description="Comma-separated list of symbols to filter (e.g., 'AAPL,MSFT,GOOGL').",
    )
    offset: int | None = Field(
        default=0,
        description="Offset for pagination (number of records to skip).",
    )
    limit: int | None = Field(
        default=500,
        description="Maximum number of records to return (max 500).",
    )
    version: int | None = Field(
        default=None,
        description="API version for response format.",
    )
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. In v1.1, only json format is supported. Choices: json.",
    )


class V11BulkFundamentalsDataGeneral(BaseModel):
    """V11BulkFundamentalsDataGeneral.

    Parameters
    ----------
    Code : str, optional
    Name : str, optional
    Exchange : str, optional
    Sector : str, optional
    Industry : str, optional
    """

    Code: str | None = Field(default=None, description="")
    Name: str | None = Field(default=None, description="")
    Exchange: str | None = Field(default=None, description="")
    Sector: str | None = Field(default=None, description="")
    Industry: str | None = Field(default=None, description="")


class V11BulkFundamentalsDataHighlights(BaseModel):
    """V11BulkFundamentalsDataHighlights.

    Parameters
    ----------
    MarketCapitalization : float, optional
    EBITDA : float, optional
    PERatio : float, optional
    """

    MarketCapitalization: float | None = Field(default=None, description="")
    EBITDA: float | None = Field(default=None, description="")
    PERatio: float | None = Field(default=None, description="")


class V11BulkFundamentalsDataValuation(BaseModel):
    """V11BulkFundamentalsDataValuation.

    Parameters
    ----------
    TrailingPE : float, optional
    ForwardPE : float, optional
    """

    TrailingPE: float | None = Field(default=None, description="")
    ForwardPE: float | None = Field(default=None, description="")


class V11BulkFundamentalsData(Data):
    """Response row for v1_1.bulk-fundamentals.

    Parameters
    ----------
    General : V11BulkFundamentalsDataGeneral, optional
        Inner fields: Code (str), Name (str), Exchange (str), Sector (str), Industry (str).
    Highlights : V11BulkFundamentalsDataHighlights, optional
        Inner fields: MarketCapitalization (float), EBITDA (float), PERatio (float).
    Valuation : V11BulkFundamentalsDataValuation, optional
        Inner fields: TrailingPE (float), ForwardPE (float).
    """

    General: V11BulkFundamentalsDataGeneral | None = Field(
        default=None,
        description="Inner fields: Code (str), Name (str), Exchange (str), Sector (str), Industry (str).",
    )
    Highlights: V11BulkFundamentalsDataHighlights | None = Field(
        default=None,
        description="Inner fields: MarketCapitalization (float), EBITDA (float), PERatio (float).",
    )
    Valuation: V11BulkFundamentalsDataValuation | None = Field(
        default=None,
        description="Inner fields: TrailingPE (float), ForwardPE (float).",
    )

    @field_validator("General", "Highlights", "Valuation", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class V11BulkFundamentalsFetcher(
    Fetcher[V11BulkFundamentalsQueryParams, list[V11BulkFundamentalsData]]
):
    """Fetches fundamental data in bulk for all symbols on a given exchange using API v1.1. Supports filtering by specific symbols and data sections (General, Highlights, Valuation, etc.). In v1.1, the fmt parameter only supports json format."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> V11BulkFundamentalsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        V11BulkFundamentalsQueryParams
            Validated query parameters.
        """
        return V11BulkFundamentalsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: V11BulkFundamentalsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/v1.1/bulk-fundamentals/{EXCHANGE} and split rows from metadata.

        Parameters
        ----------
        query : V11BulkFundamentalsQueryParams
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
        _path = f"/v1.1/bulk-fundamentals/{query.EXCHANGE}"

        _query_dict = query.model_dump(by_alias=True, exclude={"EXCHANGE"}, exclude_none=True)
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
        query: V11BulkFundamentalsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[V11BulkFundamentalsData] | AnnotatedResult[list[V11BulkFundamentalsData]]:
        """Type the unpacked rows as V11BulkFundamentalsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : V11BulkFundamentalsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[V11BulkFundamentalsData] | AnnotatedResult[list[V11BulkFundamentalsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [V11BulkFundamentalsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
