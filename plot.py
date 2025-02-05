import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_prediction_chart(labels, predictions):
    """예측 확률 차트를 생성하여 Streamlit에 표시"""
    st.markdown("### 📊 예측 확률 분포")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(labels, predictions * 100, color="skyblue")
    ax.set_xlabel("확률 (%)", fontsize=12)
    ax.set_ylabel("품종", fontsize=12)
    ax.set_title("품종별 예측 확률", fontsize=16)
    ax.set_xlim(0, 100)

    # ✅ 바 위에 확률값 표시
    for i, v in enumerate(predictions * 100):
        ax.text(v + 1, i, f"{v:.1f}%", color="blue", va="center", fontsize=10)

    st.pyplot(fig)
