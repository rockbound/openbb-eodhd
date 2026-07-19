"""Fetcher for cboe.indices — generated from spec.

Hits ``https://eodhd.com/api/cboe/indices`` via HTTP GET.
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


class CboeIndicesQueryParams(QueryParams):
    """Query parameters for cboe.indices.

    Parameters
    ----------
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class CboeIndicesData(Data):
    """Response row for cboe.indices.

    Parameters
    ----------
    code : str, optional
        Index symbol code.
    name : str, optional
        Index name.
    last_value : float, optional
        Latest index value.
    change : float, optional
        Change from previous close.
    change_p : float, optional
        Percentage change.
    last_update : datetime.date, optional
        Date of last update.
    """

    code: str | None = Field(default=None, description="Index symbol code.")
    name: str | None = Field(default=None, description="Index name.")
    last_value: float | None = Field(default=None, description="Latest index value.")
    change: float | None = Field(
        default=None,
        description="Change from previous close.",
    )
    change_p: float | None = Field(default=None, description="Percentage change.")
    last_update: datetime.date | None = Field(
        default=None,
        description="Date of last update.",
    )


class CboeIndicesFetcher(Fetcher[CboeIndicesQueryParams, list[CboeIndicesData]]):
    """Returns a list of all available CBOE indices with their latest values and metadata."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> CboeIndicesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        CboeIndicesQueryParams
            Validated query parameters.
        """
        return CboeIndicesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: CboeIndicesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/cboe/indices and split rows from metadata.

        Parameters
        ----------
        query : CboeIndicesQueryParams
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
        _path = "/cboe/indices"

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
        query: CboeIndicesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[CboeIndicesData] | AnnotatedResult[list[CboeIndicesData]]:
        """Type the unpacked rows as CboeIndicesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : CboeIndicesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[CboeIndicesData] | AnnotatedResult[list[CboeIndicesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [CboeIndicesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "code": {"description": "Index symbol code."},
            "name": {"description": "Index name."},
            "last_value": {"description": "Latest index value."},
            "change": {"description": "Change from previous close."},
            "change_p": {"description": "Percentage change."},
            "last_update": {"description": "Date of last update.", "format": "date"},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
