import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ✅ 모델 및 레이블 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "model", "Lizards.csv")

def display_data_analysis():
    st.title("📊 분석 데이터 보기")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    # ✅ 기존 데이터 로드
    df = load_existing_data()

    if df.empty:
        st.warning("⚠️ 현재 저장된 데이터가 없습니다.")
        return

    # ✅ 데이터 테이블 표시
    st.markdown("### 🔍 저장된 분석 데이터")
    st.dataframe(df)

    # ✅ 종별 분석
    st.markdown("### 📊 품종별 분석")
    species_count = df["Species"].value_counts()
    
    # ✅ 품종 개수 시각화 (막대그래프)
    fig, ax = plt.subplots(figsize=(8, 5))
    species_count.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("도마뱀 품종", fontsize=12)
    ax.set_ylabel("분석된 개수", fontsize=12)
    ax.set_title("품종별 분석 개수", fontsize=16)
    st.pyplot(fig)

    # ✅ 신뢰도 평균 분석
    st.markdown("### 📈 품종별 평균 신뢰도")
    species_confidence = df.groupby("Species")["Confidence"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    species_confidence.plot(kind="barh", ax=ax, color="orange")
    ax.set_xlabel("신뢰도 (%)", fontsize=12)
    ax.set_ylabel("도마뱀 품종", fontsize=12)
    ax.set_title("품종별 평균 신뢰도", fontsize=16)
    st.pyplot(fig)


# ✅ 기존 데이터 로드 함수
def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)

        # ✅ 컬럼 체크
        expected_columns = ["Date", "Image", "Species", "Confidence"]
        if list(df.columns) != expected_columns:
            st.error("❌ CSV 파일의 컬럼 구조가 맞지 않습니다. 데이터를 확인하세요.")
            return pd.DataFrame(columns=expected_columns)

        return df
    else:
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
