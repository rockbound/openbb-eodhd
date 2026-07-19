"""Fetcher for internal-user — generated from spec.

Hits ``https://eodhd.com/api/internal-user`` via HTTP GET.
"""

import datetime
from typing import Any, Literal

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.helpers import get_async_requests_session, get_querystring
from pydantic import BaseModel, Field, field_validator

from ....utils import safe_json_loads, unpack_response


class InternalUserQueryParams(QueryParams):
    """Query parameters for internal-user."""

    pass


class InternalUserDataAvailableMarketplaceDataFeeds(BaseModel):
    """Marketplace API usage and subscription details. These have a separate request counter from the standard APIs.

    Parameters
    ----------
    dailyRateLimit : int, optional
        Daily request limit for marketplace subscriptions.
    requestsSpent : int, optional
        Number of marketplace API requests made during the current counting period.
    timeToReset : str, optional
        Time remaining until the marketplace API request counter resets.
    subscriptions : list[str], optional
        List of marketplace subscriptions available to the user.
    """

    dailyRateLimit: int | None = Field(
        default=None,
        description="Daily request limit for marketplace subscriptions.",
    )
    requestsSpent: int | None = Field(
        default=None,
        description="Number of marketplace API requests made during the current counting period.",
    )
    timeToReset: str | None = Field(
        default=None,
        description="Time remaining until the marketplace API request counter resets.",
    )
    subscriptions: list[str] | None = Field(
        default=None,
        description="List of marketplace subscriptions available to the user.",
    )


class InternalUserData(Data):
    """Response row for internal-user.

    Parameters
    ----------
    name : str, optional
        Full name of the user.
    email : str, optional
        Registered email address.
    subscriptionType : Literal['monthly', 'yearly'], optional
        Type of subscription plan. Choices: monthly, yearly.
    paymentMethod : str, optional
        Payment processor used for the subscription (e.g., Stripe, PayPal).
    apiRequests : int, optional
        Number of API requests made during the current counting period.
    apiRequestsDate : datetime.date, optional
        Date for which the API request count applies.
    dailyRateLimit : int, optional
        Daily request limit for standard API usage.
    extraLimit : int, optional
        Extra daily request limit granted to the user.
    inviteToken : str, optional
        Referral invite token, if available.
    inviteTokenClicked : int, optional
        Number of times the invite token link was clicked.
    subscriptionMode : Literal['paid', 'free', 'trial'], optional
        Current subscription mode. Choices: paid, free, trial.
    availableDataFeeds : list[str], optional
        List of data feeds included in the subscription.
    availableMarketplaceDataFeeds : InternalUserDataAvailableMarketplaceDataFeeds, optional
        Marketplace API usage and subscription details. These have a separate request counter from the standard APIs. Inner fields: dailyRateLimit (int), requestsSpent (int), timeToReset (str), subscriptions (list[str]).
    """

    name: str | None = Field(default=None, description="Full name of the user.")
    email: str | None = Field(default=None, description="Registered email address.")
    subscriptionType: Literal["monthly", "yearly"] | None = Field(
        default=None,
        description="Type of subscription plan. Choices: monthly, yearly.",
    )
    paymentMethod: str | None = Field(
        default=None,
        description="Payment processor used for the subscription (e.g., Stripe, PayPal).",
    )
    apiRequests: int | None = Field(
        default=None,
        description="Number of API requests made during the current counting period.",
    )
    apiRequestsDate: datetime.date | None = Field(
        default=None,
        description="Date for which the API request count applies.",
    )
    dailyRateLimit: int | None = Field(
        default=None,
        description="Daily request limit for standard API usage.",
    )
    extraLimit: int | None = Field(
        default=None,
        description="Extra daily request limit granted to the user.",
    )
    inviteToken: str | None = Field(
        default=None,
        description="Referral invite token, if available.",
    )
    inviteTokenClicked: int | None = Field(
        default=None,
        description="Number of times the invite token link was clicked.",
    )
    subscriptionMode: Literal["paid", "free", "trial"] | None = Field(
        default=None,
        description="Current subscription mode. Choices: paid, free, trial.",
    )
    availableDataFeeds: list[str] | None = Field(
        default=None,
        description="List of data feeds included in the subscription.",
    )
    availableMarketplaceDataFeeds: InternalUserDataAvailableMarketplaceDataFeeds | None = Field(
        default=None,
        description="Marketplace API usage and subscription details. These have a separate request counter from the standard APIs. Inner fields: dailyRateLimit (int), requestsSpent (int), timeToReset (str), subscriptions (list[str]).",
    )

    @field_validator("availableMarketplaceDataFeeds", mode="before")
    @classmethod
    def _empty_list_to_none(cls, v: Any) -> Any:
        """Coerce `[]` to None."""
        return None if v == [] else v


class InternalUserFetcher(Fetcher[InternalUserQueryParams, list[InternalUserData]]):
    """Fetch detailed internal account information for the authenticated user, including subscription type, usage statistics, and available data feeds. Requires a valid `api_token` as a query parameter."""

    @staticmethod
    def transform_query(params: dict[str, Any]) -> InternalUserQueryParams:
        """Validate raw input into typed query parameters.

        Parameters
        ----------
        params : dict[str, Any]
            Raw user input (CLI flags / API body).

        Returns
        -------
        InternalUserQueryParams
            Validated query parameters.
        """
        return InternalUserQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: InternalUserQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch from https://eodhd.com/api/internal-user and split rows from metadata.

        Parameters
        ----------
        query : InternalUserQueryParams
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
        _path = "/internal-user"

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
        query: InternalUserQueryParams,
        data: dict[str, Any],
        **kwargs: Any,
    ) -> list[InternalUserData] | AnnotatedResult[list[InternalUserData]]:
        """Type the unpacked rows as InternalUserData; surface metadata via AnnotatedResult.

        Parameters
        ----------
        query : InternalUserQueryParams
            The validated query (unused but provided).
        data : dict[str, Any]
            Output of ``aextract_data``.
        **kwargs : Any
            Forwarded by the provider runtime; unused.

        Returns
        -------
        list[InternalUserData] | AnnotatedResult[list[InternalUserData]]
            Typed rows; wrapped in ``AnnotatedResult`` when the response carried metadata alongside the data array.
        """
        _typed = [InternalUserData(**row) for row in data["rows"]]
        _metadata = dict(data.get("metadata") or {})
        _column_metadata = {
            "name": {"description": "Full name of the user."},
            "email": {"description": "Registered email address.", "format": "email"},
            "subscriptionType": {"description": "Type of subscription plan."},
            "paymentMethod": {
                "description": "Payment processor used for the subscription (e.g., Stripe, PayPal)."
            },
            "apiRequests": {
                "description": "Number of API requests made during the current counting period."
            },
            "apiRequestsDate": {
                "description": "Date for which the API request count applies.",
                "format": "date",
            },
            "dailyRateLimit": {"description": "Daily request limit for standard API usage."},
            "extraLimit": {"description": "Extra daily request limit granted to the user."},
            "inviteToken": {"description": "Referral invite token, if available."},
            "inviteTokenClicked": {
                "description": "Number of times the invite token link was clicked."
            },
            "subscriptionMode": {"description": "Current subscription mode."},
            "availableDataFeeds": {
                "description": "List of data feeds included in the subscription."
            },
            "availableMarketplaceDataFeeds": {
                "description": "Marketplace API usage and subscription details. These have a separate request counter from the standard APIs."
            },
        }
        _metadata.setdefault("columns", _column_metadata)
        if _metadata:
            return AnnotatedResult(result=_typed, metadata=_metadata)
        return _typed
