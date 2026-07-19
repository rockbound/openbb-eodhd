"""Fetcher for spreads.funding-stress — generated from spec.

Hits ``https://eodhd.com/api/spreads/funding-stress`` via HTTP GET.
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


class SpreadsFundingStressQueryParams(QueryParams):
    """Query parameters for spreads.funding-stress.

    Parameters
    ----------
    filter_code_ : str, optional
        Filter by spread code (e.g., 'SOFR_OIS').
    filter_from_ : str, optional
        Start date (YYYY-MM-DD).
    filter_to_ : str, optional
        End date (YYYY-MM-DD).
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    filter_code_: str | None = Field(
        default=None,
        alias="filter[code]",
        description="Filter by spread code (e.g., 'SOFR_OIS').",
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
    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Output format. Choices: json, csv.",
    )


class SpreadsFundingStressData(Data):
    """Response row for spreads.funding-stress.

    Parameters
    ----------
    date : datetime.date, optional
        Observation date.
    code : str, optional
        Spread code.
    value_bps : float, optional
        Spread value in basis points.
    formula : str, optional
        Formula used to compute the spread.
    leg_a : str, optional
        First rate leg code.
    leg_b : str, optional
        Second rate leg code.
    leg_a_rate : float, optional
        Rate value of the first leg.
    leg_b_rate : float, optional
        Rate value of the second leg.
    """

    date: datetime.date | None = Field(default=None, description="Observation date.")
    code: str | None = Field(default=None, description="Spread code.")
    value_bps: float | None = Field(
        default=None,
        description="Spread value in basis points.",
    )
    formula: str | None = Field(
        default=None,
        description="Formula used to compute the spread.",
    )
    leg_a: str | None = Field(default=None, description="First rate leg code.")
    leg_b: str | None = Field(default=None, description="Second rate leg code.")
    leg_a_rate: float | None = Field(
        default=None,
        description="Rate value of the first leg.",
    )
    leg_b_rate: float | None = Field(
        default=None,
        description="Rate value of the second leg.",
    )


class SpreadsFundingStressFetcher(
    Fetcher[SpreadsFundingStressQueryParams, list[SpreadsFundingStressData]]
):
    """Returns funding-stress spread series (in basis points) computed as the difference between two rate legs, with the underlying formula and leg values."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SpreadsFundingStressQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SpreadsFundingStressQueryParams
            Validated query parameters.
        """
        return SpreadsFundingStressQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SpreadsFundingStressQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/spreads/funding-stress and split rows from metadata.

        Parameters
        ----------
        query : SpreadsFundingStressQueryParams
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
        _path = "/spreads/funding-stress"

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
        query: SpreadsFundingStressQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SpreadsFundingStressData] | AnnotatedResult[list[SpreadsFundingStressData]]:
        """Type the unpacked rows as SpreadsFundingStressData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SpreadsFundingStressQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SpreadsFundingStressData] | AnnotatedResult[list[SpreadsFundingStressData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SpreadsFundingStressData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "date": {"description": "Observation date.", "format": "date"},
            "code": {"description": "Spread code."},
            "value_bps": {"description": "Spread value in basis points."},
            "formula": {"description": "Formula used to compute the spread."},
            "leg_a": {"description": "First rate leg code."},
            "leg_b": {"description": "Second rate leg code."},
            "leg_a_rate": {"description": "Rate value of the first leg."},
            "leg_b_rate": {"description": "Rate value of the second leg."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
