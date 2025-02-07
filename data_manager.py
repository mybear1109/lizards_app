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
            try:
                existing_data = pd.read_csv(DATA_PATH, encoding="utf-8-sig", on_bad_lines="skip")

                # ✅ 기존 컬럼 체크 및 자동 수정
                for col in EXPECTED_COLUMNS:
                    if col not in existing_data.columns:
                        existing_data[col] = ""

                existing_data = existing_data[EXPECTED_COLUMNS]  # ✅ 컬럼 정렬
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                
                print("✅ Step 4: 기존 데이터 로드 및 병합 완료")

            except Exception as e:
                st.error(f"❌ 기존 데이터 읽기 오류: {e}")
                updated_data = new_data  # 기존 데이터가 깨진 경우 새로운 데이터만 저장

        else:
            updated_data = new_data  # 기존 데이터가 없을 경우 새로 생성
            print("✅ Step 5: 기존 데이터 없음, 새 파일 생성")

        # ✅ CSV 저장
        updated_data.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
        st.success("✅ 데이터 저장 완료!")
        print("✅ Step 6: 데이터 저장 완료")

    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")

def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, encoding="utf-8-sig", on_bad_lines="skip")

            # ✅ CSV 파일이 비어있는 경우
            if df.empty:
                st.warning("⚠️ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
                return pd.DataFrame(columns=EXPECTED_COLUMNS)

            # ✅ 컬럼 체크 및 자동 수정
            for col in EXPECTED_COLUMNS:
                if col not in df.columns:
                    df[col] = ""

            print("✅ Step 7: 기존 데이터 로드 완료")  
            return df[EXPECTED_COLUMNS]  # ✅ 올바른 컬럼 구조 유지

        else:
            st.warning("⚠️ 저장된 데이터가 없습니다. 데이터를 분석한 후 다시 확인하세요.")
            return pd.DataFrame(columns=EXPECTED_COLUMNS)

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
