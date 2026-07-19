"""Fetcher for credit-risk.corporate.hqm-yields — generated from spec.

Hits ``https://eodhd.com/api/credit-risk/corporate/hqm-yields`` via HTTP GET.
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


class CreditRiskCorporateHqmYieldsQueryParams(QueryParams):
    """Query parameters for credit-risk.corporate.hqm-yields.

    Parameters
    ----------
    filter_tenor_ : str, optional
        Filter by tenor in years, single value or comma-separated list (e.g., '10' or '2,5,10'). Allowed values 1, 2, 3, 5, 7, 10, 15, 20, 25, 30.
    filter_type_ : str, optional
        Yield curve type, single value or comma-separated list (e.g., 'par' or 'par,spot'). Allowed values par, spot (case-insensitive).
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

    filter_tenor_: str | None = Field(
        default=None,
        alias="filter[tenor]",
        description="Filter by tenor in years, single value or comma-separated list (e.g., '10' or '2,5,10'). Allowed values 1, 2, 3, 5, 7, 10, 15, 20, 25, 30.",
    )
    filter_type_: str | None = Field(
        default=None,
        alias="filter[type]",
        description="Yield curve type, single value or comma-separated list (e.g., 'par' or 'par,spot'). Allowed values par, spot (case-insensitive).",
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


class CreditRiskCorporateHqmYieldsData(Data):
    """Response row for credit-risk.corporate.hqm-yields.

    Parameters
    ----------
    series_id : str, optional
        Source series identifier.
    tenor_years : float, optional
        Tenor in years.
    yield_type : str, optional
        Yield curve type (par or spot).
    as_of_date : datetime.datetime, optional
        As-of timestamp for the yield value.
    yield_value : float, optional
        Yield value.
    source : str, optional
        Data source.
    """

    series_id: str | None = Field(default=None, description="Source series identifier.")
    tenor_years: float | None = Field(default=None, description="Tenor in years.")
    yield_type: str | None = Field(
        default=None,
        description="Yield curve type (par or spot).",
    )
    as_of_date: datetime.datetime | None = Field(
        default=None,
        description="As-of timestamp for the yield value.",
    )
    yield_value: float | None = Field(default=None, description="Yield value.")
    source: str | None = Field(default=None, description="Data source.")


class CreditRiskCorporateHqmYieldsFetcher(
    Fetcher[CreditRiskCorporateHqmYieldsQueryParams, list[CreditRiskCorporateHqmYieldsData]]
):
    """Returns High Quality Market corporate bond yield curve values (par and spot) across standard tenors."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CreditRiskCorporateHqmYieldsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CreditRiskCorporateHqmYieldsQueryParams
            Validated query parameters.
        """
        return CreditRiskCorporateHqmYieldsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CreditRiskCorporateHqmYieldsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/credit-risk/corporate/hqm-yields and split rows from metadata.

        Parameters
        ----------
        query : CreditRiskCorporateHqmYieldsQueryParams
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
        _path = "/credit-risk/corporate/hqm-yields"

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
        query: CreditRiskCorporateHqmYieldsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> (
        list[CreditRiskCorporateHqmYieldsData]
        | AnnotatedResult[list[CreditRiskCorporateHqmYieldsData]]
    ):
        """Type the unpacked rows as CreditRiskCorporateHqmYieldsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CreditRiskCorporateHqmYieldsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CreditRiskCorporateHqmYieldsData] | AnnotatedResult[list[CreditRiskCorporateHqmYieldsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CreditRiskCorporateHqmYieldsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "series_id": {"description": "Source series identifier."},
            "tenor_years": {"description": "Tenor in years."},
            "yield_type": {"description": "Yield curve type (par or spot)."},
            "as_of_date": {
                "description": "As-of timestamp for the yield value.",
                "format": "date-time",
            },
            "yield_value": {"description": "Yield value."},
            "source": {"description": "Data source."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
