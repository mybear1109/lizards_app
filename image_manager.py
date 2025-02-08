import os
import pandas as pd
import datetime
from PIL import Image
import streamlit as st

# ✅ 데이터 파일 경로 설정
IMAGE_FOLDER = "data/images/"

# ✅ 이미지 저장 함수 (이미지 경로 및 파일명 반환)
def save_image(image_file):
    """ 이미지를 'data/images/' 폴더에 저장하는 함수 """
    try:
        # 저장할 파일 경로 생성 (유니크한 이름 부여)
        if hasattr(image_file, "name"):
            image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.name}"
        else:
            image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file}"

        # 이미지 파일 저장 경로
        image_path = os.path.join(IMAGE_FOLDER, image_name)

        # 이미지 열기
        image = Image.open(image_file)

        # 파일 형식 확인 (지원되는 이미지 형식인지)
        if image.format not in ['JPEG', 'PNG']:
            st.error("❌ 지원되지 않는 이미지 형식입니다. JPG 또는 PNG 파일을 업로드해주세요.")
            return None

        # 이미지를 지정된 경로에 저장
        image.save(image_path)
        st.success(f"✅ 이미지가 성공적으로 저장되었습니다: {image_path}")
        
        # 이미지 경로와 이름 반환
        return image_path, image_name

    except Exception as e:
        st.error(f"❌ 이미지 저장 중 오류 발생: {e}")
        return None, None


# 예시: 이미지 업로드 및 처리
uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지를 저장하고 경로 반환
    image_path, image_name = save_image(uploaded_file)
    
    if image_path:
        st.image(image_path, caption="업로드된 이미지", use_column_width=True)

        # 이미지 경로와 이름만 사용
        st.write(f"이미지 경로: {image_path}")
        st.write(f"이미지 이름: {image_name}")
