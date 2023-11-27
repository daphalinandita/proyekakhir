import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_sum_product_df(df): 
    sum_product_df = product_df.groupby("product_category_name").product_weight_g.sum().sort_values(ascending=False).reset_index()
    return sum_product_df

def create_monthly_review_df(df): 
    monthly_review_df = review_df.resample(rule='M', on='review_creation_date').agg({
        "order_id": "nunique",
        "review_score": "mean"
        })
    monthly_review_df = monthly_review_df.reset_index()
    monthly_review_df.rename(columns={
        "order_id": "order_count",
        "review_score": "review_mean"
        }, inplace=True)
    return monthly_review_df

# Load cleaned data
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["review_creation_date", "review_answer_timestamp"]
all_df.sort_values(by="review_creation_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["review_creation_date"].min()
max_date = all_df["review_creation_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["review_creation_date"] >= str(start_date)) & 
                (all_df["review_creation_date"] <= str(end_date))]

# Menyiapkan berbagai dataframe
sum_product_df = create_sum_product_df(main_df)
monthly_review_df = create_monthly_review_df(main_df)

st.header('The Shop Collection Dashboard :sparkles:')
st.subheader('Average Reviews per Month')
 
col1 = st.columns(1)
 
with col1:
    total_orders = monthly_review_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_review_df["review_creation_date"],
    monthly_review_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#data 2
st.subheader("5 Most Heaviest Products")

fig, ax = plt.subplots(nrows=1, figsize=(24, 6))

colors = ["#B996CB", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_weight_g", y="product_category_name", data=sum_product_df.head(5), palette=colors)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Heaviest Products", loc="center", fontsize=18)
ax.tick_params(axis ='y', labelsize=15)

plt.show()