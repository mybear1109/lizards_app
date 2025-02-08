import streamlit as st

def show_about():
    """앱 소개 페이지"""
    st.title("🦎 파충류 AI 탐정 ")
    st.subheader("Teachable Machine을 활용한 파충류 분류 AI 🏆")
    st.write("" * 2)
    st.markdown("""
        AI 모델을 이용해 총 **18종의 파충류 및 양서류**를 자동으로 분류하고,
                
        병원 검색과 유튜브 검색 기능까지 제공하는 간단하고 편리한 웹 애플리케이션입니다.
                
        자세한 설명은 아래를 참고부탁드립니다.🎉
                
        https://github.com/mybear1109/lizards_app/blob/main/README.md                 
            
    """)
    st.image("images/you.png", use_column_width=True)
    st.write("" * 2)
    st.write("" * 2)
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
    st.write("" * 2)
    st.write("" * 2)
    st.header("2️⃣ 앱 사용 방법 (상세 설명)")
    
    st.subheader("📌 2.1 Streamlit 앱 실행하기")
    st.code("streamlit run app.py", language="bash")

    st.subheader("📌 2.2 메인 화면 살펴보기")
    st.markdown("앱 메인 화면에서는 프로젝트 개요 및 이용 가이드를 간단히 확인할 수 있습니다.")
    st.image("images/hompage.png1", use_column_width=True)
    st.write("" * 2)
    st.subheader("📌 2.3 이미지 분석 (AI 분류) 기능")
    st.markdown("""
    1. 메뉴에서 **이미지 분석**을 선택합니다.
    """)
    st.markdown("""
    2. 분석할 **도마뱀 이미지를 업로드**합니다. (`.jpg, .jpeg, .png` 지원)
    """)
    st.image("images/hompage.png2", use_column_width=True)               
    st.markdown("""
    3. AI가 **예측된 종과 확률(%)**을 분석하여 표시합니다.
    """)
    st.image("images/hompage.png3", use_column_width=True)       
    st.write("" * 2)

    st.subheader("📌 2.4 병원 검색 기능")
    st.markdown("""
    1. **병원 검색** 메뉴에서 키워드를 입력합니다. (예: "파충류 병원", "이구아나")
    """)
    st.markdown("""
    2. 관련 병원의 목록이 나타납니다.
    """)
    st.image("images/hompage.png5", use_column_width=True)       
    st.markdown("""
    3. 지도를 통해 위치를 확인할 수도 있습니다.
    """)
    st.image("images/hompage.png6", use_column_width=True)   
    st.write("" * 2)
    st.subheader("📌 2.5 유튜브 검색 기능")
    st.markdown("""
    1. **유튜브 검색** 메뉴에서 키워드를 입력합니다. (예: "파충류 탐험")
    """)
    st.image("images/you.png", use_column_width=True)
    st.markdown("""
    2. 관련된 유튜브 영상 목록이 나타납니다.
    3. 제목을 클릭하면 유튜브에서 해당 영상을 바로 확인할 수 있습니다.
    """)
    st.image("images/hompage.png6", use_column_width=True) 
    st.write("" * 2)
    st.write("" * 2)  
    st.header("3️⃣ 데이터 및 모델")
    st.markdown("""
    - `Teachable Machine`을 사용해 18가지 파충류/양서류 학습  
                
    - **5회 반복 학습**하여 유사한 종들의 오분류 확률 감소  
                
    - **Epoch=100, Batch=128** 설정으로 다양한 이미지 상황 대응  
    """)

    st.header("4️⃣ 차별화 포인트 & 질의응답 준비")
    st.markdown("""

     - **🔹1. 왜 여러 번 학습을 진행했는가? **  
    파충류/양서류는 종 간 유사성이 높아 정확도 확보가 쉽지 않습니다.
    반복 학습 + 데이터 증강을 통해 과적합을 피하고, 다양한 특징을 학습시켰습니다.
    실제 촬영 환경(각도, 조명 등)을 고려한 테스트로 일반화 능력을 극대화했습니다.
                
                
     - **🔹2. 기술적 차별점
    Teachable Machine을 활용해 빠른 개발과 높은 성능을 함께 달성
    병원 검색 + 유튜브 검색을 통합해, 종 분류 후 즉시 정보 탐색이 가능
    단순 분류 도구를 넘어, 정보 허브로 자리 잡을 수 있는 플랫폼
                

     - **🔹3. 추가 발전 가능성
    커뮤니티 기능(Q&A, 데이터셋 공유)으로 사용자 간 활발한 정보 교류
    보호 단체 협업: 멸종위기종 정보를 추가해 환경 보호에 기여
    오픈소스 프로젝트로 확장해 글로벌 개발자들과 협업

    """)

    st.warning("⚠️ 본 AI 모델은 참고용입니다. 정확한 진단이나 치료는 전문가와 상담하세요!")

    st.success("🦎 새로운 파충류 세계를 탐험해보세요!")
