import streamlit as st
import pandas as pd
import os

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"

# ✅ 기존 데이터 불러오기 함수
def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)

            # ✅ 컬럼 체크
            expected_columns = ["Date", "Image", "Species", "Confidence"]
            if list(df.columns) != expected_columns:
                st.error("❌ CSV 파일의 컬럼 구조가 맞지 않습니다. 데이터를 확인하세요.")
                return pd.DataFrame(columns=expected_columns)

            return df
        else:
            st.warning("⚠️ 저장된 데이터가 없습니다.")
            return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])

# ✅ 데이터 분석 및 시각화
def display_data_analysis():
    """ 저장된 데이터를 기반으로 분석 결과를 출력하는 함수 """
    df = load_existing_data()

    if not df.empty:
        st.dataframe(df)

        # ✅ 종별 예측 횟수 시각화
        species_count = df["Species"].value_counts()
        st.bar_chart(species_count)

        # ✅ 신뢰도 평균 시각화
        avg_confidence = df.groupby("Species")["Confidence"].mean()
        st.bar_chart(avg_confidence)

        st.success("📊 분석 데이터가 성공적으로 로드되었습니다.")
    else:
        st.warning("❌ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
