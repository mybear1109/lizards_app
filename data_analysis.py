import streamlit as st
import pandas as pd
from data_manager import load_existing_data  # ✅ 데이터 로드 함수 가져오기

def display_data_analysis():
    """ 데이터 분석 결과를 화면에 표시 """
    st.title("📊 데이터 분석")
    st.write("저장된 데이터를 바탕으로 분석 결과를 시각화합니다.")

    # ✅ 데이터 로드
    df = load_existing_data()

    if df.empty:
        st.warning("저장된 데이터가 없습니다. 분석을 위해 데이터를 추가하세요.")
    else:
        # ✅ 데이터 표시
        st.dataframe(df)

        # ✅ 분석 요약
        st.markdown("### 🔍 분석 요약")
        st.write(f"총 데이터 수: {len(df)}개")
        st.write(f"분석된 종 수: {df['Species'].nunique()}종")

        # ✅ 종별 데이터 비율
        st.markdown("### 📊 종별 비율")
        species_counts = df["Species"].value_counts(normalize=True) * 100
        st.bar_chart(species_counts)
