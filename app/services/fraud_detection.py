import datetime
from typing import Dict, List, Tuple

class FraudDetectionSystem:
    def __init__(self):
        self.transaction_history: Dict[str, List[Dict]] = {}
        self.flagged_transactions: List[Dict] = []

    def add_transaction(self, user_id: str, amount: float, timestamp: datetime.datetime, merchant: str) -> None:
        """Add a new transaction to the user's history."""
        if user_id not in self.transaction_history:
            self.transaction_history[user_id] = []
        
        transaction = {
            "amount": amount,
            "timestamp": timestamp,
            "merchant": merchant
        }
        self.transaction_history[user_id].append(transaction)

    def check_transaction(self, user_id: str, amount: float, timestamp: datetime.datetime, merchant: str) -> Tuple[bool, str]:
        """Check if a transaction is potentially fraudulent."""
        is_fraudulent = False
        reason = ""

        # Rule 1: Check for unusually large transactions
        if amount > 1000:
            is_fraudulent = True
            reason = "Unusually large transaction amount"

        # Rule 2: Check for rapid succession of transactions
        if user_id in self.transaction_history:
            recent_transactions = [t for t in self.transaction_history[user_id] 
                                   if (timestamp - t['timestamp']).total_seconds() < 300]
            if len(recent_transactions) > 3:
                is_fraudulent = True
                reason = "Too many transactions in a short time"

        # Rule 3: Check for transactions from unusual locations (simplified)
        if user_id in self.transaction_history:
            usual_merchants = set(t['merchant'] for t in self.transaction_history[user_id][-10:])
            if merchant not in usual_merchants and len(usual_merchants) > 5:
                is_fraudulent = True
                reason = "Transaction from unusual merchant"

        if is_fraudulent:
            self.flag_transaction(user_id, amount, timestamp, merchant, reason)

        return is_fraudulent, reason

    def flag_transaction(self, user_id: str, amount: float, timestamp: datetime.datetime, merchant: str, reason: str) -> None:
        """Flag a transaction as potentially fraudulent."""
        flagged_transaction = {
            "user_id": user_id,
            "amount": amount,
            "timestamp": timestamp,
            "merchant": merchant,
            "reason": reason
        }
        self.flagged_transactions.append(flagged_transaction)

    def get_flagged_transactions(self) -> List[Dict]:
        """Return all flagged transactions."""
        return self.flagged_transactions

# Example usage
if __name__ == "__main__":
    fds = FraudDetectionSystem()

    # Add some normal transactions
    fds.add_transaction("user1", 100, datetime.datetime.now(), "Amazon")
    fds.add_transaction("user1", 50, datetime.datetime.now(), "Walmart")
    fds.add_transaction("user1", 75, datetime.datetime.now(), "Target")

    # Check a normal transaction
    is_fraud, reason = fds.check_transaction("user1", 200, datetime.datetime.now(), "Best Buy")
    print(f"Transaction fraudulent: {is_fraud}, Reason: {reason}")

    # Check a large transaction
    is_fraud, reason = fds.check_transaction("user1", 2000, datetime.datetime.now(), "Electronics Store")
    print(f"Transaction fraudulent: {is_fraud}, Reason: {reason}")

    # Check rapid succession of transactions
    for _ in range(5):
        is_fraud, reason = fds.check_transaction("user1", 10, datetime.datetime.now(), "Coffee Shop")
        print(f"Transaction fraudulent: {is_fraud}, Reason: {reason}")

    # Check transaction from unusual merchant
    is_fraud, reason = fds.check_transaction("user1", 500, datetime.datetime.now(), "Foreign Online Store")
    print(f"Transaction fraudulent: {is_fraud}, Reason: {reason}")

    # Print all flagged transactions
    print("\nFlagged Transactions:")
    for transaction in fds.get_flagged_transactions():
        print(transaction)