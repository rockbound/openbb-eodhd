"""Fetcher for mp.praams.bank.income_statement.isin — generated from spec.

Hits ``https://eodhd.com/api/mp/praams/bank/income_statement/isin/{isin}`` via HTTP GET.
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


class MpPraamsBankIncomeStatementIsinQueryParams(QueryParams):
    """Query parameters for mp.praams.bank.income_statement.isin.

    Parameters
    ----------
    isin : str
        ISIN code (e.g., 'US46625H1005').
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    isin: str = Field(description="ISIN code (e.g., 'US46625H1005').")
    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class MpPraamsBankIncomeStatementIsinData(Data):
    """Response row for mp.praams.bank.income_statement.isin.

    Parameters
    ----------
    date : datetime.date, optional
    net_interest_income : float, optional
    net_income : float, optional
    """

    date: datetime.date | None = Field(default=None, description="")
    net_interest_income: float | None = Field(default=None, description="")
    net_income: float | None = Field(default=None, description="")


class MpPraamsBankIncomeStatementIsinFetcher(
    Fetcher[MpPraamsBankIncomeStatementIsinQueryParams, list[MpPraamsBankIncomeStatementIsinData]]
):
    """Returns bank-specific income statement analysis for the specified ISIN from PRAAMS."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> MpPraamsBankIncomeStatementIsinQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        MpPraamsBankIncomeStatementIsinQueryParams
            Validated query parameters.
        """
        return MpPraamsBankIncomeStatementIsinQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: MpPraamsBankIncomeStatementIsinQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/mp/praams/bank/income_statement/isin/{isin} and split rows from metadata.

        Parameters
        ----------
        query : MpPraamsBankIncomeStatementIsinQueryParams
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
        _path = f"/mp/praams/bank/income_statement/isin/{query.isin}"

        _query_dict = query.model_dump(by_alias=True, exclude={"isin"}, exclude_none=True)
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
        query: MpPraamsBankIncomeStatementIsinQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> (
        list[MpPraamsBankIncomeStatementIsinData]
        | AnnotatedResult[list[MpPraamsBankIncomeStatementIsinData]]
    ):
        """Type the unpacked rows as MpPraamsBankIncomeStatementIsinData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : MpPraamsBankIncomeStatementIsinQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[MpPraamsBankIncomeStatementIsinData] | AnnotatedResult[list[MpPraamsBankIncomeStatementIsinData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [MpPraamsBankIncomeStatementIsinData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {"date": {"format": "date"}}
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
