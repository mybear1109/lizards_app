import streamlit as st
import pandas as pd
import os
from PIL import Image

# CSV와 이미지 경로 설정
DATA_FILE = "model/thebreeder.csv"  # 실제 CSV 파일 경로로 변경
IMAGE_DIR = "image/folders"  # 이미지 폴더 경로로 변경

# Streamlit 앱
def main():
    st.title("종별 분류와 데이터 시각화")
    st.info("업로드된 데이터와 이미지를 이용해 종별로 분류하고 시각화합니다.")

    # CSV 파일 읽기
    try:
        df = pd.read_csv(DATA_FILE)
        st.subheader("📋 CSV 데이터 미리보기")
        st.dataframe(df)
    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류 발생: {e}")
        return

    # 폴더 구조에서 이미지 분류
    try:
        st.subheader("📂 종별 이미지 분류")
        folders = os.listdir(IMAGE_DIR)
        for folder in folders:
            folder_path = os.path.join(IMAGE_DIR, folder)
            if os.path.isdir(folder_path):
                st.write(f"### {folder}")
                files = os.listdir(folder_path)
                for file in files[:5]:  # 각 폴더에서 최대 5개 이미지 표시
                    image_path = os.path.join(folder_path, file)
                    try:
                        image = Image.open(image_path)
                        st.image(image, caption=file, use_column_width=True)
                    except Exception as img_error:
                        st.warning(f"이미지를 불러오지 못했습니다: {file} - {img_error}")
    except Exception as e:
        st.error(f"이미지 폴더를 읽는 중 오류 발생: {e}")
        return

    # 데이터 분석
    st.subheader("📊 데이터 분석")
    if "종" in df.columns:
        st.write(df["종"].value_counts())
    else:
        st.warning("데이터에서 '종' 열을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
