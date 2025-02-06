import os
import pandas as pd
import datetime

# ✅ 데이터 파일 경로
DATA_PATH = "data/Lizards.csv"

def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    try:
        # ✅ 저장 경로 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        # ✅ 새로운 데이터 생성
        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Species": [species],
            "Confidence": [confidence]
        })

        # ✅ 기존 데이터와 병합
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # ✅ CSV 저장
        updated_data.to_csv(DATA_PATH, index=False)
    except Exception as e:
        print(f"❌ 데이터 저장 중 오류 발생: {e}")

def load_existing_data():
    """ 기존 분석 데이터를 로드하는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            return pd.read_csv(DATA_PATH)
        else:
            return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
    except Exception as e:
        print(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
