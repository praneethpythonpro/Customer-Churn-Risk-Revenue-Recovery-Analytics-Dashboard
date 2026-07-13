import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

# -------------------------------
# SETTINGS
# -------------------------------
NUM_CUSTOMERS = 5000
NUM_TRANSACTIONS = 50000

cities = [
    "New York","Chicago","Dallas","Los Angeles",
    "Seattle","Boston","Houston","Miami"
]

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Sports",
    "Beauty",
    "Books",
    "Groceries"
]

payment_methods = [
    "Credit Card",
    "Debit Card",
    "Cash",
    "UPI",
    "PayPal"
]

# -------------------------------
# CUSTOMER TABLE
# -------------------------------

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    join_date = fake.date_between(
        start_date="-5y",
        end_date="-30d"
    )

    customers.append({

        "Customer_ID": customer_id,
        "Name": fake.name(),
        "Age": random.randint(18,70),
        "Gender": random.choice(["Male","Female"]),
        "City": random.choice(cities),
        "Join_Date": join_date,
        "Membership": random.choice(
            ["Bronze","Silver","Gold","Platinum"]
        )

    })

customers_df = pd.DataFrame(customers)

# -------------------------------
# TRANSACTIONS
# -------------------------------

transactions = []

for order_id in range(1, NUM_TRANSACTIONS + 1):

    customer = random.randint(1, NUM_CUSTOMERS)

    category = random.choice(categories)

    quantity = random.randint(1,5)

    price = round(random.uniform(15,800),2)

    discount = random.choice([0,5,10,15,20])

    amount = round(
        quantity * price * (1-discount/100),
        2
    )

    transaction_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    transactions.append({

        "Order_ID": order_id,
        "Customer_ID": customer,
        "Date": transaction_date,
        "Category": category,
        "Quantity": quantity,
        "Unit_Price": price,
        "Discount_%": discount,
        "Amount": amount,
        "Payment_Method": random.choice(payment_methods)

    })

transactions_df = pd.DataFrame(transactions)

# -------------------------------
# SAVE CSV FILES
# -------------------------------

customers_df.to_csv(
    "customers.csv",
    index=False
)

transactions_df.to_csv(
    "transactions.csv",
    index=False
)

print("===================================")
print("DATA GENERATED SUCCESSFULLY")
print("===================================")

print()

print("Customers :", len(customers_df))
print("Transactions :", len(transactions_df))

print()

print(customers_df.head())

print()

print(transactions_df.head())
