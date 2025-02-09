import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_manager import load_existing_data

def display_data_analysis():
    """ 저장된 데이터를 기반으로 분석 결과를 출력하는 함수 """
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    # ✅ 기존 데이터 로드
    df = load_existing_data()
    
    # ✅ 데이터가 없을 경우 메시지 출력
    if df is None or df.empty:
        st.warning("❌ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
        return

    # ✅ 데이터프레임 표시
    st.markdown("### 📋 저장된 분석 데이터")
    st.dataframe(df)

    # ✅ 종별 예측 횟수 시각화
    st.markdown("### 📊 도마뱀 종별 예측 횟수")
    species_count = df["Species"].value_counts().reset_index()
    species_count.columns = ["Species", "Count"]
    st.bar_chart(species_count.set_index("Species"))

    # ✅ 신뢰도 평균 시각화
    st.markdown("### 📈 평균 신뢰도 분석")
    avg_confidence = df.groupby("Species")["Confidence"].mean().reset_index()
    avg_confidence.columns = ["Species", "Avg Confidence"]
    st.bar_chart(avg_confidence.set_index("Species"))

def plot_prediction_chart(labels, predictions):
    """예측 확률 차트를 생성하여 Streamlit에 표시"""
    st.markdown("### 📊 예측 확률 분포")
    
    # ✅ 한글 폰트 깨짐 방지 (Mac, Windows 공통 적용)
    plt.rcParams["font.family"] = "Arial"

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(labels, [p * 100 for p in predictions], color="skyblue")
    ax.set_xlabel("확률 (%)", fontsize=12)
    ax.set_ylabel("품종", fontsize=12)
    ax.set_title("품종별 예측 확률", fontsize=16)
    ax.set_xlim(0, 100)

    # ✅ 바 위에 확률값 표시
    for i, v in enumerate(predictions):
        ax.text(v * 100 + 1, i, f"{v * 100:.1f}%", color="blue", va="center", fontsize=10)

    st.pyplot(fig)
