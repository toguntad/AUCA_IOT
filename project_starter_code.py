import random
import time
import uuid
from datetime import datetime, timedelta

# Generate a large pool of users (up to 100,000)
USERS = [f"User{i}" for i in range(1, 100001)]
BANKS = ["BankA", "BankB", "BankC", "BankD"]

# Transaction types: deposit, withdrawal, transfer
TRANSACTION_TYPES = ["deposit", "withdrawal", "transfer"]

# Fraud scenarios for injection
FRAUD_SCENARIOS = [
    "multiple_transactions_in_short_time",
    "large_amount_transfer",
    "frequent_transfers_between_same_accounts"
]

# Initialize each user's balance with a random starting value
USER_BALANCES = {user: random.uniform(100, 10000) for user in USERS}

def generate_transaction(sender=None, receiver=None, fraud_type=None, timestamp=None):
    """
    Generate a transaction and optionally inject specific sender/receiver or fraud patterns.
    """
    transaction_id = str(uuid.uuid4())
    transaction_type = random.choice(TRANSACTION_TYPES) if not fraud_type else "transfer"
    
    sender = sender or random.choice(USERS)
    available_balance = USER_BALANCES[sender]

    if transaction_type == "withdrawal":
        receiver = sender
        amount = round(random.uniform(10, min(available_balance, 1000)), 2)
        USER_BALANCES[sender] -= amount
    elif transaction_type == "deposit":
        receiver = receiver or random.choice(BANKS)
        amount = round(random.uniform(10, 1000), 2)
        USER_BALANCES[sender] += amount
    else:  # transfer
        receiver = receiver or random.choice([user for user in USERS if user != sender])
        amount = round(random.uniform(10, min(available_balance, 1000)), 2)
        USER_BALANCES[sender] -= amount
        USER_BALANCES[receiver] += amount

    timestamp = timestamp or datetime.now()

    return {
        "transaction_id": transaction_id,
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "transaction_type": transaction_type,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }

def inject_fraud(base_transaction, transactions_per_minute):
    """
    Inject fraudulent behavior by creating multiple transactions for certain fraud scenarios.
    """
    fraud_type = random.choice(FRAUD_SCENARIOS)
    fraudulent_transactions = [base_transaction]
    
    if fraud_type == "multiple_transactions_in_short_time":
        for _ in range(random.randint(3, 5)):
            timestamp = datetime.strptime(base_transaction["timestamp"], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=random.randint(1, 30))
            fraudulent_transactions.append(generate_transaction(base_transaction["sender"], timestamp=timestamp))
    
    elif fraud_type == "large_amount_transfer":
        base_transaction["amount"] = round(random.uniform(10000, 100000), 2)
    
    elif fraud_type == "frequent_transfers_between_same_accounts":
        for _ in range(random.randint(3, 5)):
            timestamp = datetime.strptime(base_transaction["timestamp"], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=random.randint(5, 30))
            fraudulent_transactions.append(generate_transaction(base_transaction["sender"], base_transaction["sender"], timestamp=timestamp))
    
    return fraudulent_transactions

def transaction_stream(transactions_per_minute=60, total_time_minutes=10, fraud_probability=0.05):
    """
    Generate a continuous stream of transactions with configurable transactions per minute.
    Inject fraud patterns based on a probability.
    """
    total_transactions = transactions_per_minute * total_time_minutes
    delay_between_transactions = 60.0 / transactions_per_minute
    start_time = datetime.now()

    for _ in range(total_transactions):
        current_time = start_time + timedelta(seconds=_ * delay_between_transactions)
        
        if random.random() < fraud_probability:
            base_transaction = generate_transaction(timestamp=current_time)
            transactions = inject_fraud(base_transaction, transactions_per_minute)
        else:
            transactions = [generate_transaction(timestamp=current_time)]
        
        for transaction in transactions:
            # Output all transactions in the same format
            print(transaction, "\n")
        
        time.sleep(delay_between_transactions)

if __name__ == "__main__":
    transactions_per_minute = 120
    total_time_minutes = 10
    fraud_probability = 0.1

    transaction_stream(transactions_per_minute, total_time_minutes, fraud_probability)