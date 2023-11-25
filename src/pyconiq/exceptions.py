r"""
Specific exceptions tied to `pyconiq`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any

    from pyconiq.integrations.base import BaseIntegration
    from pyconiq.integrations.base import Transaction


class UnauthorizedError(Exception):
    def __init__(
        self,
        response: dict[str, Any],
        integration: BaseIntegration,
    ) -> None:
        message = (
            f"The merchant {integration.merchant} does not have an API key or the"
            "provided API key is incorrect."
        )

        super().__init__(message)
        self.integration = integration
        self.response = response


class ForbiddenTransactionError(Exception):
    def __init__(
        self,
        response: dict[str, Any],
        integration: BaseIntegration,
    ) -> None:
        self.reason = response.get("code", None)
        match self.reason:
            case "ACCESS_DENIED":
                detail = (
                    f"The merchant {integration.merchant} and the provided"
                    "API key could not be verified or the API key does not"
                    "contain the required authority to access the resource requested"
                )
            case "CALLER_NOT_ALLOWED_TO_CANCEL":
                detail = (
                    f"The merchant {integration.merchant} is not allowed to"
                    "cancel this transaction."
                )
            case _:
                detail = "Unknown authorization error."

        message = f"Forbidden: {self.reason}. {detail}"

        super().__init__(message)
        self.integration = integration
        self.response = response


class UnknownTransactionError(Exception):
    def __init__(
        self,
        response: dict[str, Any],
        transaction: Transaction | str,
    ) -> None:
        transaction_id = (
            transaction.id if isinstance(transaction, Transaction) else transaction
        )
        super().__init__(f"Transaction {transaction_id} could not be found.")
        self.response = response
        self.transaction = transaction_id


class TransactionNotPendingError(Exception):
    def __init__(
        self,
        response: dict[str, Any],
        transaction: Transaction,
    ) -> None:
        super().__init__(
            f"Transaction {transaction.id} could not be cancelled because"
            "the transaction isn't pending."
        )
        self.response = response
        self.transaction = transaction


class RateLimitError(Exception):
    def __init__(self, response: dict[str, Any] | None = None):
        super().__init__()
        self.response = response


class UnknownTransactionStatusError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PayconiqTechnicalError(Exception):
    def __init__(self, response: dict[str, Any] | None = None):
        super().__init__()
        self.response = response


class PayconiqUnavailableError(Exception):
    def __init__(self, response: dict[str, Any] | None = None):
        super().__init__()
        self.response = response
