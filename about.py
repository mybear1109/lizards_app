import streamlit as st
import webbrowser

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
    st.write("" * 2)
    st.write("" * 2) 
    st.write("" * 2)    
    st.markdown("""
      ##### 좀더 자세한 설명은 아래를 참고부탁드립니다.🎉         
      """)             
    st.write("" * 2)
    
    # GitHub README 링크를 버튼으로 표시
    st.markdown("[GitHub에서 자세히 보기 🚀](https://github.com/mybear1109/lizards_app/blob/main/README.md)")

        



    st.markdown("""
        -----------------
      """)  
    st.subheader("파충류 AI 탐정: '누구냐 너?' 18종, AI가 밝히는 파충류들의 정체와 비밀 💻")
    st.write("" * 2)
    st.write("" * 2)
    st.image("images/you.png", width=400)
    st.write("" * 2)
    st.markdown("""
        -----------------
      """)  
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
  
    st.markdown("앱 메인 화면에서는 프로젝트 개요 및 이용 가이드를 간단히 확인할 수 있습니다.")
    st.image("images/hompage1.png", use_column_width=True)
    st.write("" * 2)
    st.subheader("📌 2.3 이미지 분석 (AI 분류) 기능")
    st.markdown("""
    1. 메뉴에서 **이미지 분석**을 선택합니다.
    """)
    st.markdown("""
    2. 분석할 **도마뱀 이미지를 업로드**합니다. (`.jpg, .jpeg, .png` 지원)
    """)
    st.image("images/hompage2.png", use_column_width=True)               
    st.markdown("""
    3. AI가 **예측된 종과 확률(%)**을 분석하여 표시합니다.
    """)
    st.image("images/hompage3.png", use_column_width=True)
    st.markdown("""
    4. 추가로 정보를 입력할수 있습니다. 
    """)
    st.image("images/hompage4.png", use_column_width=True)              
    st.write("" * 2)

    st.subheader("📌 2.4 병원 검색 기능")
    st.markdown("""
    1. **병원 검색** 메뉴에서 키워드를 입력합니다. (예: "파충류 병원", "이구아나")
    """)
    st.markdown("""
    2. 관련 병원의 목록이 나타납니다.
    """)
    st.image("images/hompage5.png", use_column_width=True)       
    st.markdown("""
    3. 지도를 통해 위치를 확인할 수도 있습니다.
    """)
    st.image("images/hompage6.png", use_column_width=True)   
    st.write("" * 2)
    st.subheader("📌 2.5 유튜브 검색 기능")
    st.markdown("""
    1. **유튜브 검색** 메뉴에서 키워드를 입력합니다. (예: "파충류 탐험")
    """)
    st.markdown("""
    2. 관련된 유튜브 영상 목록이 나타납니다.
    """)
    st.markdown("""
    3. 제목을 클릭하면 유튜브에서 해당 영상을 바로 확인할 수 있습니다.
    """)
    st.image("images/hompage7.png", use_column_width=True) 
    st.write("" * 2)
    st.write("" * 2)
    st.markdown("""
        -----------------
      """)  
    st.write("" * 2)
    st.header("차별화 포인트 & 질의응답 준비")
    st.write("" * 2)     
    st.markdown("""

    ##### 🔹1. 왜 여러 번 학습을 진행했는가?  
                
    파충류/양서류는 종 간 유사성이 높아 정확도 확보가 쉽지 않습니다.
    반복 학습 + 데이터 증강을 통해 과적합을 피하고, 다양한 특징을 학습시켰습니다.
    실제 촬영 환경(각도, 조명 등)을 고려한 테스트로 일반화 능력을 극대화했습니다.
      """)  
    st.write("" * 2)
    st.markdown("""            
    ##### 🔹2. 기술적 차별점
                
    Teachable Machine을 활용해 빠른 개발과 높은 성능을 함께 달성
    병원검색 + 유튜브 검색을 통합해, 종 분류 후 즉시 정보 탐색이 가능
    단순 분류 도구를 넘어, 정보 허브로 자리 잡을 수 있는 플랫폼
      """)  
    st.write("" * 2)
    st.markdown("""   
    ##### 🔹3. 추가 발전 가능성
                
    커뮤니티 기능(Q&A, 데이터셋 공유)으로 사용자 간 활발한 정보 교류
    보호 단체 협업: 멸종위기종 정보를 추가해 환경 보호에 기여
    오픈소스 프로젝트로 확장해 글로벌 개발자들과 협업

    """)
    st.write("" * 2)
    st.write("" * 2)
    st.warning("### ⚠️ 본 AI 모델은 참고용입니다. 정확한 진단이나 치료는 전문가와 상담하세요!")

  
