"""Fetcher for exchanges-list — generated from spec.

Hits ``https://eodhd.com/api/exchanges-list`` via HTTP GET.
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


class ExchangesListQueryParams(QueryParams):
    """Query parameters for exchanges-list.

    Parameters
    ----------
    fmt : Literal['json', 'csv'], optional
        Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv. (default: 'json')
    """

    fmt: Literal["json", "csv"] | None = Field(
        default="json",
        description="Response format. Options are 'json' and 'csv'. Defaults to JSON. Choices: json, csv.",
    )


class ExchangesListData(Data):
    """Response row for exchanges-list.

    Parameters
    ----------
    Name : str, optional
    Code : str, optional
    OperatingMIC : str, optional
    Country : str, optional
    Currency : str, optional
    CountryISO2 : str, optional
    CountryISO3 : str, optional
    """

    Name: str | None = Field(default=None, description="")
    Code: str | None = Field(default=None, description="")
    OperatingMIC: str | None = Field(default=None, description="")
    Country: str | None = Field(default=None, description="")
    Currency: str | None = Field(default=None, description="")
    CountryISO2: str | None = Field(default=None, description="")
    CountryISO3: str | None = Field(default=None, description="")


class ExchangesListFetcher(Fetcher[ExchangesListQueryParams, list[ExchangesListData]]):
    """Retrieve the list of supported exchanges with their details."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> ExchangesListQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        ExchangesListQueryParams
            Validated query parameters.
        """
        return ExchangesListQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: ExchangesListQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/exchanges-list and split rows from metadata.

        Parameters
        ----------
        query : ExchangesListQueryParams
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
        _path = "/exchanges-list"

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
        query: ExchangesListQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[ExchangesListData] | AnnotatedResult[list[ExchangesListData]]:
        """Type the unpacked rows as ExchangesListData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : ExchangesListQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[ExchangesListData] | AnnotatedResult[list[ExchangesListData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [ExchangesListData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
