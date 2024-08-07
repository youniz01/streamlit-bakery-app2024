import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as plt

def load_data():
    file = 'bakerysales.csv'
    df = pd.read_csv(file)
    df.rename(columns={'Unnamed: 0':'id','article': 'product', 'Quantity':'quantity'},
           inplace =True)
    df.unit_price = df.unit_price.str.replace(",",".").str.replace("€", "").str.strip()
    type(df.unit_price[0])
    df.unit_price = df.unit_price.astype('float')

    # calculate sales
    df['sales'] = df.quantity * df.unit_price
    # drop columns with zero sales
    df.drop(df[df.sales == 0].index, inplace=True)
    # convert date column to date format
    df['date'] = pd.to_datetime(df.date)
    return df


    return df.head(100)



# load the data set
df = load_data()

# app title
st.title("Bakery sales App")

# display the table
# st.dataframe(df.head(50))
products = df['product'].unique()
selected_product = st.sidebar.multiselect(
                    "Choose Product",
                    products,
                    [products[0],
                    products[2]
                    ])
filtered_table = df[df['product'].isin(selected_product)]

# display metrics
total_sales = 0
if len(filtered_table) > 0:
    total_sales = filtered_table['sales'].sum()
else:
    total_sales = df.sales.sum()

total_qty = df.quantity.sum()
total_no_transactions = df.id.count()

st.subheader("Calculations")
col1, col2, col3, = st.columns(3)

col1.metric("No of Transactions", total_no_transactions)
col2.metric("Total Quantity", total_qty)
col3.metric("Total Sales", total_sales)

# end of metrics
# select and display specific products
# add filters


# display the filtered table
st.dataframe(filtered_table[["date","product","quantity","unit_price","sales"]])

# chart 
try:
   st.write("## Total sales of selected product")
   bar1 = filtered_table.groupby(['product'])['sales'].sum().sort_values(ascending=True)
   st.bar_chart(bar1)
except ValueError as e:
   st.error(
      """ Error: """ % e.reason 
   )

# sales analysis
try:
   daily_sales = df.groupby('date')['sales'].sum()
   daily_sales_df = daily_sales.reset_index().rename(columns={'sales':"total sales"})
   st.area_cahrt = daily_sales_df.plot(x='date',
                         y='total sales')
except ValueError as e:
    st.error(
        """ Error: """ % e.reason
    )