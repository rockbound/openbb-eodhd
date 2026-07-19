"""Fetcher for exchange-details — generated from spec.

Hits ``https://eodhd.com/api/exchange-details/{EXCHANGE_CODE}`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field, field_validator

from ....utils import safe_json_loads, unpack_response


class ExchangeDetailsQueryParams(QueryParams):
    """Query parameters for exchange-details.

    Parameters
    ----------
    EXCHANGE_CODE : str
        Exchange code for which details are to be retrieved (e.g., 'US' for the USA exchange).
    fmt : Literal['json', 'csv'], optional
        Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv. (default: 'json')
    from_ : str, optional
        Start date for holiday data (YYYY-MM-DD). Defaults to 6 months before the current date.
    to : str, optional
        End date for holiday data (YYYY-MM-DD). Defaults to 6 months after the current date.
    format_version : int, optional
        Response format version.
    """

    EXCHANGE_CODE: str = Field(
        description="Exchange code for which details are to be retrieved (e.g., 'US' for the USA exchange).",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv.",
    )
    from_: str | None = Field(
        default=None,
        alias="from",
        description="Start date for holiday data (YYYY-MM-DD). Defaults to 6 months before the current date.",
    )
    to: str | None = Field(
        default=None,
        description="End date for holiday data (YYYY-MM-DD). Defaults to 6 months after the current date.",
    )
    format_version: int | None = Field(
        default=None,
        description="Response format version.",
    )


class ExchangeDetailsDataExchangeHolidaysItem(BaseModel):
    """ExchangeDetailsDataExchangeHolidaysItem.

    Parameters
    ----------
    Holiday : str, optional
    Date : datetime.date, optional
    Type : str, optional
    """

    Holiday: str | None = Field(default=None, description="")
    Date: datetime.date | None = Field(default=None, description="")
    Type: str | None = Field(default=None, description="")


class ExchangeDetailsDataExchangeEarlyCloseDaysItem(BaseModel):
    """ExchangeDetailsDataExchangeEarlyCloseDaysItem.

    Parameters
    ----------
    Date : datetime.date, optional
    CloseTime : str, optional
    """

    Date: datetime.date | None = Field(default=None, description="")
    CloseTime: str | None = Field(default=None, description="")


class ExchangeDetailsDataTradingHours(BaseModel):
    """ExchangeDetailsDataTradingHours.

    Parameters
    ----------
    Open : str, optional
    Close : str, optional
    OpenUTC : str, optional
    CloseUTC : str, optional
    WorkingDays : str, optional
    """

    Open: str | None = Field(default=None, description="")
    Close: str | None = Field(default=None, description="")
    OpenUTC: str | None = Field(default=None, description="")
    CloseUTC: str | None = Field(default=None, description="")
    WorkingDays: str | None = Field(default=None, description="")


class ExchangeDetailsData(Data):
    """Response row for exchange-details.

    Parameters
    ----------
    Name : str, optional
    Code : str, optional
    OperatingMIC : str, optional
    Country : str, optional
    Currency : str, optional
    Timezone : str, optional
    ExchangeHolidays : list[ExchangeDetailsDataExchangeHolidaysItem], optional
        Inner item fields: Holiday (str), Date (date), Type (str).
    ExchangeEarlyCloseDays : list[ExchangeDetailsDataExchangeEarlyCloseDaysItem], optional
        Inner item fields: Date (date), CloseTime (str).
    isOpen : bool, optional
    TradingHours : ExchangeDetailsDataTradingHours, optional
        Inner fields: Open (str), Close (str), OpenUTC (str), CloseUTC (str), WorkingDays (str).
    ActiveTickers : int, optional
    PreviousDayUpdatedTickers : int, optional
    UpdatedTickers : int, optional
    """

    Name: str | None = Field(default=None, description="")
    Code: str | None = Field(default=None, description="")
    OperatingMIC: str | None = Field(default=None, description="")
    Country: str | None = Field(default=None, description="")
    Currency: str | None = Field(default=None, description="")
    Timezone: str | None = Field(default=None, description="")
    ExchangeHolidays: list[ExchangeDetailsDataExchangeHolidaysItem] | None = Field(
        default=None,
        description="Inner item fields: Holiday (str), Date (date), Type (str).",
    )
    ExchangeEarlyCloseDays: list[ExchangeDetailsDataExchangeEarlyCloseDaysItem] | None = Field(
        default=None,
        description="Inner item fields: Date (date), CloseTime (str).",
    )
    isOpen: bool | None = Field(default=None, description="")
    TradingHours: ExchangeDetailsDataTradingHours | None = Field(
        default=None,
        description="Inner fields: Open (str), Close (str), OpenUTC (str), CloseUTC (str), WorkingDays (str).",
    )
    ActiveTickers: int | None = Field(default=None, description="")
    PreviousDayUpdatedTickers: int | None = Field(default=None, description="")
    UpdatedTickers: int | None = Field(default=None, description="")

    @field_validator("TradingHours", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class ExchangeDetailsFetcher(Fetcher[ExchangeDetailsQueryParams, list[ExchangeDetailsData]]):
    """Retrieve exchange details, trading hours, holidays, and active tickers for a specified exchange."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> ExchangeDetailsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        ExchangeDetailsQueryParams
            Validated query parameters.
        """
        return ExchangeDetailsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: ExchangeDetailsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/exchange-details/{EXCHANGE_CODE} and split rows from metadata.

        Parameters
        ----------
        query : ExchangeDetailsQueryParams
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
        _path = f"/exchange-details/{query.EXCHANGE_CODE}"

        _query_dict = query.model_dump(by_alias=True, exclude={"EXCHANGE_CODE"}, exclude_none=True)
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
        query: ExchangeDetailsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[ExchangeDetailsData] | AnnotatedResult[list[ExchangeDetailsData]]:
        """Type the unpacked rows as ExchangeDetailsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : ExchangeDetailsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[ExchangeDetailsData] | AnnotatedResult[list[ExchangeDetailsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [ExchangeDetailsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
