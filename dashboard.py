import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NovaMart Analytics",layout="wide")

customers=pd.read_csv("customers.csv")
transactions=pd.read_csv("transactions.csv")

transactions["Date"]=pd.to_datetime(transactions["Date"])
transactions["Month"]=transactions["Date"].dt.to_period("M").astype(str)

df=transactions.merge(customers,on="Customer_ID")

revenue=df["Amount"].sum()
orders=len(df)
customers_count=df["Customer_ID"].nunique()
aov=revenue/orders

st.title("📊 NovaMart Retail Analytics Dashboard")

c1,c2,c3,c4=st.columns(4)
c1.metric("Revenue",f"${revenue:,.0f}")
c2.metric("Orders",orders)
c3.metric("Customers",customers_count)
c4.metric("Avg Order",f"${aov:,.2f}")

st.divider()

left,right=st.columns(2)

with left:
    monthly=df.groupby("Month")["Amount"].sum().reset_index()
    fig=px.line(monthly,x="Month",y="Amount",markers=True,title="Monthly Revenue")
    st.plotly_chart(fig,use_container_width=True)

with right:
    cat=df.groupby("Category")["Amount"].sum().reset_index()
    fig=px.bar(cat,x="Category",y="Amount",title="Revenue by Category")
    st.plotly_chart(fig,use_container_width=True)

left,right=st.columns(2)

with left:
    city=df.groupby("City")["Amount"].sum().reset_index().sort_values("Amount",ascending=False)
    fig=px.bar(city,x="City",y="Amount",color="Amount",title="Revenue by City")
    st.plotly_chart(fig,use_container_width=True)

with right:
    pay=df.groupby("Payment_Method")["Amount"].sum().reset_index()
    fig=px.pie(pay,names="Payment_Method",values="Amount",title="Payment Methods")
    st.plotly_chart(fig,use_container_width=True)

left,right=st.columns(2)

with left:
    top=df.groupby("Customer_ID")["Amount"].sum().nlargest(10).reset_index()
    fig=px.bar(top,x="Customer_ID",y="Amount",title="Top 10 Customers")
    st.plotly_chart(fig,use_container_width=True)

with right:
    mem=df.groupby("Membership")["Customer_ID"].count().reset_index(name="Count")
    fig=px.pie(mem,names="Membership",values="Count",title="Membership Distribution")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Top Transactions")
st.dataframe(
    df[["Order_ID","Customer_ID","Category","City","Amount","Payment_Method"]]
    .sort_values("Amount",ascending=False)
    .head(20),
    use_container_width=True
)

st.subheader("Business Insights")

best=df.groupby("Category")["Amount"].sum().idxmax()
city=df.groupby("City")["Amount"].sum().idxmax()
payment=df.groupby("Payment_Method")["Amount"].sum().idxmax()

st.success(f"""
• Total Revenue: ${revenue:,.2f}

• Best Performing Category: {best}

• Highest Revenue City: {city}

• Most Used Payment Method: {payment}

• Average Order Value: ${aov:,.2f}

• Total Customers: {customers_count:,}
""")
