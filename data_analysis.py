import os
import pandas as pd
import streamlit as st

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

# ✅ 데이터 분석 및 통계
def display_data_analysis():
    """ 저장된 데이터를 기반으로 분석 결과를 출력하는 함수 """
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    # 기존 데이터 로드
    df = load_existing_data()

    # 데이터가 존재하는 경우만 실행
    if not df.empty:
        st.dataframe(df)

        # ✅ 종별 예측 횟수 시각화
        species_count = df["Species"].value_counts()
        st.bar_chart(species_count)

        # ✅ 신뢰도 평균 시각화
        avg_confidence = df.groupby("Species")["Confidence"].mean()
        st.bar_chart(avg_confidence)
    else:
        st.warning("❌ 데이터가 존재하지 않습니다. 이미지를 분석한 후 다시 확인해주세요.")
