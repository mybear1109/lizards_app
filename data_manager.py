import os
import pandas as pd
import datetime

# ✅ 데이터 파일 경로
DATA_PATH = "data/Lizards.csv"

# ✅ 분석 결과 저장 함수 (디렉터리 체크 추가)
def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    
    try:
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Species": [species],
            "Confidence": [confidence]
        })

        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 컬럼이 올바른지 확인
            expected_columns = ["Date", "Image", "Species", "Confidence"]
            if list(existing_data.columns) != expected_columns:
                print("❌ 기존 데이터 컬럼이 올바르지 않습니다. CSV 파일을 확인하세요.")
                return

            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_csv(DATA_PATH, index=False)
        print("✅ 데이터 저장 완료!")

    except Exception as e:
        print(f"❌ 데이터 저장 중 오류 발생: {e}")

# ✅ 기존 데이터 로드 함수
def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)

            # ✅ 컬럼 체크
            expected_columns = ["Date", "Image", "Species", "Confidence"]
            if list(df.columns) != expected_columns:
                print("❌ CSV 파일의 컬럼 구조가 맞지 않습니다. 데이터를 확인하세요.")
                return pd.DataFrame(columns=expected_columns)

            return df
        else:
            print("⚠️ 저장된 데이터가 없습니다.")
            return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])

    except Exception as e:
        print(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=["Date", "Image", "Species", "Confidence"])
