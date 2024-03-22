import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")

# Carregamento dos dados
df = pd.read_csv("relatorio_vendas.csv", sep=";", decimal=",", encoding='latin1')
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Adição da coluna 'Month' para filtragem por mês
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Menu lateral para seleção do mês
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtragem dos dados pelo mês selecionado
df_filtered = df[df["Month"] == month]

# Layout da página em colunas, duas superiores, três inferiores
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico de barras para faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico de barras para faturamento por tipo de produto
fig_prod = px.bar(df_filtered, y="Product line", x="Total",
                  color="City", title="Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico de barras para faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                   title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico de pizza para faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                   title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Gráfico de barras para avaliação média por cidade
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_total, y="Rating", x="City",
                   title="Avaliação média por cidade")
col5.plotly_chart(fig_rating, use_container_width=True)