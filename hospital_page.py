import streamlit as st
import requests
import urllib.parse

# 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local"

def search_hospitals(query="파충류 동물병원", display=5):
    """네이버 지역 검색 API를 사용해 병원을 검색."""
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}
    try:
        response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            st.error(f"API 호출 실패: 상태 코드 {response.status_code}")
            return []
    except Exception as e:
        st.error(f"네트워크 오류: {e}")
        return []

def display_hospitals(query):
    """병원 검색 결과를 화면에 출력."""
    st.title("🏥 병원 검색 결과")
    hospitals = search_hospitals(query)
    
    if hospitals:
        for hospital in hospitals:
            # 병원 이름 및 아이콘 표시
            st.markdown(f"### 🏥 {hospital['title']}")
            
            # 병원 주소
            st.write(f"📍 **주소**: {hospital['address']}")
            
            # 지도 Embed 생성
            address_encoded = urllib.parse.quote(hospital['address'])
            map_embed_url = f"https://www.google.com/maps/embed/v1/place?q={address_encoded}&key=AIzaSyAS_ZTJBz_vkppLJu2GkMe6uXy9sCda5"
            st.markdown(
                f"""
                <iframe 
                    src="{map_embed_url}" 
                    width="100%" 
                    height="300" 
                    style="border:0;" 
                    allowfullscreen="" 
                    loading="lazy">
                </iframe>
                """,
                unsafe_allow_html=True,
            )
            
            # 전화번호
            st.write(f"📞 **전화번호**: {hospital.get('telephone', '정보 없음')}")
            
            # 네이버 상세보기 링크
            st.markdown(f"[🔗 네이버 상세보기]({hospital['link']})", unsafe_allow_html=True)

            # 구분선
            st.divider()
    else:
        st.write("검색 결과가 없습니다.")

# 실행 예제
if __name__ == "__main__":
    st.sidebar.title("🏥 병원 검색")
    hospital_query = st.sidebar.text_input("검색어 입력", "파충류 동물병원")
    
    if st.sidebar.button("검색"):
        display_hospitals(hospital_query)
