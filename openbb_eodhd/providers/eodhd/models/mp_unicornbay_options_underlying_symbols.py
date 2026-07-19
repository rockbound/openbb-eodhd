"""Fetcher for mp.unicornbay.options.underlying-symbols — generated from spec.

Hits ``https://eodhd.com/api/mp/unicornbay/options/underlying-symbols`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field, field_validator

from ....utils import safe_json_loads, unpack_response


class MpUnicornbayOptionsUnderlyingSymbolsQueryParams(QueryParams):
    """Query parameters for mp.unicornbay.options.underlying-symbols.

    Parameters
    ----------
    page_offset_ : int, optional
        Pagination offset (records to skip). (default: 0)
    page_limit_ : int, optional
        Pagination limit. Default & max 1000. (default: 1000)
    fmt : Literal['json', 'xml'], optional
        Response format. Choices: json, xml. (default: 'json')
    """

    page_offset_: int | None = Field(
        default=0,
        alias="page[offset]",
        description="Pagination offset (records to skip).",
    )
    page_limit_: int | None = Field(
        default=1000,
        alias="page[limit]",
        description="Pagination limit. Default & max 1000.",
    )
    fmt: Literal["json", "xml"] | None = Field(
        default="json",
        description="Response format. Choices: json, xml.",
    )


class MpUnicornbayOptionsUnderlyingSymbolsDataMeta(BaseModel):
    """Pagination and field metadata.

    Parameters
    ----------
    offset : int, optional
    limit : int, optional
    total : int
    fields : list[str]
    compact : bool, optional
    """

    offset: int | None = Field(default=None, description="")
    limit: int | None = Field(default=None, description="")
    total: int = Field(description="")
    fields: list[str] = Field(description="")
    compact: bool | None = Field(default=None, description="")


class MpUnicornbayOptionsUnderlyingSymbolsDataLinks(BaseModel):
    """MpUnicornbayOptionsUnderlyingSymbolsDataLinks.

    Parameters
    ----------
    next : str
        URL to fetch the next page, or null if last page.
    """

    next: str | None = Field(
        description="URL to fetch the next page, or null if last page.",
    )


class MpUnicornbayOptionsUnderlyingSymbolsData(Data):
    """Response row for mp.unicornbay.options.underlying-symbols.

    Parameters
    ----------
    meta : MpUnicornbayOptionsUnderlyingSymbolsDataMeta
        Pagination and field metadata. Inner fields: offset (int), limit (int), total (int), fields (list[str]), compact (Any).
    data : list[str]
    links : MpUnicornbayOptionsUnderlyingSymbolsDataLinks, optional
        Inner fields: next (Any).
    """

    meta: MpUnicornbayOptionsUnderlyingSymbolsDataMeta = Field(
        description="Pagination and field metadata. Inner fields: offset (int), limit (int), total (int), fields (list[str]), compact (Any).",
    )
    data: list[str] = Field(description="")
    links: MpUnicornbayOptionsUnderlyingSymbolsDataLinks | None = Field(
        default=None,
        description="Inner fields: next (Any).",
    )

    @field_validator("links", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class MpUnicornbayOptionsUnderlyingSymbolsFetcher(
    Fetcher[
        MpUnicornbayOptionsUnderlyingSymbolsQueryParams,
        list[MpUnicornbayOptionsUnderlyingSymbolsData],
    ]
):
    """Returns the list of all supported stock symbols for which option contracts are available. May be paginated."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpUnicornbayOptionsUnderlyingSymbolsQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpUnicornbayOptionsUnderlyingSymbolsQueryParams
            Validated query parameters.
        """
        return MpUnicornbayOptionsUnderlyingSymbolsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpUnicornbayOptionsUnderlyingSymbolsQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/unicornbay/options/underlying-symbols and split rows from metadata.

        Parameters
        ----------
        query : MpUnicornbayOptionsUnderlyingSymbolsQueryParams
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
        _path = "/mp/unicornbay/options/underlying-symbols"

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
        query: MpUnicornbayOptionsUnderlyingSymbolsQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> (
        list[MpUnicornbayOptionsUnderlyingSymbolsData]
        | AnnotatedResult[list[MpUnicornbayOptionsUnderlyingSymbolsData]]
    ):
        """Type the unpacked rows as MpUnicornbayOptionsUnderlyingSymbolsData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpUnicornbayOptionsUnderlyingSymbolsQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpUnicornbayOptionsUnderlyingSymbolsData] | AnnotatedResult[list[MpUnicornbayOptionsUnderlyingSymbolsData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpUnicornbayOptionsUnderlyingSymbolsData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"meta": {"description": "Pagination and field metadata."}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
