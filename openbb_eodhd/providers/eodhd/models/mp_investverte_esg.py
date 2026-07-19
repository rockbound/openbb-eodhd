"""Fetcher for mp.investverte.esg — generated from spec.

Hits ``https://eodhd.com/api/mp/investverte/esg/{symbol}`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import Field, field_validator

from ....utils import safe_json_loads, unpack_response


class MpInvestverteEsgQueryParams(QueryParams):
    """Query parameters for mp.investverte.esg.

    Parameters
    ----------
    symbol : str
        Ticker symbol (e.g., 'AAPL.US').
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    symbol: str = Field(description="Ticker symbol (e.g., 'AAPL.US').")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpInvestverteEsgData(Data):
    """Response row for mp.investverte.esg.

    Parameters
    ----------
    symbol : str, optional
        Ticker symbol.
    name : str, optional
        Company name.
    esg_score : float, optional
        Overall ESG score.
    esg_rating : str, optional
        ESG rating grade (e.g., 'A', 'BBB', 'CCC').
    environmental_score : float, optional
        Environmental pillar score.
    social_score : float, optional
        Social pillar score.
    governance_score : float, optional
        Governance pillar score.
    environmental_details : dict[str, Any], optional
        Detailed environmental metrics.
    social_details : dict[str, Any], optional
        Detailed social metrics.
    governance_details : dict[str, Any], optional
        Detailed governance metrics.
    last_updated : datetime.date, optional
        Date of last rating update.
    """

    symbol: str | None = Field(default=None, description="Ticker symbol.")
    name: str | None = Field(default=None, description="Company name.")
    esg_score: float | None = Field(default=None, description="Overall ESG score.")
    esg_rating: str | None = Field(
        default=None,
        description="ESG rating grade (e.g., 'A', 'BBB', 'CCC').",
    )
    environmental_score: float | None = Field(
        default=None,
        description="Environmental pillar score.",
    )
    social_score: float | None = Field(default=None, description="Social pillar score.")
    governance_score: float | None = Field(
        default=None,
        description="Governance pillar score.",
    )
    environmental_details: dict[str, Any] | None = Field(
        default=None,
        description="Detailed environmental metrics.",
    )
    social_details: dict[str, Any] | None = Field(
        default=None,
        description="Detailed social metrics.",
    )
    governance_details: dict[str, Any] | None = Field(
        default=None,
        description="Detailed governance metrics.",
    )
    last_updated: datetime.date | None = Field(
        default=None,
        description="Date of last rating update.",
    )

    @field_validator("environmental_details", "social_details", "governance_details", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class MpInvestverteEsgFetcher(Fetcher[MpInvestverteEsgQueryParams, list[MpInvestverteEsgData]]):
    """Returns detailed ESG ratings and scores for a specific company from Investverte."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpInvestverteEsgQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpInvestverteEsgQueryParams
            Validated query parameters.
        """
        return MpInvestverteEsgQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpInvestverteEsgQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/investverte/esg/{symbol} and split rows from metadata.

        Parameters
        ----------
        query : MpInvestverteEsgQueryParams
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
        _path = f"/mp/investverte/esg/{query.symbol}"

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
        query: MpInvestverteEsgQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[MpInvestverteEsgData] | AnnotatedResult[list[MpInvestverteEsgData]]:
        """Type the unpacked rows as MpInvestverteEsgData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpInvestverteEsgQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpInvestverteEsgData] | AnnotatedResult[list[MpInvestverteEsgData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpInvestverteEsgData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "symbol": {"description": "Ticker symbol."},
            "name": {"description": "Company name."},
            "esg_score": {"description": "Overall ESG score."},
            "esg_rating": {"description": "ESG rating grade (e.g., 'A', 'BBB', 'CCC')."},
            "environmental_score": {"description": "Environmental pillar score."},
            "social_score": {"description": "Social pillar score."},
            "governance_score": {"description": "Governance pillar score."},
            "environmental_details": {"description": "Detailed environmental metrics."},
            "social_details": {"description": "Detailed social metrics."},
            "governance_details": {"description": "Detailed governance metrics."},
            "last_updated": {"description": "Date of last rating update.", "format": "date"},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
