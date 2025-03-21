# 🦎  "파충류 AI 탐정" : Teachable Machine을 활용한 파충류 분류 AI  🏆 

<br>

---
## **✨ 프로젝트 소개**

###  " 파충류 AI 탐정: '누구냐 너?' 15종, AI가 밝히는 파충류들의 정체와 비밀 💻"

<br>



<img src="https://github.com/user-attachments/assets/c7092f83-4064-4cc6-b4ea-79df032e6296" width="60%" height="auto">
<br>



---




### [🖥️ HOME PAGE](https://lizardsapp-gbr4mdxzrsw7ngzbkhk4pc.streamlit.app/)



---

## 💡 기획 의도

<br>

![발표 메인](https://github.com/user-attachments/assets/b409d493-8183-409e-9f01-a0653d709a74)
<br>
<br>


### 1. **⚒️ 실용성과 편의성**
    - 이미지 분류 + 병원 검색 + 유튜브 영상 검색을 **한 플랫폼**에서 해결
    - 긴급한 상황에도 **신속하게** 주변 병원 찾기 가능
    - 최근 사육 기록 앱(렙다이어리 등)과 **차별화**된 종합 서비스

### 2. **📚 교육 및 연구 혁신**
    - 학교·박물관 등에서 **AI 기반 파충류·양서류 분류 체험**
    - 유튜브 영상과 결합해 **흥미로운 교육 자료**로 활용
    - **생물학 연구** 분야에서도 **선구자적 역할** 기대

### 3. **🗂️ 모프 정보 수집 및 교배 예측**
    - 레오파드 게코, 볼파이톤처럼 **색·무늬 변이(모프)**가 다양한 종에 적용
    - **데이터 축적**을 통해 2세대 형질 예측 가능
    - **전문 브리더 및 연구자**에게 귀중한 정보 제공

### 4. **🗄️ 지속적인 발전 및 확장성**
    - 15종에서 더 확장해 다른 동물군(포유류, 조류 등)에도 적용 가능
    - 실시간 스트리밍 분석, 사용자 커뮤니티 기능 등 구현 여지
    - **환경 보호**와 **멸종위기종** 식별에도 기여 가능

### 5. **🧮 파충류 관련 산업 진흥**
    - 파충류 O2O 플랫폼과 연계해 애완용품 시장 활성화
    - **AI 기술을 활용한 건강 관리 서비스** 확장 (예: 탈피 과정
---

## 모프(morph)란?

Polymorphism 단어에서 파생되었으며 다형성이라는 뜻을 가지고 있습니다. 다형성이란, 같은 종의 생물이지만 모습이나 고유한 특징이 다양한 성질을 말합니다. 
예를 들어, 펫테일 게코라는 같은 도마뱀 종류더라도 모프에 따라서 색깔과 무늬, 패턴 이 등이 다른 생김새를 가지게 됩니다.

![모프이미지](https://github.com/user-attachments/assets/fc3e8972-de02-4519-b981-9304805be8c7)
<br>
<br>
<br>
<br>


---
## **📂 프로젝트 구조**

- [skill] 부모 도마뱀의 각 유전자 값을 입력하는 페이지 입니다.세분화된 파일 구성으로 각 기능이 모듈화되어 있습니다.
<br>

```bash

project_root/
├── __pycache__/
├── .git/
├── data/
├── icons/
├── image/
├── model/
├── test_image/
├── .gitignore
├── lisards.ipynb
├── README.md
├── requirements.txt
├── about.py              # 앱에 대한 설명
├── app.py                # Streamlit 메인 애플리케이션
├── data_analysis.py      # 데이터 시각화
├── data_manager.py       # 데이터및 이미지 저장
├── hospital_page.py      # 병원 검색 기능
├── image_analysis.py     # 이미지 분석(AI 모델) 기능
├── sidebar.py            # 사이드바 UI
├── species_info.py       # 종별 상세 설명
├── youtube_page.py       # 유튜브 검색 기능


```

---

## **⚙️ 기술 스택**

> 다양한 기술과 API를 활용하여 효율적이고 정확한 애플리케이션을 개발했습니다.

<br>

| **기술/라이브러리** | **역할** |
| --- | --- |
| 🧠 **Teachable Machine** | AI 기반 15종 파충류/양서류 분류 모델 구축 |
| 💻 **Streamlit** | Python 기반 웹 애플리케이션 프레임워크 |
| 📊 **Pandas, NumPy** | 데이터 처리 및 전처리 |
| 📈 **Matplotlib, Seaborn, Plotly** | 데이터 시각화 및 통계 차트 생성 |
| 🎥 **YouTube API** | 파충류 관련 영상 검색 |
| 🗺️ **병원 검색 API** | 네이버/구글 병원 데이터 연계 및 정확도 향상 |
| 📝 **블로그(네이버) 데이터 연계** | 병원 정보의 신뢰도 향상을 위한 추가 데이터 사용 |


<br>
<br>
<br>
<br>

---
## **🌟 주요 특징**

### 풍부한 데이터 기반 AI 모델

- Kaggle의 **Reptiles and Amphibians Dataset** + 국내 애완 파충류 시장 정보(**The Breeders**)를 결합
- **야생 생태계**와 **애완 시장** 데이터를 모두 반영하여 **데이터 다양성** 극대화
- 초기 **9종**에서 **15종**으로 확장하면서 **뱀, 이구아나, 양서류**까지 포함


### 금액 예측에서 이미지 분류로의 전환 (도전과 혁신)

- 초기에는 **파충류 금액 예측 모델**(R² = 0.27) 시도
- 가격 결정 요인이 **비정형적**이고, 데이터도 **부족**함을 인지
- **문제 해결**을 위해 **이미지 분류 모델**로 과감히 전환
- 오히려 **종 식별**에 초점을 맞춰 **실용적 가치**를 높임
<br>
<br>
<br>

### 확장성과 다양성

- 애완 파충류뿐 아니라 **야생 파충류·양서류**까지 수용
- **지속적인 데이터 확장**을 통해 모델 정확도 및 범용성 개선
- 차후 **다른 동물군**으로도 확장이 가능해 **무궁무진한 발전 가능성** 보유
<br>
<br>
<br>

---

## **🏆 애플리케이션 기능**

<br>

## 이미지 분석 (AI 기반 분류)

#### Teachable Machine 으로 이미지의 종과 활률을 표시하게 됩니다. 
<br>

#### 이미지를 업로드하게되면 
![이미지 분석1](https://github.com/user-attachments/assets/47a1c8dc-9741-45c6-9791-245f36b75f0b)
<br>

## 1. **이미지 업로드 → 종 분류**

 - AI 모델이 업로드된 이미지를 분석하여, 가장 유사한 종과 예측 확률(%)을 표시
 - 학교·박물관 등에서 **AI 기반 파충류·양서류 분류 체험** 대리 경험 가능 


   
![이미지 분석2](https://github.com/user-attachments/assets/83b23642-9bf8-44d4-894c-047cf67cd069)
<br>

## 2. **모프(morph) 정보 수집**


- 사용자가 레오파드 게코(Leopardgeko)와 크레스티드 게코(Crestedgeko) 각각
![이미지 분석3](https://github.com/user-attachments/assets/592d37a9-0508-43eb-8689-af8ded6622c0)
![이미지 분석4](https://github.com/user-attachments/assets/a6047ef7-7bfe-479c-a5d4-f6b6099ae163)
<br>
  
- **모프** 정보를 추가 입력하면 데이터베이스에 축적
- 교배 시 **2세대 특성**을 어느 정도 예측할 수 있는 기반 마련
  
    
![이미지 분석5](https://github.com/user-attachments/assets/44f24050-e7df-44b7-82c9-9b8354ab5cc7)
 
## 3. **주의 문구**
- 결과는 참고용이며, 실제 종 확인이 필요한 경우 전문가 진단 권장

### 파충류 병원 검색
  <br>     
  <br>

## 1. **특수동물 병원 찾기**

  <br>   
  
- 일반 동물병원은 많지만, 특수동물 병원은 적어 찾기가 어려운 현실 보완
- **네이버/구글 API** + **블로그** 데이터를 종합해 **정확도** 향상

![파충류 병원 검색](https://github.com/user-attachments/assets/a3421090-7b40-4f05-9e5b-2cc05732c194)
<br>  
<br>   



## 2. **지도 연동 및 상세 정보**
<br>   
  
- 주소, 전화번호, 운영시간 등 **바로 확인**
- “파충류”, “도마뱀”, “뱀”, “거북”, “양서류” 등 **허용 키워드** 검색
    
<br>   
   
![지도 연동 및 상세 정보6](https://github.com/user-attachments/assets/d59c0b4d-ebfd-42bb-99c1-dca84a4c8d19)
<br>   
<br> 
<br>   
## 유튜브 검색 기능 <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" />   

<br>   
### 1. **영상 학습**
<br>   

- 파충류 사육법, 질병 예방, 서식 환경 개선 등 **유익한 영상** 검색
- **클릭 시** 유튜브로 연결되어 **바로 시청** 가능
    
   <br>
   

 ![영상 학습](https://github.com/user-attachments/assets/1c05ed88-f5ce-40d3-8802-bf4f079c3d4c)



### 2. **콘텐츠 관련성 강화**


- 특정 키워드(“파충류”, “이구아나” 등)로 검색 범위를 제한하여 효율적 정보 탐색
  
   <br>


  
### 3. **초보 사육자 지원**

 - 올바른 사육법, 안전하게 키우는 방법 등을 쉽게 습득

<br>
<br>

---
## 👀 차별화 포인트 & 질의응답 준비
<br>


### 1. **왜 7번이나 학습을 진행했는가?**
<br>

- 파충류/양서류는 **종 간 유사성**이 높아 정확도 확보가 쉽지 않습니다.
- **반복 학습 + 데이터 증강**을 통해 **과적합**을 피하고, **다양한 특징**을 학습시켰습니다.
- 실제 촬영 환경(각도, 조명 등)을 고려한 테스트로 **일반화 능력**을 극대화했습니다.
<br>
  
### 2. **기술적 차별점**
<br>

- **Teachable Machine**을 활용해 **빠른 개발**과 **높은 성능**을 함께 달성
- **병원 검색** + **유튜브 검색**을 통합해, 종 분류 후 **즉시 정보 탐색**이 가능
- 단순 분류 도구를 넘어, **정보 허브**로 자리 잡을 수 있는 플랫폼
<br>

### 3. **추가 발전 가능성**
<br>

- **커뮤니티 기능**(Q&A, 데이터셋 공유)으로 사용자 간 활발한 정보 교류
- **보호 단체 협업**: 멸종위기종 정보를 추가해 환경 보호에 기여
- **오픈소스 프로젝트**로 확장해 글로벌 개발자들과 협업



---
## 📚 자료 출처 


<img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white" />   


- [amphibians-data-set](https://www.kaggle.com/datasets/ishandutta/amphibians-data-set)
- [Reptiles and Amphibians Image Dataset](https://www.kaggle.com/datasets/vencerlanz09/reptiles-and-amphibians-image-dataset)
- [Breeders_20241101-20241201](https://www.kaggle.com/datasets/cyj5480140/breeders-20241101-20241201)




