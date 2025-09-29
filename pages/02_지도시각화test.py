import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("your_data.csv")  # 파일명 변경 필요

df = load_data()

st.title("🌍 나라별 MBTI 데이터 시각화")
st.write("나라를 선택하면 상위 10개 MBTI 분포와 지도에서 해당 국가 위치를 볼 수 있어요.")

# 나라 선택
countries = df['Country'].unique()
selected_country = st.selectbox("나라 선택 ✨", countries)

# 선택된 나라 데이터 필터링
country_data = df[df['Country'] == selected_country]

# MBTI별 상위 10개
top10 = (
    country_data.groupby("MBTI")["Count"]  # Count 컬럼명은 실제 데이터에 맞게 수정
    .sum()
    .reset_index()
    .sort_values("Count", ascending=False)
    .head(10)
)

st.subheader(f"📊 {selected_country} MBTI 상위 10 유형")

bar_chart = (
    alt.Chart(top10)
    .mark_bar(color="#6C63FF")
    .encode(
        x=alt.X("Count:Q", title="비율/개수"),
        y=alt.Y("MBTI:N", sort="-x", title="MBTI 유형"),
        tooltip=["MBTI", "Count"]
    )
    .properties(width=600, height=400)
)

st.altair_chart(bar_chart)

# 지도 시각화
st.subheader("🗺 나라 위치 지도")

# 나라별 평균 좌표 (위도, 경도 컬럼 필요)
if "Latitude" in df.columns and "Longitude" in df.columns:
    map_data = df.groupby("Country")[["Latitude", "Longitude"]].mean().reset_index()
    fig = px.scatter_geo(
        map_data,
        lat="Latitude",
        lon="Longitude",
        text="Country",
        projection="natural earth",
        title="국가별 위치",
    )
    # 선택된 나라 강조
    highlight = map_data[map_data["Country"] == selected_country]
    fig.add_scattergeo(
        lat=highlight["Latitude"],
        lon=highlight["Longitude"],
        text=highlight["Country"],
        mode="markers+text",
        marker=dict(size=15, color="red"),
        name="선택된 나라"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ 지도 표시를 위해 데이터에 Latitude/Longitude 컬럼이 필요합니다.")
