"""Fetcher for mp.unicornbay.options.eod — generated from spec.

Hits ``https://eodhd.com/api/mp/unicornbay/options/eod`` via HTTP GET.
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


class MpUnicornbayOptionsEodQueryParams(QueryParams):
    """Query parameters for mp.unicornbay.options.eod.

    Parameters
    ----------
    filter_contract_ : str, optional
        Exact contract name, e.g., AAPL270115P00450000.
    filter_underlying_symbol_ : str, optional
        Underlying symbol, e.g., AAPL.
    filter_exp_date_eq_ : str, optional
        Expiration equals (YYYY-MM-DD).
    filter_exp_date_from_ : str, optional
        Expiration from (YYYY-MM-DD).
    filter_exp_date_to_ : str, optional
        Expiration to (YYYY-MM-DD).
    filter_tradetime_eq_ : str, optional
        Trade time equals (YYYY-MM-DD).
    filter_tradetime_from_ : str, optional
        Trade time from (YYYY-MM-DD).
    filter_tradetime_to_ : str, optional
        Trade time to (YYYY-MM-DD).
    filter_type_ : Literal['put', 'call'], optional
        Option type. Choices: put, call.
    filter_strike_eq_ : float, optional
        Strike equals.
    filter_strike_from_ : float, optional
        Strike from.
    filter_strike_to_ : float, optional
        Strike to.
    sort : Literal['exp_date', 'strike', '-exp_date', '-strike'], optional
        Sort by expiration date or strike (asc/desc). Choices: exp_date, strike, -exp_date, -strike.
    page_offset_ : int, optional
        Pagination offset (records to skip). Max 10000. (default: 0)
    page_limit_ : int, optional
        Pagination limit. Default & max 1000. (default: 1000)
    fields_options_eod_ : str, optional
        CSV of fields to include (e.g., contract,exp_date,strike).
    compact : Literal[0, 1], optional
        Set 1 for compact mode (rows as arrays in `data`, columns = `meta.fields`). Choices: 0, 1. (default: 0)
    fmt : Literal['json', 'xml'], optional
        Response format. Choices: json, xml. (default: 'json')
    """

    filter_contract_: str | None = Field(
        default=None,
        alias="filter[contract]",
        description="Exact contract name, e.g., AAPL270115P00450000.",
    )
    filter_underlying_symbol_: str | None = Field(
        default=None,
        alias="filter[underlying_symbol]",
        description="Underlying symbol, e.g., AAPL.",
    )
    filter_exp_date_eq_: str | None = Field(
        default=None,
        alias="filter[exp_date_eq]",
        description="Expiration equals (YYYY-MM-DD).",
    )
    filter_exp_date_from_: str | None = Field(
        default=None,
        alias="filter[exp_date_from]",
        description="Expiration from (YYYY-MM-DD).",
    )
    filter_exp_date_to_: str | None = Field(
        default=None,
        alias="filter[exp_date_to]",
        description="Expiration to (YYYY-MM-DD).",
    )
    filter_tradetime_eq_: str | None = Field(
        default=None,
        alias="filter[tradetime_eq]",
        description="Trade time equals (YYYY-MM-DD).",
    )
    filter_tradetime_from_: str | None = Field(
        default=None,
        alias="filter[tradetime_from]",
        description="Trade time from (YYYY-MM-DD).",
    )
    filter_tradetime_to_: str | None = Field(
        default=None,
        alias="filter[tradetime_to]",
        description="Trade time to (YYYY-MM-DD).",
    )
    filter_type_: Literal["put", "call"] | None = Field(
        default=None,
        alias="filter[type]",
        description="Option type. Choices: put, call.",
    )
    filter_strike_eq_: float | None = Field(
        default=None,
        alias="filter[strike_eq]",
        description="Strike equals.",
    )
    filter_strike_from_: float | None = Field(
        default=None,
        alias="filter[strike_from]",
        description="Strike from.",
    )
    filter_strike_to_: float | None = Field(
        default=None,
        alias="filter[strike_to]",
        description="Strike to.",
    )
    sort: Literal["exp_date", "strike", "-exp_date", "-strike"] | None = Field(
        default=None,
        description="Sort by expiration date or strike (asc/desc). Choices: exp_date, strike, -exp_date, -strike.",
    )
    page_offset_: int | None = Field(
        default=0,
        alias="page[offset]",
        description="Pagination offset (records to skip). Max 10000.",
    )
    page_limit_: int | None = Field(
        default=1000,
        alias="page[limit]",
        description="Pagination limit. Default & max 1000.",
    )
    fields_options_eod_: str | None = Field(
        default=None,
        alias="fields[options-eod]",
        description="CSV of fields to include (e.g., contract,exp_date,strike).",
    )
    compact: Literal[0, 1] | None = Field(
        default=0,
        description="Set 1 for compact mode (rows as arrays in `data`, columns = `meta.fields`). Choices: 0, 1.",
    )
    fmt: Literal["json", "xml"] | None = Field(
        default="json",
        description="Response format. Choices: json, xml.",
    )


class MpUnicornbayOptionsEodDataAttributes(BaseModel):
    """Common fields for options contract/EOD records. Values may be null.

    Parameters
    ----------
    contract : str, optional
    underlying_symbol : str, optional
    exp_date : str, optional
        YYYY-MM-DD.
    expiration_type : str, optional
    type : Literal['call', 'put'], optional
        Choices: call, put.
    strike : float, optional
    exchange : str, optional
    currency : str, optional
    open : float, optional
    high : float, optional
    low : float, optional
    last : float, optional
    last_size : int, optional
    change : float, optional
    pctchange : float, optional
    previous : float, optional
    previous_date : str, optional
    bid : float, optional
    bid_date : str, optional
    bid_size : int, optional
    ask : float, optional
    ask_date : str, optional
    ask_size : int, optional
    moneyness : float, optional
    volume : int, optional
    volume_change : int, optional
    volume_pctchange : float, optional
    open_interest : int, optional
    open_interest_change : int, optional
    open_interest_pctchange : float, optional
    volatility : float, optional
    volatility_change : float, optional
    volatility_pctchange : float, optional
    theoretical : float, optional
    delta : float, optional
    gamma : float, optional
    theta : float, optional
    vega : float, optional
    rho : float, optional
    tradetime : str, optional
        YYYY-MM-DD (last trade or last market update; see docs).
    vol_oi_ratio : float, optional
    dte : int, optional
        Days to expiration.
    midpoint : float, optional
    """

    contract: str | None = Field(default=None, description="")
    underlying_symbol: str | None = Field(default=None, description="")
    exp_date: str | None = Field(default=None, description="YYYY-MM-DD.")
    expiration_type: str | None = Field(default=None, description="")
    type: Literal["call", "put"] | None = Field(
        default=None,
        description="Choices: call, put.",
    )
    strike: float | None = Field(default=None, description="")
    exchange: str | None = Field(default=None, description="")
    currency: str | None = Field(default=None, description="")
    open: float | None = Field(default=None, description="")
    high: float | None = Field(default=None, description="")
    low: float | None = Field(default=None, description="")
    last: float | None = Field(default=None, description="")
    last_size: int | None = Field(default=None, description="")
    change: float | None = Field(default=None, description="")
    pctchange: float | None = Field(default=None, description="")
    previous: float | None = Field(default=None, description="")
    previous_date: str | None = Field(default=None, description="")
    bid: float | None = Field(default=None, description="")
    bid_date: str | None = Field(default=None, description="")
    bid_size: int | None = Field(default=None, description="")
    ask: float | None = Field(default=None, description="")
    ask_date: str | None = Field(default=None, description="")
    ask_size: int | None = Field(default=None, description="")
    moneyness: float | None = Field(default=None, description="")
    volume: int | None = Field(default=None, description="")
    volume_change: int | None = Field(default=None, description="")
    volume_pctchange: float | None = Field(default=None, description="")
    open_interest: int | None = Field(default=None, description="")
    open_interest_change: int | None = Field(default=None, description="")
    open_interest_pctchange: float | None = Field(default=None, description="")
    volatility: float | None = Field(default=None, description="")
    volatility_change: float | None = Field(default=None, description="")
    volatility_pctchange: float | None = Field(default=None, description="")
    theoretical: float | None = Field(default=None, description="")
    delta: float | None = Field(default=None, description="")
    gamma: float | None = Field(default=None, description="")
    theta: float | None = Field(default=None, description="")
    vega: float | None = Field(default=None, description="")
    rho: float | None = Field(default=None, description="")
    tradetime: str | None = Field(
        default=None,
        description="YYYY-MM-DD (last trade or last market update; see docs).",
    )
    vol_oi_ratio: float | None = Field(default=None, description="")
    dte: int | None = Field(default=None, description="Days to expiration.")
    midpoint: float | None = Field(default=None, description="")


class MpUnicornbayOptionsEodData(Data):
    """Response row for mp.unicornbay.options.eod.

    Parameters
    ----------
    id : str
    type : Literal['options-eod']
        Choices: options-eod.
    attributes : MpUnicornbayOptionsEodDataAttributes
        Common fields for options contract/EOD records. Values may be null. Inner fields: contract (str), underlying_symbol (str), exp_date (str), expiration_type (Any), type (str), strike (Any), exchange (Any), currency (Any), open (Any), high (Any), low (Any), last (Any), last_size (Any), change (Any), pctchange (Any), previous (Any), previous_date (Any), bid (Any), bid_date (Any), bid_size (Any), ask (Any), ask_date (Any), ask_size (Any), moneyness (Any), volume (Any), volume_change (Any), volume_pctchange (Any), open_interest (Any), open_interest_change (Any), open_interest_pctchange (Any), volatility (Any), volatility_change (Any), volatility_pctchange (Any), theoretical (Any), delta (Any), gamma (Any), theta (Any), vega (Any), rho (Any), tradetime (Any), vol_oi_ratio (Any), dte (Any), midpoint (Any).
    """

    id: str = Field(description="")
    type: Literal["options-eod"] = Field(description="Choices: options-eod.")
    attributes: MpUnicornbayOptionsEodDataAttributes = Field(
        description="Common fields for options contract/EOD records. Values may be null. Inner fields: contract (str), underlying_symbol (str), exp_date (str), expiration_type (Any), type (str), strike (Any), exchange (Any), currency (Any), open (Any), high (Any), low (Any), last (Any), last_size (Any), change (Any), pctchange (Any), previous (Any), previous_date (Any), bid (Any), bid_date (Any), bid_size (Any), ask (Any), ask_date (Any), ask_size (Any), moneyness (Any), volume (Any), volume_change (Any), volume_pctchange (Any), open_interest (Any), open_interest_change (Any), open_interest_pctchange (Any), volatility (Any), volatility_change (Any), volatility_pctchange (Any), theoretical (Any), delta (Any), gamma (Any), theta (Any), vega (Any), rho (Any), tradetime (Any), vol_oi_ratio (Any), dte (Any), midpoint (Any).",
    )


class MpUnicornbayOptionsEodFetcher(
    Fetcher[MpUnicornbayOptionsEodQueryParams, list[MpUnicornbayOptionsEodData]]
):
    """Returns EOD trades/bid data for options, with the same filter set as contracts. Supports compact mode (`compact=1`) to return arrays instead of objects."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpUnicornbayOptionsEodQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpUnicornbayOptionsEodQueryParams
            Validated query parameters.
        """
        return MpUnicornbayOptionsEodQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpUnicornbayOptionsEodQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/unicornbay/options/eod and split rows from metadata.

        Parameters
        ----------
        query : MpUnicornbayOptionsEodQueryParams
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
        _path = "/mp/unicornbay/options/eod"

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
        query: MpUnicornbayOptionsEodQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpUnicornbayOptionsEodData] | AnnotatedResult[list[MpUnicornbayOptionsEodData]]:
        """Type the unpacked rows as MpUnicornbayOptionsEodData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpUnicornbayOptionsEodQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpUnicornbayOptionsEodData] | AnnotatedResult[list[MpUnicornbayOptionsEodData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpUnicornbayOptionsEodData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "attributes": {
                "description": "Common fields for options contract/EOD records. Values may be null."
            }
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
