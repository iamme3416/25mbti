import streamlit as st
import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# 제목
st.title("MBTI 국가별 데이터 미리보기")

# 데이터 상위 5줄 표시
st.write("상위 5줄 데이터:")
st.dataframe(df.head())
