import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Your Shopping Curator 🛍️",
    page_icon="🛒",
    layout="wide"
)

# --- 커스텀 CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    .stButton>button {
        background-color: #FF6F61;
        color: white;
        font-weight: 700;
        border-radius: 10px;
        padding: 0.6em 1em;
        border: none;
        width: 100%;
    }

    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 0.5em;
        border: 1px solid #ddd;
    }

    .img-card {
        padding: 5px;
        margin-bottom: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True
)

# --- 제목 및 설명 ---
st.markdown("## 🛍️ Your Shopping Curator")
st.markdown("원하는 옷 종류, 색상, 디자인을 입력하면 관련 이미지를 바로 보여주는 스마트 이미지 검색기입니다!")

# --- 사용자 입력 ---
with st.form(key="search_form"):
    col1, col2 = st.columns([3,1])
    with col1:
        type_ = st.text_input("종류 (예: hoodie, sweatshirt, jacket, 티셔츠 등)")
        color = st.text_input("색깔 (예: grey, black, white, blue 등)")
        design = st.text_input("디자인 키워드 (예: black text, graphic, 로고 등)")
    with col2:
        num_images = st.slider("이미지 개수", 1, 20, 9)
    submitted = st.form_submit_button("🔍 검색하기")

# --- 검색어 생성 ---
def build_query(type_, color, design):
    pieces = []
    if type_:
        pieces.append(type_)
    if color:
        pieces.append(color)
    if design:
        pieces += design.split()
    return " ".join(pieces)

# --- 구글 이미지 검색 ---
def search_google_images(query, max_results=9):
    query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    img_tags = soup.find_all("img")

    img_urls = []
    for img in img_tags:
        src = img.get("src")
        if not src:
            continue
        # 실제 이미지 URL만 추출 (로고/깨진 이미지 제거)
        if src.startswith("http") and "gstatic.com" not in src:
            img_urls.append(src)
        if len(img_urls) >= max_results:
            break
    return img_urls

# --- 검색 결과 표시 (핀터레스트 3열) ---
def display_images_3col(img_urls):
    if not img_urls:
        st.warning("검색 결과가 없습니다!")
        return
    # 3개씩 분할하여 컬럼 배치
    for i in range(0, len(img_urls), 3):
        cols = st.columns(3)
        for idx, url in enumerate(img_urls[i:i+3]):
            with cols[idx]:
                st.image(url, use_column_width=True)

# --- 검색 버튼 동작 ---
if submitted:
    query = build_query(type_.lower(), color.lower(), design.lower())
    st.markdown(f"### 🔎 검색어: {query}")
    try:
        img_urls = search_google_images(query, num_images)
        st.markdown(f"#### {len(img_urls)}개 이미지 찾음:")
        display_images_3col(img_urls)
    except Exception as e:
        st.error(f"이미지 검색 실패: {e}")
