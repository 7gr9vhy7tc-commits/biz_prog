import streamlit as st # 스트림릿 라이브러리 임포트

# 타이틀 텍스트 출력
st.title("첫 번째 웹 어플 만들기 👋🐱")

"## 이건 부제목입니다."

"""
# 비즈니스 모델 분석

[네이버](https://www.naver.com)  
[홍익대학교](https://www.hongik.ac.kr)  

이것은 일반 본문
:red[빨간색 글씨] :blue[파란색 글씨] :green[초록색 글씨]
"""

st.caption("이건 캡션입니다.")

print("코드 블록")

with st.echo():
    name = 'Hyunju'
    st.write(f"Hello, streamlit! {name}")    

st.latex('\int_a^b f(x) dx')
"$$\int_a^b f(x) dx$$"

"""
"""

"#### :orange[이미지:st.image()]"
st.image("/Users/hyunju/Documents/2026_biz/lectures/data/파이썬 설명.jpeg", caption="파이썬 설명 이미지", width=500)

"#### :orange[비디오:st.video()]"
st.video("/Users/hyunju/Documents/2026_biz/lectures/data/17422066-hd_1080_1920_25fps.mp4")

"#### :orange[오디오:st.audio()]"
st.audio("/Users/hyunju/Documents/2026_biz/lectures/data/파이썬 음원.mp3")

# 폴더 만들어서 넣어 줘야 올라감
