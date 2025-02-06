import os
import pandas as pd
import datetime
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"
IMAGE_FOLDER = "data/images/"

# ✅ CSV 파일의 올바른 컬럼 구조 (Morph 및 Price 컬럼 포함)
EXPECTED_COLUMNS = ["Date", "Image", "Size", "Species", "Confidence", "Morph", "Price"]

def save_prediction(image_file, species, confidence, morph="", size="", price=""):
    """ 분석된 결과를 CSV 파일에 추가하는 함수 """
    try:
        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        print(f"안녕1")

        # ✅ 이미지 파일명 생성 (유니크한 이름)
        if hasattr(image_file, "name"):
            image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.name}"
        else:
            image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file}"
        print(f"안녕2")
        image_path = os.path.join(IMAGE_FOLDER, image_name)


        # ✅ 새로운 데이터 생성 (기본값 자동 적용)
        new_data = pd.DataFrame([{
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Image": image_name,
            "Size": size,
            "Species": species,
            "Confidence": confidence,
            "Morph": morph,
            "Price": price
        }])
        print(f"안녕3")
  
        # ✅ 기존 데이터 로드 및 컬럼 정리
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 기존 컬럼과 기대하는 컬럼 비교하여 수정
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in existing_data.columns]
            for col in missing_columns:
                existing_data[col] = ""  # ✅ 누락된 컬럼을 공란으로 추가

            existing_data = existing_data[EXPECTED_COLUMNS]
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

            # ✅ CSV 저장
            updated_data.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")

        st.success("✅ 데이터 저장 완료!")

    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")


