"""Fetcher for mp.unicornbay.spglobal.comp — generated from spec.

Hits ``https://eodhd.com/api/mp/unicornbay/spglobal/comp/{symbol}`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field

from ....utils import safe_json_loads, unpack_response


class MpUnicornbaySpglobalCompQueryParams(QueryParams):
    """Query parameters for mp.unicornbay.spglobal.comp.

    Parameters
    ----------
    symbol : str
        Index symbol, e.g., GSPC.INDX.
    fmt : Literal['json', 'xml'], optional
        Response format. Choices: json, xml. (default: 'json')
    """

    symbol: str = Field(description="Index symbol, e.g., GSPC.INDX.")
    fmt: Literal["json", "xml"] | None = Field(
        default="json",
        description="Response format. Choices: json, xml.",
    )


class MpUnicornbaySpglobalCompDataGeneral(BaseModel):
    """MpUnicornbaySpglobalCompDataGeneral.

    Parameters
    ----------
    Code : str
    Type : str
    Name : str
    Exchange : str
    MarketCap : float, optional
    CurrencyCode : str, optional
    CurrencyName : str, optional
    CurrencySymbol : str, optional
    CountryName : str, optional
    CountryISO : str, optional
    OpenFigi : str, optional
    """

    Code: str = Field(description="")
    Type: str = Field(description="")
    Name: str = Field(description="")
    Exchange: str = Field(description="")
    MarketCap: float | None = Field(default=None, description="")
    CurrencyCode: str | None = Field(default=None, description="")
    CurrencyName: str | None = Field(default=None, description="")
    CurrencySymbol: str | None = Field(default=None, description="")
    CountryName: str | None = Field(default=None, description="")
    CountryISO: str | None = Field(default=None, description="")
    OpenFigi: str | None = Field(default=None, description="")


class MpUnicornbaySpglobalCompDataComponentsValue(BaseModel):
    """MpUnicornbaySpglobalCompDataComponentsValue.

    Parameters
    ----------
    Code : str
    Exchange : str
    Name : str
    Sector : str, optional
    Industry : str, optional
    Weight : float, optional
    """

    Code: str = Field(description="")
    Exchange: str = Field(description="")
    Name: str = Field(description="")
    Sector: str | None = Field(default=None, description="")
    Industry: str | None = Field(default=None, description="")
    Weight: float | None = Field(default=None, description="")


class MpUnicornbaySpglobalCompDataHistoricalTickerComponentsValue(BaseModel):
    """MpUnicornbaySpglobalCompDataHistoricalTickerComponentsValue.

    Parameters
    ----------
    Code : str
    Name : str
    StartDate : str
        YYYY-MM-DD.
    EndDate : str, optional
        YYYY-MM-DD or null.
    IsActiveNow : Literal[0, 1]
        Choices: 0, 1.
    IsDelisted : Literal[0, 1]
        Choices: 0, 1.
    """

    Code: str = Field(description="")
    Name: str = Field(description="")
    StartDate: str = Field(description="YYYY-MM-DD.")
    EndDate: str | None = Field(default=None, description="YYYY-MM-DD or null.")
    IsActiveNow: Literal[0, 1] = Field(description="Choices: 0, 1.")
    IsDelisted: Literal[0, 1] = Field(description="Choices: 0, 1.")


class MpUnicornbaySpglobalCompData(Data):
    """Response row for mp.unicornbay.spglobal.comp.

    Parameters
    ----------
    General : MpUnicornbaySpglobalCompDataGeneral
        Inner fields: Code (str), Type (str), Name (str), Exchange (str), MarketCap (Any), CurrencyCode (Any), CurrencyName (Any), CurrencySymbol (Any), CountryName (Any), CountryISO (Any), OpenFigi (Any).
    Components : dict[str, MpUnicornbaySpglobalCompDataComponentsValue]
    HistoricalTickerComponents : dict[str, MpUnicornbaySpglobalCompDataHistoricalTickerComponentsValue]
    """

    General: MpUnicornbaySpglobalCompDataGeneral = Field(
        description="Inner fields: Code (str), Type (str), Name (str), Exchange (str), MarketCap (Any), CurrencyCode (Any), CurrencyName (Any), CurrencySymbol (Any), CountryName (Any), CountryISO (Any), OpenFigi (Any).",
    )
    Components: dict[str, MpUnicornbaySpglobalCompDataComponentsValue] = Field(
        description="",
    )
    HistoricalTickerComponents: dict[
        str, MpUnicornbaySpglobalCompDataHistoricalTickerComponentsValue
    ] = Field(
        description="",
    )


class MpUnicornbaySpglobalCompFetcher(
    Fetcher[MpUnicornbaySpglobalCompQueryParams, list[MpUnicornbaySpglobalCompData]]
):
    """Returns the current components and historical changes for an index symbol."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpUnicornbaySpglobalCompQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpUnicornbaySpglobalCompQueryParams
            Validated query parameters.
        """
        return MpUnicornbaySpglobalCompQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpUnicornbaySpglobalCompQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/unicornbay/spglobal/comp/{symbol} and split rows from metadata.

        Parameters
        ----------
        query : MpUnicornbaySpglobalCompQueryParams
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
        _path = f"/mp/unicornbay/spglobal/comp/{query.symbol}"

        _query_dict = query.model_dump(by_alias=True, exclude={"symbol"}, exclude_none=True)
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
        query: MpUnicornbaySpglobalCompQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpUnicornbaySpglobalCompData] | AnnotatedResult[list[MpUnicornbaySpglobalCompData]]:
        """Type the unpacked rows as MpUnicornbaySpglobalCompData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpUnicornbaySpglobalCompQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpUnicornbaySpglobalCompData] | AnnotatedResult[list[MpUnicornbaySpglobalCompData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpUnicornbaySpglobalCompData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
