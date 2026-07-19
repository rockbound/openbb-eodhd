"""Fetcher for mp.unicornbay.spglobal.list — generated from spec.

Hits ``https://eodhd.com/api/mp/unicornbay/spglobal/list`` via HTTP GET.
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


class MpUnicornbaySpglobalListQueryParams(QueryParams):
    """Query parameters for mp.unicornbay.spglobal.list.

    Parameters
    ----------
    fmt : Literal['json', 'xml'], optional
        Response format. Choices: json, xml. (default: 'json')
    """

    fmt: Literal["json", "xml"] | None = Field(
        default="json",
        description="Response format. Choices: json, xml.",
    )


class MpUnicornbaySpglobalListData(Data):
    """Response row for mp.unicornbay.spglobal.list.

    Parameters
    ----------
    ID : str
    Code : str
    Name : str
    Constituents : int
    LastUpdate : str
        YYYY-MM-DD.
    Value : float, optional
    MarketCap : float, optional
    Divisor : float, optional
    DailyReturn : float | str, optional
    Dividend : float, optional
    AdjustedMarketCap : float, optional
    AdjustedDivisor : float, optional
    AdjustedConstituents : int, optional
    CurrencyCode : str, optional
    CurrencyName : str, optional
    CurrencySymbol : str, optional
    """

    ID: str = Field(description="")
    Code: str = Field(description="")
    Name: str = Field(description="")
    Constituents: int = Field(description="")
    LastUpdate: str = Field(description="YYYY-MM-DD.")
    Value: float | None = Field(default=None, description="")
    MarketCap: float | None = Field(default=None, description="")
    Divisor: float | None = Field(default=None, description="")
    DailyReturn: float | str | None = Field(default=None, description="")
    Dividend: float | None = Field(default=None, description="")
    AdjustedMarketCap: float | None = Field(default=None, description="")
    AdjustedDivisor: float | None = Field(default=None, description="")
    AdjustedConstituents: int | None = Field(default=None, description="")
    CurrencyCode: str | None = Field(default=None, description="")
    CurrencyName: str | None = Field(default=None, description="")
    CurrencySymbol: str | None = Field(default=None, description="")


class MpUnicornbaySpglobalListFetcher(
    Fetcher[MpUnicornbaySpglobalListQueryParams, list[MpUnicornbaySpglobalListData]]
):
    """Returns essential EOD details for 100+ S&P & Dow Jones indices."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpUnicornbaySpglobalListQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpUnicornbaySpglobalListQueryParams
            Validated query parameters.
        """
        return MpUnicornbaySpglobalListQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpUnicornbaySpglobalListQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/unicornbay/spglobal/list and split rows from metadata.

        Parameters
        ----------
        query : MpUnicornbaySpglobalListQueryParams
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
        _path = "/mp/unicornbay/spglobal/list"

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
        query: MpUnicornbaySpglobalListQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpUnicornbaySpglobalListData] | AnnotatedResult[list[MpUnicornbaySpglobalListData]]:
        """Type the unpacked rows as MpUnicornbaySpglobalListData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpUnicornbaySpglobalListQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpUnicornbaySpglobalListData] | AnnotatedResult[list[MpUnicornbaySpglobalListData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpUnicornbaySpglobalListData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"LastUpdate": {"description": "YYYY-MM-DD"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
