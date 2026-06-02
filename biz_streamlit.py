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
st.image("./data2/파이썬 설명.jpeg", caption="파이썬 설명 이미지입니다.", width=500)

"#### :orange[비디오:st.video()]"
st.video("./data2/커피.mp4")

"#### :orange[오디오:st.audio()]"
st.audio("./data2/파이썬 음원.mp3")


"#### :orange[Pandas 데이터프레임]"
import pandas as pd
df = pd.DataFrame({
    '이름': ['홍길동', '김철수', '박영희'],
    '나이': [25, 30, 22],
    '직업': ['학생', '회사원', '프리랜서'] 
})
st.dataframe(df)

'''

|이름|나이|직업|
|---|---|---|
|홍길동|25|학생|
|김철수|30|회사원|
|박영희|22|프리랜서|

'''

'#### :orange[지표:st.metric()]'
col1, col2, col3, col4 = st.columns(4)
col1.metric("온도", "25°C", "2°C")
col1.write("이건 온도입니다.")
col2.metric("습도", "60%", "-5%")
col2.write("이건 습도입니다.")
col3.metric("풍속", "10km/h", "1km/h")
col4.metric("강수량", "5mm", "0mm")


import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
    )

"#### :orange[차트:st.line_chart()]"
st.line_chart(chart_data)

st.bar_chart(chart_data)

st.area_chart(chart_data)

st.scatter_chart(chart_data)

df = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.55, 126.97],
    columns=['lat', 'lon']
    )
st.map(df)

st.divider()

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)
