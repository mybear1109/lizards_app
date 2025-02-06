import os
import pandas as pd
import datetime
import streamlit as st  # ✅ Streamlit 모듈 추가
import matplotlib.pyplot as plt  # ✅ 데이터 시각화를 위한 Matplotlib 추가

# ✅ 데이터 파일 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "model", "Lizards.csv")

# ✅ 데이터 분석 페이지
def display_data_analysis():
    st.title("📊 도마뱀 이미지 분석 데이터")
    
    # ✅ 기존 데이터 로드
    df = load_existing_data()

    if df.empty:
        st.warning("⚠️ 저장된 데이터가 없습니다. 먼저 이미지를 분석하세요!")
        return

    # ✅ 데이터 미리보기
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df)

    # ✅ 품종별 데이터 개수 시각화
    st.subheader("📊 품종별 분석 개수")
    species_counts = df["Species"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    species_counts.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_xlabel("도마뱀 품종")
    ax.set_ylabel("분석 횟수")
    ax.set_title("품종별 분석 데이터 분포")
    st.pyplot(fig)

# ✅ 분석 결과 저장 함수
def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    
    try:
        # ✅ 저장 경로가 존재하지 않으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Species": [species],
            "Confidence": [confidence]
        })

        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 컬럼이 올바른지 확인
            expected_columns = ["Date", "Image", "Species", "Confidence"]
            if list(existing_data.columns) != expected_columns:
                st.error("❌ 기존 데이터 컬럼이 올바르지 않습니다. CSV 파일을 확인하세요.")
                return

            # ✅ 데이터 추가 후 저장
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_csv(DATA_PATH, index=False)
        st.success("✅ 데이터 저장 완료!")

    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")

# ✅ 기존 데이터 로드 함수
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
            return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
