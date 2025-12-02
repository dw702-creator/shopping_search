import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Clothing Image Search", layout="wide")
st.title("옷 이미지 검색기")

# 사용자 입력
type_ = st.text_input("종류 (예: hoodie, sweatshirt, jacket, 티셔츠 등)")
color = st.text_input("색깔 (예: grey, black, white, blue 등)")
design = st.text_input("디자인 키워드 (예: black text, graphic, 로고 등)")
num_images = st.slider("이미지 개수", 1, 20, 5)

def build_query(type_, color, design):
    pieces = []
    if type_:
        pieces.append(type_)
    if color:
        pieces.append(color)
    if design:
        pieces += design.split()
    return " ".join(pieces)

def search_google_images(query, max_results=5):
    query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    img_tags = soup.find_all("img")
    img_urls = []
    for img in img_tags:
        src = img.get("src")
        if src and src.startswith("http"):
            img_urls.append(src)
        if len(img_urls) >= max_results:
            break
    return img_urls

if st.button("검색"):
    query = build_query(type_.lower(), color.lower(), design.lower())
    st.write(f"🔎 검색어: {query}")
    try:
        img_urls = search_google_images(query, num_images)
        if img_urls:
            st.write(f"{len(img_urls)}개 이미지 찾음:")
            for url in img_urls:
                st.image(url, use_column_width=True)
        else:
            st.write("검색 결과 없음. 검색어를 바꿔보세요.")
    except Exception as e:
        st.write("이미지 검색 실패:", e)
