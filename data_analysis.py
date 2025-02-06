import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_manager import load_existing_data  # ✅ 여기서 데이터 로드

def display_data_analysis():
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    df = load_existing_data()

    if df.empty:
        st.warning("⚠️ 저장된 데이터가 없습니다.")
        return

    st.dataframe(df)

    # ✅ 품종별 분석
    st.markdown("### 🦎 품종별 분석")
    species_counts = df["Species"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(species_counts.index, species_counts.values, color="green")
    ax.set_xlabel("도마뱀 품종")
    ax.set_ylabel("분석 횟수")
    ax.set_title("품종별 예측 분석")
    plt.xticks(rotation=45)
    st.pyplot(fig)
