import os
import pandas as pd
import datetime

# ✅ 데이터 파일 경로 변경 (쓰기 권한 문제 해결)
DATA_PATH = "./data/Lizards.csv"  # ✅ 현재 디렉토리의 data 폴더 사용 (권장)
# DATA_PATH = "/tmp/Lizards.csv"  # ✅ Streamlit Cloud 또는 서버 환경에서는 /tmp 사용 가능

# ✅ 분석 결과 저장 함수 (디렉터리 체크 추가)
def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    
    # ✅ 저장 경로가 존재하지 않으면 생성
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    new_data = pd.DataFrame({
        "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Image": [image_name],
        "Species": [species],
        "Confidence": [confidence]
    })

    if os.path.exists(DATA_PATH):
        existing_data = pd.read_csv(DATA_PATH)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(DATA_PATH, index=False)


# ✅ 기존 데이터 로드 함수
def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
