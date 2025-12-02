import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

st.set_page_config(page_title="Clothing Search Online", layout="wide")
st.title("온라인 의류 검색기")

type_ = st.text_input("종류 (예: hoodie, sweatshirt, jacket, 티셔츠 등)", "")
color = st.text_input("색깔 (예: grey, black, white, blue 등)", "")
design = st.text_input("디자인 키워드 (예: black text, graphic, 로고 등)", "")

SEARCH_COUNT = st.sidebar.number_input("최대 검색 결과 수 (per 사이트)", min_value=5, max_value=50, value=10)

def build_query(type_, color, design):
    pieces = []
    if type_:
        pieces.append(type_)
    if color:
        pieces.append(color)
    if design:
        pieces += design.split()
    return " ".join(pieces)

def search_naver_shopping(query, max_results=10):
    url = "https://search.shopping.naver.com/search/all"
    params = {"query": query}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for item in soup.select("a.basicList_link__JLQJf")[:max_results]:
        title = item.get_text().strip()
        link = item.get("href")
        items.append({"title": title, "link": link, "source": "Naver Shopping"})
    return items

def search_google(query, max_results=10):
    # Note: 구글은 크롤링 방지 정책이 있음 — 잘 동작하지 않을 수 있음
    url = "https://www.google.com/search"
    params = {"q": query + " 의류", "num": max_results}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for g in soup.select("div.g")[:max_results]:
        a = g.select_one("a")
        if not a:
            continue
        title = a.get_text().strip()
        link = a.get("href")
        # 간단 필터: title 또는 snippet 안에 색깔/디자인 키워드 포함 여부 확인
        results.append({"title": title, "link": link, "source": "Google"})
    return results

if st.button("검색"):
    query = build_query(type_.lower(), color.lower(), design.lower())
    st.write("🔎 검색어:", query)
    results = []
    try:
        results += search_naver_shopping(query, SEARCH_COUNT)
    except Exception as e:
        st.write("네이버 쇼핑 검색 실패:", e)
    try:
        results += search_google(query, SEARCH_COUNT)
    except Exception as e:
        st.write("구글 검색 실패:", e)

    if results:
        st.write(f"{len(results)}개 결과 (최대 {SEARCH_COUNT} per 사이트).")
        for r in results:
            st.write(f"- **{r['title']}** — {r['source']} — [링크 열기]({r['link']})")
    else:
        st.write("검색 결과가 없습니다. 검색어를 바꿔 보세요.")
