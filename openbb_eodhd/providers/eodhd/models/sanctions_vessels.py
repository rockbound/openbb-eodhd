"""Fetcher for sanctions.vessels — generated from spec.

Hits ``https://eodhd.com/api/sanctions/vessels`` via HTTP GET.
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


class SanctionsVesselsQueryParams(QueryParams):
    """Query parameters for sanctions.vessels.

    Parameters
    ----------
    source : Literal['ofac'], optional
        Filter by sanctions source. Choices: ofac.
    imo : str, optional
        Filter by IMO number.
    flag : str, optional
        Filter by flag (country of registration).
    vessel_type : str, optional
        Filter by vessel type.
    q : str, optional
        Free-text search query (minimum 2 characters).
    program : str, optional
        Filter by sanctions program code.
    page_offset_ : int, optional
        Pagination offset (records to skip). (default: 0)
    page_limit_ : int, optional
        Number of records per page. Default 20, maximum 100. (default: 20)
    fmt : Literal['json', 'csv'], optional
        Output format. Choices: json, csv. (default: 'json')
    """

    source: Literal["ofac"] | None = Field(
        default=None,
        description="Filter by sanctions source. Choices: ofac.",
    )
    imo: str | None = Field(default=None, description="Filter by IMO number.")
    flag: str | None = Field(
        default=None,
        description="Filter by flag (country of registration).",
    )
    vessel_type: str | None = Field(default=None, description="Filter by vessel type.")
    q: str | None = Field(
        default=None,
        description="Free-text search query (minimum 2 characters).",
    )
    program: str | None = Field(
        default=None,
        description="Filter by sanctions program code.",
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


class SanctionsVesselsData(Data):
    """Response row for sanctions.vessels.

    Parameters
    ----------
    id : int, optional
        Unique identifier of the record.
    call_sign : str, optional
        Vessel call sign.
    vessel_type : str, optional
        Type of vessel.
    flag : str, optional
        Flag (country of registration).
    tonnage : float, optional
        Vessel tonnage.
    gross_tonnage : float, optional
        Gross registered tonnage.
    owner : str, optional
        Vessel owner.
    imo_number : str, optional
        IMO number.
    mmsi : str, optional
        Maritime Mobile Service Identity.
    entity_source_uid : str, optional
        Source UID of the linked sanctioned entity.
    entity_name : str, optional
        Name of the linked sanctioned entity.
    source : str, optional
        Sanctions data source (e.g., 'OFAC').
    programs : list[str], optional
        Sanctions program codes the vessel is listed under.
    country : str, optional
        Associated country.
    is_active : bool, optional
        Whether the listing is currently active.
    """

    id: int | None = Field(default=None, description="Unique identifier of the record.")
    call_sign: str | None = Field(default=None, description="Vessel call sign.")
    vessel_type: str | None = Field(default=None, description="Type of vessel.")
    flag: str | None = Field(
        default=None,
        description="Flag (country of registration).",
    )
    tonnage: float | None = Field(default=None, description="Vessel tonnage.")
    gross_tonnage: float | None = Field(
        default=None,
        description="Gross registered tonnage.",
    )
    owner: str | None = Field(default=None, description="Vessel owner.")
    imo_number: str | None = Field(default=None, description="IMO number.")
    mmsi: str | None = Field(
        default=None,
        description="Maritime Mobile Service Identity.",
    )
    entity_source_uid: str | None = Field(
        default=None,
        description="Source UID of the linked sanctioned entity.",
    )
    entity_name: str | None = Field(
        default=None,
        description="Name of the linked sanctioned entity.",
    )
    source: str | None = Field(
        default=None,
        description="Sanctions data source (e.g., 'OFAC').",
    )
    programs: list[str] | None = Field(
        default=None,
        description="Sanctions program codes the vessel is listed under.",
    )
    country: str | None = Field(default=None, description="Associated country.")
    is_active: bool | None = Field(
        default=None,
        description="Whether the listing is currently active.",
    )


class SanctionsVesselsFetcher(Fetcher[SanctionsVesselsQueryParams, list[SanctionsVesselsData]]):
    """Returns sanctioned vessels aggregated from OFAC and other sanctions sources, including IMO/MMSI identifiers, flag, and linked sanctioned entity."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SanctionsVesselsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SanctionsVesselsQueryParams
            Validated query parameters.
        """
        return SanctionsVesselsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SanctionsVesselsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/sanctions/vessels and split rows from metadata.

        Parameters
        ----------
        query : SanctionsVesselsQueryParams
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
        _path = "/sanctions/vessels"

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
        query: SanctionsVesselsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SanctionsVesselsData] | AnnotatedResult[list[SanctionsVesselsData]]:
        """Type the unpacked rows as SanctionsVesselsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SanctionsVesselsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SanctionsVesselsData] | AnnotatedResult[list[SanctionsVesselsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SanctionsVesselsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "id": {"description": "Unique identifier of the record."},
            "call_sign": {"description": "Vessel call sign."},
            "vessel_type": {"description": "Type of vessel."},
            "flag": {"description": "Flag (country of registration)."},
            "tonnage": {"description": "Vessel tonnage."},
            "gross_tonnage": {"description": "Gross registered tonnage."},
            "owner": {"description": "Vessel owner."},
            "imo_number": {"description": "IMO number."},
            "mmsi": {"description": "Maritime Mobile Service Identity."},
            "entity_source_uid": {"description": "Source UID of the linked sanctioned entity."},
            "entity_name": {"description": "Name of the linked sanctioned entity."},
            "source": {"description": "Sanctions data source (e.g., 'OFAC')."},
            "programs": {"description": "Sanctions program codes the vessel is listed under."},
            "country": {"description": "Associated country."},
            "is_active": {"description": "Whether the listing is currently active."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
