import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

customers=pd.read_csv("customers.csv")
transactions=pd.read_csv("transactions.csv")

transactions["Date"]=pd.to_datetime(transactions["Date"])

today=transactions["Date"].max()

rfm=transactions.groupby("Customer_ID").agg(
    Recency=("Date",lambda x:(today-x.max()).days),
    Frequency=("Order_ID","count"),
    Monetary=("Amount","sum")
).reset_index()

# Rule-based labels for training
rfm["Churn"]=(rfm["Recency"]>120).astype(int)

X=rfm[["Recency","Frequency","Monetary"]]
y=rfm["Churn"]

X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.2,random_state=42
)

model=RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train,y_train)

pred=model.predict(X_test)

print("Accuracy:",round(accuracy_score(y_test,pred)*100,2),"%")

rfm["Prediction"]=model.predict(X)
rfm["Risk Score"]=model.predict_proba(X)[:,1]*100

rfm["Risk Level"]=pd.cut(
    rfm["Risk Score"],
    bins=[0,40,70,100],
    labels=["Low","Medium","High"]
)

print("\nTop High-Risk Customers\n")

print(
    rfm.sort_values(
        "Risk Score",
        ascending=False
    ).head(20)
)

rfm.to_csv("customer_churn_predictions.csv",index=False)

print("\nSaved -> customer_churn_predictions.csv")
