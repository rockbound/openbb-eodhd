"""Fetcher for mp.investverte.country — generated from spec.

Hits ``https://eodhd.com/api/mp/investverte/country/{symbol}`` via HTTP GET.
"""

from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field

from ....utils import safe_json_loads, unpack_response


class MpInvestverteCountryQueryParams(QueryParams):
    """Query parameters for mp.investverte.country.

    Parameters
    ----------
    symbol : str
        Country code (e.g., 'US', 'GB', 'DE').
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    symbol: str = Field(description="Country code (e.g., 'US', 'GB', 'DE').")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpInvestverteCountryDataTopCompaniesItem(BaseModel):
    """MpInvestverteCountryDataTopCompaniesItem.

    Parameters
    ----------
    symbol : str, optional
    name : str, optional
    esg_score : float, optional
    """

    symbol: str | None = Field(default=None, description="")
    name: str | None = Field(default=None, description="")
    esg_score: float | None = Field(default=None, description="")


class MpInvestverteCountryDataSectorBreakdownItem(BaseModel):
    """MpInvestverteCountryDataSectorBreakdownItem.

    Parameters
    ----------
    sector : str, optional
    avg_esg_score : float, optional
    num_companies : int, optional
    """

    sector: str | None = Field(default=None, description="")
    avg_esg_score: float | None = Field(default=None, description="")
    num_companies: int | None = Field(default=None, description="")


class MpInvestverteCountryData(Data):
    """Response row for mp.investverte.country.

    Parameters
    ----------
    country : str, optional
        Country name.
    country_code : str, optional
        ISO country code.
    esg_score : float, optional
        Overall ESG score.
    environmental_score : float, optional
        Environmental pillar score.
    social_score : float, optional
        Social pillar score.
    governance_score : float, optional
        Governance pillar score.
    top_companies : list[MpInvestverteCountryDataTopCompaniesItem], optional
        Top ESG-rated companies in this country. Inner item fields: symbol (str), name (str), esg_score (float).
    sector_breakdown : list[MpInvestverteCountryDataSectorBreakdownItem], optional
        ESG scores by sector within this country. Inner item fields: sector (str), avg_esg_score (float), num_companies (int).
    """

    country: str | None = Field(default=None, description="Country name.")
    country_code: str | None = Field(default=None, description="ISO country code.")
    esg_score: float | None = Field(default=None, description="Overall ESG score.")
    environmental_score: float | None = Field(
        default=None,
        description="Environmental pillar score.",
    )
    social_score: float | None = Field(default=None, description="Social pillar score.")
    governance_score: float | None = Field(
        default=None,
        description="Governance pillar score.",
    )
    top_companies: list[MpInvestverteCountryDataTopCompaniesItem] | None = Field(
        default=None,
        description="Top ESG-rated companies in this country. Inner item fields: symbol (str), name (str), esg_score (float).",
    )
    sector_breakdown: list[MpInvestverteCountryDataSectorBreakdownItem] | None = Field(
        default=None,
        description="ESG scores by sector within this country. Inner item fields: sector (str), avg_esg_score (float), num_companies (int).",
    )


class MpInvestverteCountryFetcher(
    Fetcher[MpInvestverteCountryQueryParams, list[MpInvestverteCountryData]]
):
    """Returns detailed ESG scores and metrics for a specific country from Investverte."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpInvestverteCountryQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpInvestverteCountryQueryParams
            Validated query parameters.
        """
        return MpInvestverteCountryQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpInvestverteCountryQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/investverte/country/{symbol} and split rows from metadata.

        Parameters
        ----------
        query : MpInvestverteCountryQueryParams
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
        _path = f"/mp/investverte/country/{query.symbol}"

        _query_dict = query.model_dump(by_alias=True, exclude={"symbol"}, exclude_none=True)
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
        query: MpInvestverteCountryQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpInvestverteCountryData] | AnnotatedResult[list[MpInvestverteCountryData]]:
        """Type the unpacked rows as MpInvestverteCountryData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpInvestverteCountryQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpInvestverteCountryData] | AnnotatedResult[list[MpInvestverteCountryData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpInvestverteCountryData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "country": {"description": "Country name."},
            "country_code": {"description": "ISO country code."},
            "esg_score": {"description": "Overall ESG score."},
            "environmental_score": {"description": "Environmental pillar score."},
            "social_score": {"description": "Social pillar score."},
            "governance_score": {"description": "Governance pillar score."},
            "top_companies": {"description": "Top ESG-rated companies in this country."},
            "sector_breakdown": {"description": "ESG scores by sector within this country."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
