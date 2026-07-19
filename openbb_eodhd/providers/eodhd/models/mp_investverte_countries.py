"""Fetcher for mp.investverte.countries — generated from spec.

Hits ``https://eodhd.com/api/mp/investverte/countries`` via HTTP GET.
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


class MpInvestverteCountriesQueryParams(QueryParams):
    """Query parameters for mp.investverte.countries.

    Parameters
    ----------
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpInvestverteCountriesData(Data):
    """Response row for mp.investverte.countries.

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
    num_companies : int, optional
        Number of rated companies in country.
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
    num_companies: int | None = Field(
        default=None,
        description="Number of rated companies in country.",
    )


class MpInvestverteCountriesFetcher(
    Fetcher[MpInvestverteCountriesQueryParams, list[MpInvestverteCountriesData]]
):
    """Returns a list of all countries with their aggregate ESG scores from Investverte."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpInvestverteCountriesQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpInvestverteCountriesQueryParams
            Validated query parameters.
        """
        return MpInvestverteCountriesQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpInvestverteCountriesQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/investverte/countries and split rows from metadata.

        Parameters
        ----------
        query : MpInvestverteCountriesQueryParams
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
        _path = "/mp/investverte/countries"

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
        query: MpInvestverteCountriesQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpInvestverteCountriesData] | AnnotatedResult[list[MpInvestverteCountriesData]]:
        """Type the unpacked rows as MpInvestverteCountriesData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpInvestverteCountriesQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpInvestverteCountriesData] | AnnotatedResult[list[MpInvestverteCountriesData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpInvestverteCountriesData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "country": {"description": "Country name."},
            "country_code": {"description": "ISO country code."},
            "esg_score": {"description": "Overall ESG score."},
            "environmental_score": {"description": "Environmental pillar score."},
            "social_score": {"description": "Social pillar score."},
            "governance_score": {"description": "Governance pillar score."},
            "num_companies": {"description": "Number of rated companies in country."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
