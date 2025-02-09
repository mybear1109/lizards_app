import streamlit as st
import webbrowser
import os

def show_about():
    """앱 소개 페이지"""
    st.title("🦎 파충류 AI 탐정 ")
    st.subheader("Teachable Machine을 활용한 파충류 분류 AI 🏆")

    st.write("" * 2)
    st.write("" * 2)
    st.markdown("""
      ##### **단순 분류를 넘어선 종합 정보 플랫폼의 진화🧠**
                
      **🔬 고성능 AI 분류**
                
      Teachable Machine으로 학습된 AI 모델이 18종의 파충류와 양서류를 정확하게 식별

      **⚡ 신속한 개발 & 우수한 성능**
                
      Teachable Machine의 직관적 인터페이스로 빠른 개발과 높은 분류 정확도 동시 달성

      **🔍 원스톱 통합 정보 검색**
                
      종 분류 후 즉시 관련 병원 정보와 유튜브 영상 검색 가능

      **📚 교육 및 연구 지원**
                
      애호가, 학생, 초보자들을 위한 귀중한 학습 및 연구 도구

      **🚀 확장 가능한 플랫폼**
                
      18종에서 시작, 더 많은 정보가 추가 가능한 유연한 구조

    """)

    # ✅ GitHub 버튼 추가 (새 창에서 열기)
    github_url = "https://github.com/mybear1109/lizards_app/blob/main/README.md"
    if st.button("GitHub에서 자세히 보기 🚀"):
        webbrowser.open_new_tab(github_url)

    st.markdown("""---""")  

    # ✅ 이미지 파일 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    image_path = os.path.join(base_dir, "images", "you.png")

    # ✅ 이미지 파일이 존재하면 표시
    if os.path.exists(image_path):
        st.image(image_path, width=400)
    else:
        st.warning(f"⚠️ 이미지 파일을 찾을 수 없습니다: {image_path}")

    st.markdown("""---""")  
    st.header("1️⃣ 주요 기능 한눈에 보기")
    st.markdown("""
    - **📸 이미지 분석 (AI 분류)**  
                
      업로드된 이미지를 AI 모델로 분석해 가장 유사한 종을 예측  
                
      예측 확률과 함께 결과를 시각화  

    - **🏥 병원 검색**  
                
      특수동물을 진료하는 병원을 찾아 지도 위에서 확인  
                
      원하는 키워드를 입력해 검색  

    - **📺 유튜브 검색**  
                
      파충류와 양서류 관련 영상을 유튜브에서 찾아보기 
                 
      허용된 키워드를 사용해 불필요한 콘텐츠를 최소화  
    """)

    st.markdown("""---""")  
    st.header("2️⃣ 앱 사용 방법 (상세 설명)")

    # ✅ 이미지가 정상적으로 로드되는지 확인 후 표시
    homepage_images = ["hompage1.png", "hompage2.png", "hompage3.png", "hompage4.png", "hompage5.png", "hompage6.png", "hompage7.png"]
    for img in homepage_images:
        img_path = os.path.join(base_dir, "images", img)
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"⚠️ 이미지 파일을 찾을 수 없습니다: {img_path}")

    st.markdown("""---""")  
    st.header("차별화 포인트 & 질의응답 준비")
    st.write("" * 2)     
    st.markdown("""
    ##### 🔹1. 왜 여러 번 학습을 진행했는가?  
                
    파충류/양서류는 종 간 유사성이 높아 정확도 확보가 쉽지 않습니다.
    반복 학습 + 데이터 증강을 통해 과적합을 피하고, 다양한 특징을 학습시켰습니다.
    실제 촬영 환경(각도, 조명 등)을 고려한 테스트로 일반화 능력을 극대화했습니다.
      """)

    st.markdown("""            
    ##### 🔹2. 기술적 차별점
                
    - **Teachable Machine**을 활용해 빠른 개발과 높은 성능을 함께 달성
    - **병원 검색 + 유튜브 검색**을 통합하여, 종 분류 후 즉시 정보 탐색 가능
    - 단순 분류 도구를 넘어, **정보 허브**로 자리 잡을 수 있는 플랫폼
      """)

    st.markdown("""   
    ##### 🔹3. 추가 발전 가능성
                
    - **커뮤니티 기능** (Q&A, 데이터셋 공유)으로 사용자 간 활발한 정보 교류
    - **보호 단체 협업:** 멸종위기종 정보를 추가해 환경 보호에 기여
    - **오픈소스 프로젝트**로 확장해 글로벌 개발자들과 협업

    """)

    st.warning("### ⚠️ 본 AI 모델은 참고용입니다. 정확한 진단이나 치료는 전문가와 상담하세요!")
