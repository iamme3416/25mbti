import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

# CSV 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# MBTI 유형 리스트 (Country 제외)
mbti_types = [col for col in df.columns if col != "Country"]

# 제목
st.title("🌍 MBTI 유형별 상위 10개 국가 + 지도 시각화")
st.write("MBTI 유형을 선택하면 상위 10개 국가와 세계 지도가 표시됩니다 🗺️✨")

# 사이드바에서 MBTI 유형 선택
mbti_choice = st.sidebar.selectbox("🔎 MBTI 유형 선택", mbti_types)

# 선택한 MBTI 유형 기준 상위 10개 국가
top10 = df[["Country", mbti_choice]].sort_values(by=mbti_choice, ascending=False).head(10)

# Altair 막대 그래프
chart = (
    alt.Chart(top10)
    .mark_bar(color="teal")
    .encode(
        x=alt.X(mbti_choice, title="비율"),
        y=alt.Y("Country", sort="-x", title="국가"),
        tooltip=["Country", mbti_choice]
    )
    .properties(
        title=f"🏆 {mbti_choice} 비율이 높은 상위 10개 국가",
        width=600,
        height=400
    )
)

# 값 라벨 추가
text = chart.mark_text(
    align="left",
    baseline="middle",
    dx=3
).encode(
    text=alt.Text(mbti_choice, format=".3f")
)

st.altair_chart(chart + text, use_container_width=True)

# ---------------- 지도 시각화 ----------------
world = data.world_110m.url

# 지도 데이터와 국가 매칭
map_chart = (
    alt.Chart(world)
    .mark_geoshape(stroke="black", strokeWidth=0.5)
    .encode(
        color=alt.Color(mbti_choice, scale=alt.Scale(scheme="viridis"), title="비율"),
        tooltip=["Country", mbti_choice]
    )
    .transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(df, "Country", [mbti_choice])
    )
    .project("naturalEarth1")
    .properties(
        title=f"🗺️ 전 세계 {mbti_choice} 분포",
        width=700,
        height=400
    )
)

st.altair_chart(map_chart, use_container_width=True)

# 데이터 테이블 표시
st.write("📋 데이터 확인")
st.dataframe(top10.reset_index(drop=True))
