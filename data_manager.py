import os
import pandas as pd
import datetime

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"

def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    try:
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
    except Exception as e:
        print(f"❌ 데이터 저장 중 오류 발생: {e}")

def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    if os.path.exists(DATA_PATH):
        try:
            return pd.read_csv(DATA_PATH)
        except Exception as e:
            print(f"❌ 데이터 로드 중 오류 발생: {e}")
            return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
    else:
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
