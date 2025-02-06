import os
import pandas as pd
import datetime

# ✅ 데이터 파일 경로
DATA_PATH = "data/Lizards.csv"

# ✅ CSV 파일의 올바른 컬럼 구조 (Morph 컬럼 추가)
EXPECTED_COLUMNS = ["Date", "Image", "Species", "Confidence", "Morph"]

def save_prediction(image_name, species, confidence, morph):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    
    try:
        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Species": [species],
            "Confidence": [confidence],
            "Morph": [morph]  # ✅ 모프 데이터 추가
        })

        # ✅ 기존 데이터 확인 후 컬럼 체크
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 컬럼이 올바른지 확인 및 자동 수정
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in existing_data.columns]
            for col in missing_columns:
                existing_data[col] = None  # ✅ 누락된 컬럼 추가
            
            existing_data = existing_data[EXPECTED_COLUMNS]  # ✅ 컬럼 정렬
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # ✅ CSV 파일 저장
        updated_data.to_csv(DATA_PATH, index=False)
        print("✅ 데이터 저장 완료!")

    except Exception as e:
        print(f"❌ 데이터 저장 중 오류 발생: {e}")
