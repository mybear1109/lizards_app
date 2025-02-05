import streamlit as st
import pandas as pd
import os
from PIL import Image
import random

# 앱 메인 함수
def main():
    st.title("🦎 Guess the Species Game!")
    st.info("이미지를 보고 해당 종(Species)을 맞춰보세요.")

    # CSV 데이터 로드
    data_file = "model/Lizards.csv"  # CSV 파일 이름
    image_folder = "image"  # 이미지 폴더 이름

    if not os.path.exists(data_file):
        st.error("❌ CSV 파일이 존재하지 않습니다. 파일 경로를 확인하세요.")
        return

    if not os.path.exists(image_folder):
        st.error("❌ 이미지 폴더가 존재하지 않습니다. 폴더 경로를 확인하세요.")
        return

    # 데이터 로드
    df = pd.read_csv(data_file)

    # 이미지와 종 정보 매칭
    if "Filename" not in df.columns or "Species" not in df.columns:
        st.error("❌ CSV 파일에 'Filename' 또는 'Species' 컬럼이 없습니다.")
        return

    # 이미지 선택 (랜덤)
    image_files = df["Filename"].tolist()
    selected_image = random.choice(image_files)
    image_path = os.path.join(image_folder, selected_image)

    # 이미지 표시
    if os.path.exists(image_path):
        st.image(Image.open(image_path), caption="Guess the Species!", use_column_width=True)

        # 사용자 입력 (종 선택)
        species_list = sorted(df["Species"].unique())
        user_guess = st.selectbox("어떤 종인지 선택하세요:", species_list)

        # 정답 확인 버튼
        if st.button("정답 확인"):
            actual_species = df[df["Filename"] == selected_image]["Species"].values[0]
            if user_guess == actual_species:
                st.success(f"🎉 정답입니다! 이 종은 **{actual_species}** 입니다.")
            else:
                st.error(f"❌ 틀렸습니다. 정답은 **{actual_species}** 입니다.")
    else:
        st.error(f"❌ 이미지 파일을 찾을 수 없습니다: {selected_image}")

    # 추가 기능: 전체 데이터 보기
    if st.checkbox("전체 데이터 보기"):
        st.dataframe(df)

if __name__ == "__main__":
    main()
