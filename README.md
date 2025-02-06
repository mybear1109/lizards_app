
# 🦎 <span style="font-size: 2em; color: #4CAF50;">Reptile Explorer: Discover the World of Reptiles</span>

---

## <span style="color: #FF5733;">✨ 프로젝트 소개</span>

> **Reptile Explorer**는 **AI 모델(Teachable Machine)**을 활용하여  
> **<span style="color: #2ECC71;">18종의 파충류 및 양서류를 자동 분류</span>**하고,  
> 🏥 **특수동물 병원 검색**과 🎥 **유튜브 영상 검색**까지 지원하는  
> **Streamlit 기반 웹 애플리케이션**입니다.  

**누구나 쉽고 빠르게 파충류를 식별**하고,  
**관련 정보를 한눈에 확인할 수 있는 유용한 플랫폼**입니다.  

---

## **🎯 <span style="color: #3498DB;">주요 목표</span>**

✅ **<span style="font-size: 1.2em;">18종 파충류/양서류 자동 분류</span>**  
✅ **<span style="font-size: 1.2em;">파충류 병원 검색 및 위치 안내</span>**  
✅ **<span style="font-size: 1.2em;">파충류 관련 유튜브 영상 검색</span>**  

---

## **📂 <span style="color: #8E44AD;">프로젝트 구조</span>**

> **세분화된 파일 구성**으로 각 기능이 모듈화되어 있습니다.

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
├── about.py
├── app.py                # Streamlit 메인 애플리케이션
├── data_analysis.py      # 데이터로드와 시각화
├── data_manager.py       # 데이터저장과 수정
├── hospital_page.py      # 병원 검색 기능
├── image_analysis.py     # 이미지 분석(AI 모델) 기능
├── plot.py               # 데이터 시각화
├── sidebar.py            # 사이드바 UI
├── species_info.py       # 종별 상세 설명
├── youtube_page.py       # 유튜브 검색 기능


```

---

## **⚙️ <span style="color: #F39C12;">기술 스택</span>**

> **다양한 기술과 API를 활용**하여 효율적이고 정확한 애플리케이션을 개발했습니다.

| **기술/라이브러리**            | **역할**                                                         |
|--------------------------------|-----------------------------------------------------------------|
| 🧠 **Teachable Machine**       | AI 기반 18종 파충류/양서류 분류 모델 구축                      |
| 💻 **Streamlit**               | Python 기반 웹 애플리케이션 프레임워크                          |
| 📊 **Pandas, NumPy**           | 데이터 처리 및 전처리                                           |
| 📈 **Matplotlib, Seaborn, Plotly**| 데이터 시각화 및 통계 차트 생성                               |
| 🎥 **YouTube API**             | 파충류 관련 영상 검색                                          |
| 🗺️ **병원 검색 API**            | 네이버/구글 병원 데이터 연계 및 정확도 향상                   |
| 📝 **블로그/데이터 연계** | 병원 정보의 신뢰도 향상을 위한 추가 데이터 사용               |

---

## **🌟 <span style="color: #27AE60;">주요 특징</span>**

### **1️⃣ 풍부한 데이터 기반 AI 모델**
- Kaggle의 **Reptiles and Amphibians Dataset** + 국내 애완 파충류 시장 데이터(**The Breeders**) 결합  
- 초기 9종 → 현재 **18종**으로 확장!  
  🦎 **뱀, 이구아나, 양서류**까지 폭넓게 지원  

---

### **2️⃣ 이미지 분석 (AI 기반 분류)**

- **사용자 이미지 업로드** → **AI 모델 자동 분류**  
- 예측 결과(종명 + 확률) 및 간략한 설명 제공  
- 🦎 **모프 정보 입력 가능**:  
  → 교배 시 **2세대 특성 예측** 지원  

---

### **3️⃣ 파충류 병원 검색**

- **특수동물 병원 찾기 어려움**을 해결하기 위해 개발된 기능  
- 🗺️ **지도 기반 병원 검색**으로 가까운 병원을 빠르게 확인  
- 네이버/구글 API와 **블로그/인스타 정보 연계**로 신뢰도 향상  

---

### **4️⃣ 유튜브 검색 기능**

- **유튜브 영상 검색 및 연결**  
- 🎥 파충류 사육법, 질병 예방, 서식 환경 개선 등 유익한 정보를 제공  
- 초보 사육자에게 **안전한 사육 환경 조성**을 돕습니다!  

---

## **🛠️ <span style="color: #E74C3C;">설치 및 실행 가이드</span>**

1️⃣ **필요 라이브러리 설치**  

```bash
pip install -r requirements.txt
```  

2️⃣ **Streamlit 앱 실행**  

```bash
streamlit run app.py
```  

3️⃣ **웹 브라우저 접속**  
- 기본 주소: **`http://localhost:8501`**  

---

## **📊 <span style="color: #2980B9;">데이터 및 학습 과정</span>**

### **분류 대상 (총 18종)**  
- Beardy Dragon, Panther Chamaeleon, Crestedgeko, Leopardgeko, Iguana, Frog, Salamander,  
  Snake, Turtle, Newt, Pacman, Toad, Leachianus Gecko, Gecko, Chahoua Gecko, Gargoyle Gecko, Skink  

### **학습 과정**  
- **Epoch**: 100  
- **Batch Size**: 128  
- **5번 반복 학습**으로 동일 무늬/패턴 문제 해결  
- **데이터 증강**(조명·각도 변화)으로 **모델의 일반화 성능** 극대화  

---

## **✨ <span style="color: #8E44AD;">실제 활용 & 기대 효과</span>**

### **1️⃣ 실용성과 편의성**  
- 이미지 분류 + 병원 검색 + 유튜브 검색을 **한 플랫폼**에서 제공  
- **특수동물 병원 정보**를 빠르게 확인 가능  

### **2️⃣ 교육 및 연구 활용**  
- AI 기반 **파충류 분류 체험**  
- 심층적인 학습 자료 제공  

### **3️⃣ 모프 정보 수집 및 교배 예측**  
- 다양한 **모프 데이터**를 체계적으로 축적  
- 2세대 교배 특성 예측 지원  

---

## **🏆 <span style="color: #9B59B6;">프로젝트의 독창성</span>**

- **단순 AI 분류**를 넘어 **정보 허브**로서 기능!  
- 생물학 연구, 환경 보호, 교육 등 **다양한 분야**에서 활용 가능!  

---

### **"Reptile Explorer"는 파충류와 양서류를 사랑하는 모든 분들을 위한  
**<span style="color: #2ECC71;">혁신적인 플랫폼</span>입니다. 🦎  
지금 바로 탐험을 시작하세요! 🎉**

