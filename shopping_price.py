import streamlit as st
import json

# --- 예시 데이터베이스 ---
# 실제로는 CSV, DB, 외부 API 등으로 바꿀 수 있음
PRODUCTS = [
    {
        "id": 1,
        "name": "Grey Hoodie with Black Lettering",
        "type": "hoodie",
        "color": "grey",
        "design": "black_text",
        "description": "A comfy grey hoodie with bold black letter print on chest."
    },
    {
        "id": 2,
        "name": "Black Hoodie with White Design",
        "type": "hoodie",
        "color": "black",
        "design": "white_graphic",
        "description": "Stylish black hoodie with white graphic print."
    },
    {
        "id": 3,
        "name": "Grey Sweatshirt Plain",
        "type": "sweatshirt",
        "color": "grey",
        "design": "plain",
        "description": "Simple grey sweatshirt, no print."
    },
    {
        "id": 4,
        "name": "Blue Hoodie with Black Text",
        "type": "hoodie",
        "color": "blue",
        "design": "black_text",
        "description": "Blue hoodie with black letters."
    },
    # ... 필요하면 더 추가
]

# --- 매칭 함수 ---
def matches(product, type_, color, design_keywords):
    if type_ and product.get("type") != type_:
        return False
    if color and product.get("color") != color:
        return False
    if design_keywords:
        # design_keywords는 여러 단어일 수 있음 (예: ["black","text"])
        # product["design"] 또는 description에 포함 여부 체크
        d = product.get("design", "") + " " + product.get("description", "")
        for kw in design_keywords:
            if kw.lower() not in d.lower():
                return False
    return True

def search_products(type_, color, design_keywords):
    results = []
    for p in PRODUCTS:
        if matches(p, type_, color, design_keywords):
            results.append(p)
    return results

# --- Streamlit UI ---
st.title("Simple Clothing Search")

st.write("원하는 옷: 종류, 색깔, 디자인 키워드를 입력하세요.")

type_ = st.text_input("종류 (예: hoodie, sweatshirt 등)", value="")
color = st.text_input("색깔 (예: grey, black, blue …)", value="")
design = st.text_input("디자인 키워드 (예: black text, white graphic)", value="")

if st.button("검색"):
    design_keywords = design.split()
    results = search_products(type_.lower().strip() or None,
                              color.lower().strip() or None,
                              design_keywords)
    if results:
        st.write(f"{len(results)}개 찾음.")
        for p in results:
            st.write(f"**{p['name']}** (ID: {p['id']}) — 색상: {p['color']}, 디자인: {p['design']}")
            st.write(p.get("description", ""))
    else:
        st.write("조건에 맞는 상품이 없습니다.")

