import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_manager import load_existing_data

def display_data_analysis():
    """ 저장된 데이터를 기반으로 분석 결과를 출력하는 함수 """
    st.title("📊 데이터 분석")
    st.write("분석된 도마뱀 이미지 데이터를 시각화하고, 예측 확률을 분석합니다.")

    # ✅ 기존 데이터 로드
    df = load_existing_data()

    # ✅ 데이터가 없을 경우 메시지 출력
    if df is None or df.empty:
        st.warning("❌ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
        return

    # ✅ 데이터프레임 표시
    st.markdown("### 📋 저장된 분석 데이터")
    st.dataframe(df)

    # ✅ 종별 평균 예측 확률 분석
    st.markdown("### 📈 종별 평균 예측 확률 (%)")

    # ✅ 종별 평균 확률 계산
    avg_prediction = df.groupby("Species")["Confidence"].mean().reset_index()
    avg_prediction.columns = ["Species", "Avg Confidence"]
    
    # ✅ Matplotlib 그래프 생성
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(avg_prediction["Species"], avg_prediction["Avg Confidence"] * 100, color="royalblue")
    ax.set_xlabel("예측 확률 (%)", fontsize=12)
    ax.set_ylabel("도마뱀 품종", fontsize=12)
    ax.set_title("품종별 평균 예측 확률", fontsize=16)
    ax.set_xlim(0, 100)

    # ✅ 바 위에 확률값 추가
    for i, v in enumerate(avg_prediction["Avg Confidence"]):
        ax.text(v * 100 + 1, i, f"{v * 100:.1f}%", color="black", va="center", fontsize=10)

    st.pyplot(fig)

import streamlit as st
import random
import pandas as pd
import plotly.express as px

# 모프 유전 확률 계산 함수
def calculate_offspring_morph(parent1, parent2):
    # 실제 유전 모델은 더 복잡할 수 있습니다. 이는 간단한 예시입니다.
    if parent1 == parent2:
        return parent1
    else:
        return random.choice([parent1, parent2, "Normal"])

# 스트림릿 앱 시작
st.title("게코 모프 2세 확률 계산기")

# 게코 종류 선택
gecko_type = st.selectbox("게코 종류를 선택하세요", ["6 레오파드 게코(Leopardgeko)", "12 크레스티드 게코(Crestedgeko)"])

# 모프 옵션 설정
if gecko_type == "6 레오파드 게코(Leopardgeko)":
    morph_options = ['Normal(일반)', 'Albino(알비노)', 'Leucistic(루시스틱)', 'Melanistic(멜라니스틱)',
                            'Hypomelanistic(하이포멜라니스틱)', 'Tangerine(탠저린)', 'Carrot Tail(캐럿테일)', 'Blizzard(블리자드)',
                            'Eclipse(이클립스)', 'Jungle(정글)', 'Striped(스트라이프)', 'Banded(밴디드)', 'Patternless(무늬없음)',
                            'Mack Snow(맥 스노우)', 'Super Snow(슈퍼 스노우)', 'Giant(자이언트)', 'Black Night(블랙 나이트)',
                            'Rainwater(레인워터)', 'Typhoon(타이푼)', 'Gem Snow(젬 스노우)', 'Wild Type(야생형)',
                            'Undefined(미정)']
else:
    morph_options = ['Normal(일반)', 'Patternless(무늬없음)', 'Bicolor(바이컬러)', 'Tiger(타이거)',
            'Dalmatian(달마시안)', 'Flame(플레임)', 'Creamsicle(크림시클)', 'Harlequin(할리퀸)',
            'Pinstripe(핀스트라이프)', 'Halloween(할로윈)', 'Quad-Stripe(쿼드-스트라이프)', 'Lilly White(릴리 화이트)',
            'Brindle(브린들)', 'Extreme Harlequin(익스트림 할리퀸)', 'Axanthic(액산틱)', 'Phantom(팬텀)',
            'Tangerine(탠저린)', 'Tri-color(트라이컬러)', 'White Wall/Whiteout(화이트 월/화이트아웃)', 'Drippy(드리피)',
            'Lavender(라벤더)', 'Charcoal(차콜)', 'Cold Fusion(콜드 퓨전)', 'Wild Type(야생형)',
            'Undefined(미정)']

# 부모 모프 선택
parent1 = st.selectbox("부모 1의 모프를 선택하세요", morph_options)
parent2 = st.selectbox("부모 2의 모프를 선택하세요", morph_options)

# 시뮬레이션 실행 버튼
if st.button("2세 확률 계산"):
    # 자손 시뮬레이션
    offspring_count = 1000
    offspring_morphs = [calculate_offspring_morph(parent1, parent2) for _ in range(offspring_count)]
    
    # 결과 집계
    morph_counts = pd.Series(offspring_morphs).value_counts().reset_index()
    morph_counts.columns = ['Morph', 'Count']
    morph_counts['Percentage'] = morph_counts['Count'] / offspring_count * 100
    
    # 결과 표시
    st.write(f"### {offspring_count}마리의 자손 시뮬레이션 결과:")
    
    # 막대 그래프로 시각화
    fig = px.bar(morph_counts, x='Morph', y='Percentage', 
                 text='Percentage', title='예상 자손 모프 분포')
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)
    
    # 상세 결과 표시
    st.write(morph_counts)

st.caption("주의: 이 시뮬레이션은 간단한 모델을 사용하며, 실제 유전 패턴과는 차이가 있을 수 있습니다.")
