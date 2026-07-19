"""Fetcher for user — generated from spec.

Hits ``https://eodhd.com/api/user`` via HTTP GET.
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


class UserQueryParams(QueryParams):
    """Query parameters for user.

    Parameters
    ----------
    fmt : Literal['json'], optional
        Output format. Choices: json. (default: 'json')
    """

    fmt: Literal["json"] | None = Field(
        default="json",
        description="Output format. Choices: json.",
    )


class UserData(Data):
    """Response row for user.

    Parameters
    ----------
    name : str, optional
        User name.
    email : str, optional
        User email.
    subscriptionType : str, optional
        Subscription plan type.
    paymentMethod : str, optional
        Payment method.
    apiRequests : int, optional
        API requests used in current period.
    apiRequestsDate : str, optional
        Date of last API request count reset.
    dailyRateLimit : int, optional
        Daily API request limit.
    """

    name: str | None = Field(default=None, description="User name.")
    email: str | None = Field(default=None, description="User email.")
    subscriptionType: str | None = Field(
        default=None,
        description="Subscription plan type.",
    )
    paymentMethod: str | None = Field(default=None, description="Payment method.")
    apiRequests: int | None = Field(
        default=None,
        description="API requests used in current period.",
    )
    apiRequestsDate: str | None = Field(
        default=None,
        description="Date of last API request count reset.",
    )
    dailyRateLimit: int | None = Field(
        default=None,
        description="Daily API request limit.",
    )


class UserFetcher(Fetcher[UserQueryParams, list[UserData]]):
    """Returns details about the authenticated user, including subscription info and API usage."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> UserQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        UserQueryParams
            Validated query parameters.
        """
        return UserQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: UserQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/user and split rows from metadata.

        Parameters
        ----------
        query : UserQueryParams
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
        _path = "/user"

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
        query: UserQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[UserData] | AnnotatedResult[list[UserData]]:
        """Type the unpacked rows as UserData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : UserQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[UserData] | AnnotatedResult[list[UserData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [UserData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "name": {"description": "User name."},
            "email": {"description": "User email."},
            "subscriptionType": {"description": "Subscription plan type."},
            "paymentMethod": {"description": "Payment method."},
            "apiRequests": {"description": "API requests used in current period."},
            "apiRequestsDate": {"description": "Date of last API request count reset."},
            "dailyRateLimit": {"description": "Daily API request limit."},
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
