import streamlit as st
import pandas as pd
import altair as alt

# CSV 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# MBTI 유형 리스트 (Country 제외)
mbti_types = [col for col in df.columns if col != "Country"]

# 제목
st.title("🌍 MBTI 유형별 상위 10개 국가")
st.write("MBTI 유형을 선택하면, 해당 유형의 비율이 높은 상위 10개 국가가 표시됩니다 🔝")

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
    dx=3  # 글자 위치 조정
).encode(
    text=alt.Text(mbti_choice, format=".3f")
)

# 그래프 출력
st.altair_chart(chart + text, use_container_width=True)

# 데이터 테이블 표시
st.write("📋 데이터 확인")
st.dataframe(top10.reset_index(drop=True))
