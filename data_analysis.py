import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_manager import load_existing_data  # ✅ 기존 데이터 불러오기

# ✅ 데이터 분석 UI 함수
def display_data_analysis():
    """ 데이터 분석 및 시각화 """
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    # ✅ 기존 데이터 불러오기
    df = load_existing_data()

    if df.empty:
        st.warning("⚠️ 저장된 데이터가 없습니다.")
        return

    # ✅ 데이터 테이블 출력
    st.dataframe(df)

    # ✅ 품종별 분석 (가장 많이 예측된 품종)
    st.markdown("### 🔎 가장 많이 예측된 품종")
    species_count = df["Species"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(species_count.index, species_count.values, color="skyblue")
    ax.set_xlabel("도마뱀 품종")
    ax.set_ylabel("예측된 횟수")
    ax.set_title("가장 많이 예측된 도마뱀 품종")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ✅ 신뢰도 평균 분석
    st.markdown("### 🔍 평균 신뢰도 분석")
    avg_confidence = df.groupby("Species")["Confidence"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(avg_confidence.index, avg_confidence.values, color="lightcoral")
    ax.set_xlabel("도마뱀 품종")
    ax.set_ylabel("평균 신뢰도 (%)")
    ax.set_title("품종별 평균 신뢰도")
    plt.xticks(rotation=45)
    st.pyplot(fig)
