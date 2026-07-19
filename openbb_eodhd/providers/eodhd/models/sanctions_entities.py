"""Fetcher for sanctions.entities — generated from spec.

Hits ``https://eodhd.com/api/sanctions/entities`` via HTTP GET.
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


class SanctionsEntitiesQueryParams(QueryParams):
    """Query parameters for sanctions.entities.

    Parameters
    ----------
    source : Literal['ofac'], optional
        Filter by sanctions source. Choices: ofac.
    type : Literal['individual', 'entity', 'vessel', 'aircraft'], optional
        Filter by entity type. Choices: individual, entity, vessel, aircraft.
    program : str, optional
        Filter by sanctions program code.
    country : str, optional
        Filter by country.
    q : str, optional
        Free-text search query (minimum 2 characters).
    active : Literal['true', 'false'], optional
        Filter by active listing status. Choices: true, false.
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
    type: Literal["individual", "entity", "vessel", "aircraft"] | None = Field(
        default=None,
        description="Filter by entity type. Choices: individual, entity, vessel, aircraft.",
    )
    program: str | None = Field(
        default=None,
        description="Filter by sanctions program code.",
    )
    country: str | None = Field(default=None, description="Filter by country.")
    q: str | None = Field(
        default=None,
        description="Free-text search query (minimum 2 characters).",
    )
    active: Literal["true", "false"] | None = Field(
        default=None,
        description="Filter by active listing status. Choices: true, false.",
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


class SanctionsEntitiesData(Data):
    """Response row for sanctions.entities.

    Parameters
    ----------
    id : int, optional
        Unique identifier of the record.
    source : str, optional
        Sanctions data source (e.g., 'OFAC').
    source_uid : str, optional
        Unique identifier of the entity within the source.
    entity_type : str, optional
        Type of entity (e.g., individual, entity, vessel).
    name : str, optional
        Primary name of the sanctioned entity.
    programs : list[str], optional
        Sanctions program codes the entity is listed under.
    country : str, optional
        Associated country.
    remarks : str, optional
        Free-text remarks from the source listing.
    listed_date : str, optional
        Date the entity was listed.
    is_active : bool, optional
        Whether the listing is currently active.
    aliases : list[str], optional
        Known aliases for the entity.
    identifiers : list[dict[str, Any]], optional
        Identification documents or numbers associated with the entity.
    """

    id: int | None = Field(default=None, description="Unique identifier of the record.")
    source: str | None = Field(
        default=None,
        description="Sanctions data source (e.g., 'OFAC').",
    )
    source_uid: str | None = Field(
        default=None,
        description="Unique identifier of the entity within the source.",
    )
    entity_type: str | None = Field(
        default=None,
        description="Type of entity (e.g., individual, entity, vessel).",
    )
    name: str | None = Field(
        default=None,
        description="Primary name of the sanctioned entity.",
    )
    programs: list[str] | None = Field(
        default=None,
        description="Sanctions program codes the entity is listed under.",
    )
    country: str | None = Field(default=None, description="Associated country.")
    remarks: str | None = Field(
        default=None,
        description="Free-text remarks from the source listing.",
    )
    listed_date: str | None = Field(
        default=None,
        description="Date the entity was listed.",
    )
    is_active: bool | None = Field(
        default=None,
        description="Whether the listing is currently active.",
    )
    aliases: list[str] | None = Field(
        default=None,
        description="Known aliases for the entity.",
    )
    identifiers: list[dict[str, Any]] | None = Field(
        default=None,
        description="Identification documents or numbers associated with the entity.",
    )


class SanctionsEntitiesFetcher(Fetcher[SanctionsEntitiesQueryParams, list[SanctionsEntitiesData]]):
    """Returns sanctioned entities (individuals and organizations) aggregated from OFAC and other sanctions sources, including programs, aliases, and identifiers."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> SanctionsEntitiesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        SanctionsEntitiesQueryParams
            Validated query parameters.
        """
        return SanctionsEntitiesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: SanctionsEntitiesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/sanctions/entities and split rows from metadata.

        Parameters
        ----------
        query : SanctionsEntitiesQueryParams
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
        _path = "/sanctions/entities"

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
        query: SanctionsEntitiesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[SanctionsEntitiesData] | AnnotatedResult[list[SanctionsEntitiesData]]:
        """Type the unpacked rows as SanctionsEntitiesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : SanctionsEntitiesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[SanctionsEntitiesData] | AnnotatedResult[list[SanctionsEntitiesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [SanctionsEntitiesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "id": {"description": "Unique identifier of the record."},
            "source": {"description": "Sanctions data source (e.g., 'OFAC')."},
            "source_uid": {"description": "Unique identifier of the entity within the source."},
            "entity_type": {"description": "Type of entity (e.g., individual, entity, vessel)."},
            "name": {"description": "Primary name of the sanctioned entity."},
            "programs": {"description": "Sanctions program codes the entity is listed under."},
            "country": {"description": "Associated country."},
            "remarks": {"description": "Free-text remarks from the source listing."},
            "listed_date": {"description": "Date the entity was listed."},
            "is_active": {"description": "Whether the listing is currently active."},
            "aliases": {"description": "Known aliases for the entity."},
            "identifiers": {
                "description": "Identification documents or numbers associated with the entity."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
