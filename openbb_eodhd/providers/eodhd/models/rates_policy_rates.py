"""Fetcher for rates.policy-rates — generated from spec.

Hits ``https://eodhd.com/api/rates/policy-rates`` via HTTP GET.
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


class RatesPolicyRatesQueryParams(QueryParams):
    """Query parameters for rates.policy-rates.

    Parameters
    ----------
    filter_code_ : str, optional
        Filter by policy rate code.
    filter_country_ : str, optional
        Filter by country.
    filter_central_bank_ : str, optional
        Filter by central bank (e.g., 'FED', 'ECB').
    filter_from_ : str, optional
        Start date (YYYY-MM-DD).
    filter_to_ : str, optional
        End date (YYYY-MM-DD).
    page_offset_ : int, optional
        Pagination offset (records to skip). (default: 0)
    page_limit_ : int, optional
        Number of records per page. Default 20, maximum 100. (default: 20)
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    filter_code_: str | None = Field(
        default=None,
        alias="filter[code]",
        description="Filter by policy rate code.",
    )
    filter_country_: str | None = Field(
        default=None,
        alias="filter[country]",
        description="Filter by country.",
    )
    filter_central_bank_: str | None = Field(
        default=None,
        alias="filter[central_bank]",
        description="Filter by central bank (e.g., 'FED', 'ECB').",
    )
    filter_from_: str | None = Field(
        default=None,
        alias="filter[from]",
        description="Start date (YYYY-MM-DD).",
    )
    filter_to_: str | None = Field(
        default=None,
        alias="filter[to]",
        description="End date (YYYY-MM-DD).",
    )
    page_offset_: int | None = Field(
        default=0,
        alias="page[offset]",
        description="Pagination offset (records to skip).",
    )
    page_limit_: int | None = Field(
        default=20,
        alias="page[limit]",
        description="Number of records per page. Default 20, maximum 100.",
    )
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class RatesPolicyRatesData(Data):
    """Response row for rates.policy-rates.

    Parameters
    ----------
    date : datetime.date, optional
        Observation date.
    code : str, optional
        Policy rate code.
    country : str, optional
        Country.
    central_bank : str, optional
        Central bank.
    rate : float, optional
        Policy rate value.
    source : str, optional
        Data source.
    source_series_id : str, optional
        Source series identifier.
    """

    date: datetime.date | None = Field(default=None, description="Observation date.")
    code: str | None = Field(default=None, description="Policy rate code.")
    country: str | None = Field(default=None, description="Country.")
    central_bank: str | None = Field(default=None, description="Central bank.")
    rate: float | None = Field(default=None, description="Policy rate value.")
    source: str | None = Field(default=None, description="Data source.")
    source_series_id: str | None = Field(
        default=None,
        description="Source series identifier.",
    )


class RatesPolicyRatesFetcher(Fetcher[RatesPolicyRatesQueryParams, list[RatesPolicyRatesData]]):
    """Returns central bank policy (target) interest rates by code, country, and central bank."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> RatesPolicyRatesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        RatesPolicyRatesQueryParams
            Validated query parameters.
        """
        return RatesPolicyRatesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: RatesPolicyRatesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/rates/policy-rates and split rows from metadata.

        Parameters
        ----------
        query : RatesPolicyRatesQueryParams
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
        _path = "/rates/policy-rates"

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
        query: RatesPolicyRatesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[RatesPolicyRatesData] | AnnotatedResult[list[RatesPolicyRatesData]]:
        """Type the unpacked rows as RatesPolicyRatesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : RatesPolicyRatesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[RatesPolicyRatesData] | AnnotatedResult[list[RatesPolicyRatesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [RatesPolicyRatesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Observation date.", "format": "date"},
            "code": {"description": "Policy rate code."},
            "country": {"description": "Country."},
            "central_bank": {"description": "Central bank."},
            "rate": {"description": "Policy rate value."},
            "source": {"description": "Data source."},
            "source_series_id": {"description": "Source series identifier."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
