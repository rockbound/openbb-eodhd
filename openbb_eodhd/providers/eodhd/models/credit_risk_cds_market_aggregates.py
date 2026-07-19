"""Fetcher for credit-risk.cds-market.aggregates — generated from spec.

Hits ``https://eodhd.com/api/credit-risk/cds-market/aggregates`` via HTTP GET.
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


class CreditRiskCdsMarketAggregatesQueryParams(QueryParams):
    """Query parameters for credit-risk.cds-market.aggregates.

    Parameters
    ----------
    filter_metric_ : Literal['gross_notional'], optional
        Aggregate metric to return. Choices: gross_notional.
    filter_dimension_ : Literal['grade', 'cleared_status'], optional
        Breakdown dimension. Choices: grade, cleared_status.
    filter_value_ : str, optional
        Filter by the value of the breakdown dimension.
    filter_region_ : str, optional
        Filter by region.
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

    filter_metric_: Literal["gross_notional"] | None = Field(
        default=None,
        alias="filter[metric]",
        description="Aggregate metric to return. Choices: gross_notional.",
    )
    filter_dimension_: Literal["grade", "cleared_status"] | None = Field(
        default=None,
        alias="filter[dimension]",
        description="Breakdown dimension. Choices: grade, cleared_status.",
    )
    filter_value_: str | None = Field(
        default=None,
        alias="filter[value]",
        description="Filter by the value of the breakdown dimension.",
    )
    filter_region_: str | None = Field(
        default=None,
        alias="filter[region]",
        description="Filter by region.",
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


class CreditRiskCdsMarketAggregatesData(Data):
    """Response row for credit-risk.cds-market.aggregates.

    Parameters
    ----------
    as_of_date : datetime.datetime, optional
        As-of timestamp for the aggregate.
    release_date : datetime.datetime, optional
        Release timestamp of the aggregate.
    metric : str, optional
        Aggregate metric name.
    breakdown_dimension : str, optional
        Dimension used for the breakdown.
    breakdown_value : str, optional
        Value of the breakdown dimension.
    region : str, optional
        Region.
    usd_notional_mn : float, optional
        Notional amount in USD millions.
    source : str, optional
        Data source.
    """

    as_of_date: datetime.datetime | None = Field(
        default=None,
        description="As-of timestamp for the aggregate.",
    )
    release_date: datetime.datetime | None = Field(
        default=None,
        description="Release timestamp of the aggregate.",
    )
    metric: str | None = Field(default=None, description="Aggregate metric name.")
    breakdown_dimension: str | None = Field(
        default=None,
        description="Dimension used for the breakdown.",
    )
    breakdown_value: str | None = Field(
        default=None,
        description="Value of the breakdown dimension.",
    )
    region: str | None = Field(default=None, description="Region.")
    usd_notional_mn: float | None = Field(
        default=None,
        description="Notional amount in USD millions.",
    )
    source: str | None = Field(default=None, description="Data source.")


class CreditRiskCdsMarketAggregatesFetcher(
    Fetcher[CreditRiskCdsMarketAggregatesQueryParams, list[CreditRiskCdsMarketAggregatesData]]
):
    """Returns aggregated CDS market statistics (e.g., gross notional) broken down by dimensions such as grade or cleared status."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CreditRiskCdsMarketAggregatesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CreditRiskCdsMarketAggregatesQueryParams
            Validated query parameters.
        """
        return CreditRiskCdsMarketAggregatesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CreditRiskCdsMarketAggregatesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/credit-risk/cds-market/aggregates and split rows from metadata.

        Parameters
        ----------
        query : CreditRiskCdsMarketAggregatesQueryParams
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
        _path = "/credit-risk/cds-market/aggregates"

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
        query: CreditRiskCdsMarketAggregatesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> (
        list[CreditRiskCdsMarketAggregatesData]
        | AnnotatedResult[list[CreditRiskCdsMarketAggregatesData]]
    ):
        """Type the unpacked rows as CreditRiskCdsMarketAggregatesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CreditRiskCdsMarketAggregatesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CreditRiskCdsMarketAggregatesData] | AnnotatedResult[list[CreditRiskCdsMarketAggregatesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CreditRiskCdsMarketAggregatesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "as_of_date": {
                "description": "As-of timestamp for the aggregate.",
                "format": "date-time",
            },
            "release_date": {
                "description": "Release timestamp of the aggregate.",
                "format": "date-time",
            },
            "metric": {"description": "Aggregate metric name."},
            "breakdown_dimension": {"description": "Dimension used for the breakdown."},
            "breakdown_value": {"description": "Value of the breakdown dimension."},
            "region": {"description": "Region."},
            "usd_notional_mn": {"description": "Notional amount in USD millions."},
            "source": {"description": "Data source."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
