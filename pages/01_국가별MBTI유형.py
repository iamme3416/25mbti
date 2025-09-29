import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 제목
st.title("🌍 나라별 MBTI 분포 대시보드")
st.write("나라를 선택하면 MBTI 유형 비율이 예쁘게 나타납니다 ✨")

# 사이드바에서 나라 선택
country = st.sidebar.selectbox("🗺️ 나라 선택", df["Country"].unique())

# 선택한 나라 데이터 필터링
country_data = df[df["Country"] == country].iloc[0, 1:]  # Country 컬럼 제외

# Plotly 막대 그래프
fig = px.bar(
    x=country_data.index,
    y=country_data.values,
    title=f"📊 {country}의 MBTI 분포",
    color=country_data.values,
    color_continuous_scale="Viridis"
)

fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    title_x=0.5
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 비율도 표로 보여주기
st.write("🔍 세부 비율 데이터")
st.dataframe(country_data.reset_index().rename(columns={"index":"MBTI 유형", 0:"비율"}))
