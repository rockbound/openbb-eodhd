"""Fetcher for mp.investverte.companies — generated from spec.

Hits ``https://eodhd.com/api/mp/investverte/companies`` via HTTP GET.
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


class MpInvestverteCompaniesQueryParams(QueryParams):
    """Query parameters for mp.investverte.companies.

    Parameters
    ----------
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpInvestverteCompaniesData(Data):
    """Response row for mp.investverte.companies.

    Parameters
    ----------
    symbol : str, optional
        Ticker symbol.
    name : str, optional
        Company name.
    country : str, optional
        Country of domicile.
    sector : str, optional
        Business sector.
    industry : str, optional
        Industry classification.
    """

    symbol: str | None = Field(default=None, description="Ticker symbol.")
    name: str | None = Field(default=None, description="Company name.")
    country: str | None = Field(default=None, description="Country of domicile.")
    sector: str | None = Field(default=None, description="Business sector.")
    industry: str | None = Field(default=None, description="Industry classification.")


class MpInvestverteCompaniesFetcher(
    Fetcher[MpInvestverteCompaniesQueryParams, list[MpInvestverteCompaniesData]]
):
    """Returns a list of all companies with ESG ratings available from Investverte."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpInvestverteCompaniesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpInvestverteCompaniesQueryParams
            Validated query parameters.
        """
        return MpInvestverteCompaniesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpInvestverteCompaniesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/investverte/companies and split rows from metadata.

        Parameters
        ----------
        query : MpInvestverteCompaniesQueryParams
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
        _path = "/mp/investverte/companies"

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
        query: MpInvestverteCompaniesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpInvestverteCompaniesData] | AnnotatedResult[list[MpInvestverteCompaniesData]]:
        """Type the unpacked rows as MpInvestverteCompaniesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpInvestverteCompaniesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpInvestverteCompaniesData] | AnnotatedResult[list[MpInvestverteCompaniesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpInvestverteCompaniesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "symbol": {"description": "Ticker symbol."},
            "name": {"description": "Company name."},
            "country": {"description": "Country of domicile."},
            "sector": {"description": "Business sector."},
            "industry": {"description": "Industry classification."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
