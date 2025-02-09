import streamlit as st
import pandas as pd
import plotly.express as px
import random

# ✅ display_data_analysis 함수를 직접 정의
def display_data_analysis():
    """ 저장된 데이터를 기반으로 분석 결과를 출력하는 함수 """
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 예측 확률을 분석합니다.")

    # ✅ 기존 데이터 로드
    df = pd.read_csv("data/morph_2.csv")  # 실제 데이터 로드 방식 확인 필요

    if df is not None and not df.empty:
        # ✅ 데이터 표시
        st.markdown("### 📋 저장된 분석 데이터")
        st.dataframe(df)

        # ✅ 종별 평균 예측 확률 분석
        st.markdown("### 📈 종별 평균 예측 확률 (%)")
        avg_prediction = df.groupby("Species")["Confidence"].mean().reset_index()
        avg_prediction.columns = ["Species", "Avg Confidence"]

        # ✅ 시각화
        fig_prob = px.bar(avg_prediction, x='Species', y='Avg Confidence', text='Avg Confidence',
                          title='종별 평균 예측 확률', labels={'Avg Confidence': '예측 확률 (%)'})
        fig_prob.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_prob)
    else:
        st.warning("❌ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")

    # ✅ 기존 데이터 분석 실행
    df = pd.read_csv("data/morph_2.csv")


# ✅ 게코 모프 유전 확률 계산기
st.title("🦎 게코 모프 2세 확률 계산기")

# ✅ 게코 종류 선택
gecko_type = st.selectbox("게코 종류를 선택하세요", ["레오파드 게코", "크레스티드 게코"])

# ✅ 모프 옵션 설정
if gecko_type == "레오파드 게코":
    morph_options = ['Normal', 'Albino', 'Leucistic', 'Melanistic', 'Hypomelanistic', 'Tangerine', 'Carrot Tail', 'Blizzard',
                     'Eclipse', 'Jungle', 'Striped', 'Banded', 'Patternless', 'Mack Snow', 'Super Snow', 'Giant', 'Black Night',
                     'Rainwater', 'Typhoon', 'Gem Snow', 'Wild Type', 'Undefined']
else:
    morph_options = ['Normal', 'Patternless', 'Bicolor', 'Tiger', 'Dalmatian', 'Flame', 'Harlequin', 'Pinstripe']

# ✅ 부모 모프 선택
parent1 = st.selectbox("부모 1의 모프를 선택하세요", morph_options)
parent2 = st.selectbox("부모 2의 모프를 선택하세요", morph_options)

# ✅ 모프 유전 확률 계산 함수
def calculate_offspring_morph(parent1, parent2):
    if parent1 == parent2:
        return parent1
    else:
        return random.choice([parent1, parent2, "Normal"])

# ✅ 시뮬레이션 실행
if st.button("2세 확률 계산"):
    offspring_count = 1000
    offspring_morphs = [calculate_offspring_morph(parent1, parent2) for _ in range(offspring_count)]
    
    morph_counts = pd.Series(offspring_morphs).value_counts().reset_index()
    morph_counts.columns = ['Morph', 'Count']
    morph_counts['Percentage'] = morph_counts['Count'] / offspring_count * 100
    
    # ✅ 결과 시각화
    st.write(f"### {offspring_count}마리의 자손 시뮬레이션 결과:")
    fig = px.bar(morph_counts, x='Morph', y='Percentage', text='Percentage', title='예상 자손 모프 분포')
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig)
    
    # ✅ 상세 결과 표시
    st.write(morph_counts)

st.caption("📌 이 시뮬레이션은 단순한 모델을 기반으로 하며, 실제 유전 패턴과 차이가 있을 수 있습니다.")
