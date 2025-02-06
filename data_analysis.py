import streamlit as st
from data_manager import load_existing_data

def display_data_analysis():
    """ 저장된 데이터를 기반으로 분석 결과를 출력하는 함수 """
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    # ✅ 기존 데이터 로드
    df = load_existing_data()

    # ✅ 데이터가 없을 경우 메시지 출력
    if df.empty:
        st.warning("❌ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
        return

    # ✅ 데이터프레임 표시
    st.markdown("### 📋 저장된 분석 데이터")
    st.dataframe(df)

    # ✅ 종별 예측 횟수 시각화
    st.markdown("### 📊 도마뱀 종별 예측 횟수")
    species_count = df["Species"].value_counts()
    st.bar_chart(species_count)

    # ✅ 신뢰도 평균 시각화
    st.markdown("### 📈 평균 신뢰도 분석")
    avg_confidence = df.groupby("Species")["Confidence"].mean()
    st.bar_chart(avg_confidence)
