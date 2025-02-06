import os
import pandas as pd
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"

def display_data_analysis():
    """데이터 분석 페이지를 스트림릿 UI에서 표시하는 함수"""
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고 통계 데이터를 제공합니다.")

    # 기존 데이터 불러오기
    df = load_existing_data()

    if df.empty:
        st.warning("⚠️ 저장된 데이터가 없습니다. 먼저 이미지를 업로드하여 분석 데이터를 생성하세요.")
        return

    # ✅ 데이터 테이블 표시
    st.markdown("### 🔍 저장된 분석 데이터")
    st.dataframe(df)

    # ✅ 데이터 통계 요약
    st.markdown("### 📊 데이터 통계 요약")
    st.write(df.describe())

    # ✅ 종별 분석
    species_count = df["Species"].value_counts()
    st.bar_chart(species_count)


def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            return df
        except Exception as e:
            st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
            return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
    else:
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
