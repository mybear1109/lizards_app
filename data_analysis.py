import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ✅ 데이터 파일 경로
DATA_PATH = "data/Lizards.csv"

def display_data_analysis():
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 통계 데이터를 제공합니다.")

    try:
        # ✅ 데이터 로드
        if not DATA_PATH or not pd.io.common.file_exists(DATA_PATH):
            st.warning("⚠️ 저장된 데이터가 없습니다. 이미지를 업로드해 분석을 실행하세요.")
            return

        df = pd.read_csv(DATA_PATH)

        if df.empty:
            st.warning("⚠️ 데이터가 없습니다. 분석을 진행하세요.")
            return

        # ✅ 데이터 요약
        st.markdown("### 📋 데이터 요약")
        st.dataframe(df)

        # ✅ 종별 데이터 집계
        species_counts = df["Species"].value_counts()
        species_confidence_avg = df.groupby("Species")["Confidence"].mean()

        # ✅ Plotly를 사용해 막대 그래프 생성
        st.markdown("### 📊 예측 결과 분포")
        fig = px.bar(
            x=species_confidence_avg.index,
            y=species_confidence_avg.values,
            text=species_confidence_avg.values,
            color=species_confidence_avg.index,
            labels={"x": "Species", "y": "Average Confidence (%)"},
            title="도마뱀 품종별 예측 평균 신뢰도",
            template="plotly_white",
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition="outside")
        fig.update_layout(
            xaxis_title="도마뱀 품종",
            yaxis_title="평균 신뢰도 (%)",
            margin=dict(l=40, r=40, t=40, b=40),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 데이터 분석 중 오류 발생: {e}")
