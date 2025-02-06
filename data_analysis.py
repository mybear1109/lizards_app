import os
import pandas as pd
import datetime

# ✅ 데이터 파일 경로
DATA_PATH = "data/Lizards.csv"

# ✅ 분석 결과 저장 함수 (디렉터리 체크 추가)
def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    
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
