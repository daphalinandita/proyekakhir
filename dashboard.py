import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_sum_product_df(df): 
    sum_product_df = all_data.groupby("product_category_name").product_weight_g.sum().sort_values(ascending=False).reset_index()
    return sum_product_df

def create_monthly_review_df(df): 
    monthly_review_df = all_data.resample(rule='M', on='review_creation_date').agg({
        "order_id": "nunique",
        "review_score": "mean"
        })
    monthly_review_df = monthly_review_df.reset_index()
    monthly_review_df.rename(columns={
        "order_id": "order_count",
        "review_score": "review_mean"
        }, inplace=True)
    return monthly_review_df

all_data = pd.read_csv("https://raw.githubusercontent.com/daphalinandita/proyekakhir/main/all_data.csv")

st.title(
"""
Data Analysis
"""
)

st.header("""User's Review""")
monthly_review_df = pd.read_csv("https://raw.githubusercontent.com/daphalinandita/proyekakhir/main/all_data.csv")
fig , ax = plt.subplots( figsize = (20 , 8))
ax.bar(x = monthly_review_df.review_comment_message ,height = monthly_review_df.review_score)
ax.set_xlabel("Comment")
ax.set_ylabel("Review")
st.pyplot(fig)

st.write(
"""
These data shows the average reviews on each months.

"""
)

st.header("""Most Weight Products""")
sum_product_df = pd.read_csv("https://raw.githubusercontent.com/daphalinandita/proyekakhir/main/all_data.csv")
fig1 , axis = plt.subplots( figsize = (20 , 8))
axis.bar(x = sum_product_df.product_category_name  ,height = sum_product_df.product_weight_g)
axis.set_xlabel("Products")
axis.set_ylabel("Weight")
st.pyplot(fig1)


st.write(
"""
These data shows the top 5 heaviest products.

"""
)

