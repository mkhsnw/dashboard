import streamlit as st 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Proyek Analisis Data")
st.write("**Nama:** Muhammad Khosyi Nawwari")
st.write("**Email:** stsunayoshi977@gmail.com")
st.write("**ID Dicoding:** mkhsnw")

def city_with_highest_sales(data):
    city_order = data.groupby('customer_city').customer_id.nunique().sort_values(ascending=False).head(5)
    return city_order

def highest_order_product(df):
    product_order = df.groupby(by='product_category_name').order_id.nunique().sort_values(ascending=False)
    return product_order

def monthly_sales_trend(data):
    monthly_order = data.resample(rule='M', on='order_purchase_timestamp').agg({
    'order_id': 'nunique',
    "payment_value": 'sum'
    })
    monthly_order.index = monthly_order.index.strftime('%B')
    monthly_order = monthly_order.reset_index()
    return monthly_order

all_df = pd.read_csv('dashboard/all_df.csv')
customers_order_location = pd.read_csv('dashboard/customers_order_location.csv')

datetime_columns = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
all_df.sort_values(by='order_purchase_timestamp', inplace=True)
all_df.reset_index()

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
min_date = all_df['order_purchase_timestamp'].min()
max_date = all_df['order_purchase_timestamp'].max()
with st.sidebar:
    st.write("Data from", min_date, "to", max_date)
    
    start_date,end_date = st.date_input(label="Select Data Range",min_value=min_date,max_value=max_date,value=[min_date,max_date])
    main_df = all_df[(all_df['order_purchase_timestamp'] >= str(start_date)) & (all_df['order_purchase_timestamp'] <= str(end_date))]
    monthly_order = monthly_sales_trend(main_df)
    highest_product = highest_order_product(main_df)
    city_order = city_with_highest_sales(customers_order_location)

st.subheader("Monthly Sales Trend")
st.write(monthly_order)

col1,col2 = st.columns(2)

with col1:
    st.subheader("Most Ordered")
    st.metric("Most Ordered",highest_product.sum())

with col2:
    st.subheader("Total Orders")
    st.metric("Total Revenue", monthly_sales_trend(main_df)['payment_value'].sum())
    
plt.subplots(figsize=(15, 5))
sns.barplot(x=customers_order_location.groupby(by='customer_city').customer_id.nunique().sort_values(ascending=False).head(5).index, y=customers_order_location.groupby(by='customer_city').customer_id.nunique().sort_values(ascending=False).head(5).values)
plt.title("Kota Dengan Penjualan terbanyak", fontsize=20)
plt.show()

st.header("Sales by City")
st.bar_chart(city_order)

st.header("Most Ordered Product")
st.bar_chart(highest_product.head(5))

st.header("Monthly Sales Trend")
st.bar_chart(monthly_order.set_index('order_purchase_timestamp'))


    
    