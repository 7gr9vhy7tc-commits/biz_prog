import streamlit as st
import json
import os
import datetime
from PIL import Image

# ==============================================================================
# 1. CONSTANTS & INITIALIZATION
# ==============================================================================
st.set_page_config(page_title="30일 다이어트 다이어리", page_icon="🥗", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "diet_data.json")
PHOTOS_DIR = os.path.join(BASE_DIR, "diet_photos")

if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

FOOD_DICT = {
    "닭가슴살 (100g)": 165, "고구마 (100g)": 130, "현미밥 (1공기)": 220,
    "흰쌀밥 (1공기)": 300, "삶은 계란 (1개)": 80, "사과 (1개)": 100,
    "바나나 (1개)": 90, "아보카도 (1개)": 320, "샐러드 (채소만)": 20,
    "소고기 (우둔살 100g)": 137, "연어 (100g)": 160, "아메리카노 (1잔)": 5,
    "우유 (200ml)": 130, "방울토마토 (10개)": 30, "그릭요거트 (100g)": 100,
    "두부 (150g)": 120, "단백질 쉐이크": 120, "견과류 (1봉지)": 150,
    "오이 (1개)": 15, "파프리카 (1개)": 30, "라면 (1봉지)": 500,
    "김밥 (1줄)": 400, "떡볶이 (1인분)": 350, "치킨 (1조각)": 250,
    "피자 (1조각)": 300, "요거트 (80g)": 70, "식빵 (1장)": 120,
    "치즈 (1장)": 60, "참치캔 (100g)": 150, "아몬드 브리즈": 45,
}

# ==============================================================================
# 2. DATA MANAGEMENT
# ==============================================================================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "start_date": datetime.date.today().strftime("%Y-%m-%d"),
        "target_calories": 1800,
        "days": {}
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "diet_data" not in st.session_state:
    st.session_state.diet_data = load_data()

data = st.session_state.diet_data

# ==============================================================================
# 3. HELPER FUNCTIONS
# ==============================================================================
def get_day_total_calories(date_str):
    day_data = data.get("days", {}).get(date_str, {})
    meals = day_data.get("meals", {})
    return sum(item.get("calories", 0) for meal_list in meals.values() for item in meal_list)

def get_dates_list():
    today = datetime.date.today()
    dates = [(today + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-180, 181)]
    if "days" in data:
        for date_str in data["days"]:
            if date_str not in dates:
                dates.append(date_str)
    return sorted(dates)

# ==============================================================================
# 4. UI: SIDEBAR
# ==============================================================================
st.sidebar.title("30일 다이어트 다이어리 🗓️")
st.sidebar.markdown("---")

new_target = st.sidebar.number_input("일일 목표 권장 칼로리 (kcal)", min_value=1, value=data.get("target_calories", 1800), step=100)
if new_target != data.get("target_calories"):
    data["target_calories"] = new_target
    save_data(data)

st.sidebar.markdown("---")
st.sidebar.subheader("식단 일지 타임라인")
dates_list = get_dates_list()
today_str = datetime.date.today().strftime("%Y-%m-%d")

# Find index of today to set as default
default_idx = dates_list.index(today_str) if today_str in dates_list else 0
selected_date = st.sidebar.selectbox("날짜 선택", dates_list, index=default_idx)

# Initialize day data if missing
if "days" not in data:
    data["days"] = {}
if selected_date not in data["days"]:
    data["days"][selected_date] = {"meals": {"breakfast": [], "lunch": [], "dinner": []}}
    
day_data = data["days"][selected_date]

# ==============================================================================
# 5. UI: MAIN PANEL
# ==============================================================================
# Parse date for a nice header display
dt = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
day_name = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
st.header(f"{dt.year}년 {dt.month:02d}월 {dt.day:02d}일 ({day_name}요일)의 식단")

col_photo, col_stat = st.columns([1, 1])

# --- Photo Card ---
with col_photo:
    st.subheader("📷 식단 사진")
    
    photo_path = day_data.get("photo_path")
    if photo_path and os.path.exists(os.path.join(BASE_DIR, photo_path)):
        img = Image.open(os.path.join(BASE_DIR, photo_path))
        st.image(img, use_container_width=True)
        if st.button("사진 삭제", key="del_photo"):
            try:
                os.remove(os.path.join(BASE_DIR, photo_path))
            except:
                pass
            day_data["photo_path"] = None
            save_data(data)
            st.rerun()
    else:
        uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg", "webp"])
        if uploaded_file is not None:
            # Save file
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            dest_filename = f"{selected_date}{ext}"
            dest_path = os.path.join(PHOTOS_DIR, dest_filename)
            with open(dest_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            day_data["photo_path"] = os.path.relpath(dest_path, BASE_DIR)
            save_data(data)
            st.rerun()

# --- Progress Stats ---
with col_stat:
    st.subheader("📊 섭취량 및 진척도")
    total_cal = get_day_total_calories(selected_date)
    target_cal = data.get("target_calories", 1800)
    
    progress_ratio = min(total_cal / target_cal, 1.0) if target_cal > 0 else 0.0
    
    st.metric(label="오늘 섭취한 칼로리", value=f"{total_cal} kcal", delta=f"{target_cal - total_cal} kcal 남음", delta_color="inverse")
    st.progress(progress_ratio)
    
    if total_cal == 0:
        st.info("오늘 하루의 건강한 식단을 기록해 보세요.")
    elif total_cal <= target_cal:
        st.success("아주 잘하고 있어요! 목표 칼로리 내에서 잘 유지 중입니다.")
    else:
        st.warning(f"목표 칼로리를 {total_cal - target_cal} kcal 초과했습니다!")

st.markdown("---")

# ==============================================================================
# 6. UI: MEAL LOGS
# ==============================================================================
st.subheader("🍽️ 식사 기록")

meal_cols = st.columns(3)
meal_names = [("breakfast", "아침 식사"), ("lunch", "점심 식사"), ("dinner", "저녁 식사")]

for col, (meal_key, meal_label) in zip(meal_cols, meal_names):
    with col:
        st.markdown(f"#### {meal_label}")
        
        meals_list = day_data.get("meals", {}).get(meal_key, [])
        meal_total = sum(item.get("calories", 0) for item in meals_list)
        st.caption(f"**총 {meal_total} kcal**")
        
        # Display existing items
        for idx, item in enumerate(meals_list):
            item_col1, item_col2 = st.columns([4, 1])
            with item_col1:
                st.write(f"- {item['food']} ({item['calories']} kcal)")
            with item_col2:
                if st.button("❌", key=f"del_{selected_date}_{meal_key}_{idx}"):
                    meals_list.pop(idx)
                    save_data(data)
                    st.rerun()
                    
        # Add new item form
        with st.expander(f"+ {meal_label} 추가"):
            with st.form(key=f"form_{selected_date}_{meal_key}"):
                food_options = ["직접 입력"] + list(FOOD_DICT.keys())
                selected_food = st.selectbox("음식 선택", food_options)
                custom_food = st.text_input("음식명 (직접 입력 시)")
                custom_cal = st.number_input("칼로리 (kcal)", min_value=0, step=10)
                
                if st.form_submit_button("추가하기"):
                    food_name = custom_food.strip() if selected_food == "직접 입력" else selected_food
                    cal = custom_cal if selected_food == "직접 입력" else FOOD_DICT[selected_food]
                    
                    if not food_name:
                        st.error("음식명을 입력해 주세요.")
                    else:
                        if "meals" not in day_data:
                            day_data["meals"] = {}
                        if meal_key not in day_data["meals"]:
                            day_data["meals"][meal_key] = []
                            
                        day_data["meals"][meal_key].append({
                            "food": food_name,
                            "calories": cal
                        })
                        save_data(data)
                        st.rerun()
