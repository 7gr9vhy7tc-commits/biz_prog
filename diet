import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import datetime
import shutil
from PIL import Image, ImageTk, ImageOps

# ==============================================================================
# 1. CONSTANTS & SOPHISTICATED NEUTRAL THEME
# ==============================================================================
COLOR_BG = "#FDFBF7"          # Alabaster warm off-white
COLOR_SIDEBAR = "#F3EFE9"     # Linen warm beige sidebar
COLOR_CARD = "#FFFFFF"        # Pure white card
COLOR_CARD_HOVER = "#FAF6EF"  # Cream warm white for hover
COLOR_ACCENT = "#768D80"      # Muted organic sage green
COLOR_ACCENT_HOVER = "#647A6E"# Darker sage green for buttons hover
COLOR_BLUE = "#9AB0A4"        # Pale sage green
COLOR_RED = "#C27A7A"         # Muted dusty rose-red
COLOR_TEXT_PRIMARY = "#2F3230"# Elegant dark charcoal-slate
COLOR_TEXT_MUTED = "#807C78"  # Warm neutral grey-taupe
COLOR_BORDER = "#E5DFD5"      # Fine linen border line
COLOR_INPUT_BG = "#FAFAFA"    # Light off-white input box background

FONT_FAMILY = "Segoe UI" if os.name == "nt" else "Arial"

# Pre-populated food dictionary with calories
FOOD_DICT = {
    "닭가슴살 (100g)": 165,
    "고구마 (100g)": 130,
    "현미밥 (1공기)": 220,
    "흰쌀밥 (1공기)": 300,
    "삶은 계란 (1개)": 80,
    "사과 (1개)": 100,
    "바나나 (1개)": 90,
    "아보카도 (1개)": 320,
    "샐러드 (채소만)": 20,
    "소고기 (우둔살 100g)": 137,
    "연어 (100g)": 160,
    "아메리카노 (1잔)": 5,
    "우유 (200ml)": 130,
    "방울토마토 (10개)": 30,
    "그릭요거트 (100g)": 100,
    "두부 (150g)": 120,
    "단백질 쉐이크": 120,
    "견과류 (1봉지)": 150,
    "오이 (1개)": 15,
    "파프리카 (1개)": 30,
    "라면 (1봉지)": 500,
    "김밥 (1줄)": 400,
    "떡볶이 (1인분)": 350,
    "치킨 (1조각)": 250,
    "피자 (1조각)": 300,
    "요거트 (80g)": 70,
    "식빵 (1장)": 120,
    "치즈 (1장)": 60,
    "참치캔 (100g)": 150,
    "아몬드 브리즈": 45,
}

# ==============================================================================
# 2. AUTOCOMPLETE ENTRY WIDGET
# ==============================================================================
class AutocompleteEntry(tk.Frame):
    def __init__(self, parent, food_dict, on_select_callback, *args, **kwargs):
        super().__init__(parent, bg=COLOR_CARD)
        self.food_dict = food_dict
        self.on_select_callback = on_select_callback
        
        # Border wrapper for a thin, elegant neutral outline
        self.border_frame = tk.Frame(self, bg=COLOR_BORDER)
        self.border_frame.pack(fill="both", expand=True)
        
        self.entry = tk.Entry(
            self.border_frame,
            bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_TEXT_PRIMARY,
            relief="flat",
            bd=6,
            font=(FONT_FAMILY, 10),
            *args, **kwargs
        )
        self.entry.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.entry.bind("<KeyRelease>", self._on_keyrelease)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Down>", self._on_down_arrow)
        
        self.listbox_win = None
        self.listbox = None
        self.listbox_items = []

    def _on_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
            
        value = self.entry.get().strip()
        if not value:
            self._hide_autocomplete()
            return
            
        matches = []
        for food in self.food_dict:
            if value.lower() in food.lower():
                matches.append(food)
                
        if matches:
            self._show_autocomplete(matches)
        else:
            self._hide_autocomplete()

    def _show_autocomplete(self, matches):
        if not self.listbox_win:
            self.listbox_win = tk.Toplevel(self.winfo_toplevel())
            self.listbox_win.wm_overrideredirect(True)
            
            self.listbox = tk.Listbox(
                self.listbox_win,
                bg=COLOR_INPUT_BG,
                fg=COLOR_TEXT_PRIMARY,
                selectbackground=COLOR_ACCENT,
                selectforeground=COLOR_CARD,
                relief="flat",
                bd=1,
                highlightthickness=0,
                font=(FONT_FAMILY, 10)
            )
            self.listbox.pack(fill="both", expand=True)
            self.listbox.bind("<Double-Button-1>", self._on_select)
            self.listbox.bind("<Return>", self._on_select)
            
        self.listbox.delete(0, tk.END)
        self.listbox_items = matches[:6]
        for item in self.listbox_items:
            self.listbox.insert(tk.END, item)
            
        self.update_listbox_position()

    def update_listbox_position(self):
        if not self.listbox_win:
            return
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        w = self.entry.winfo_width()
        h = min(130, len(self.listbox_items) * 22 + 4)
        self.listbox_win.geometry(f"{w}x{h}+{x}+{y}")
        self.listbox_win.deiconify()
        self.listbox_win.lift()

    def _hide_autocomplete(self):
        if self.listbox_win:
            self.listbox_win.withdraw()

    def _on_focus_out(self, event):
        self.after(200, self._check_focus_and_hide)

    def _check_focus_and_hide(self):
        try:
            focus = self.winfo_toplevel().focus_get()
            if self.listbox and focus != self.listbox and focus != self.entry:
                self._hide_autocomplete()
        except Exception:
            self._hide_autocomplete()

    def _on_down_arrow(self, event):
        if self.listbox and self.listbox_win.winfo_viewable():
            self.listbox.focus_set()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    def _on_select(self, event=None):
        if not self.listbox:
            return
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            food_name = self.listbox_items[index]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, food_name)
            self._hide_autocomplete()
            self.on_select_callback(food_name, self.food_dict[food_name])

    def get(self):
        return self.entry.get()

    def delete(self, first, last=None):
        self.entry.delete(first, last)

    def insert(self, index, string):
        self.entry.insert(index, string)


# ==============================================================================
# 3. SCROLLABLE SIDEBAR FRAME WIDGET
# ==============================================================================
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=kwargs.get("bg", COLOR_SIDEBAR))
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get("bg", COLOR_SIDEBAR))

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas, scrollbar, and scrollable frame
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollbar.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)

    def bind_mousewheel_recursive(self, widget):
        """Recursively binds the mouse wheel scroll event to the widget and all its children."""
        widget.bind("<MouseWheel>", self._on_mousewheel)
        try:
            widget.bind("<Button-4>", self._on_mousewheel)
            widget.bind("<Button-5>", self._on_mousewheel)
        except Exception:
            pass
        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        import platform
        num = getattr(event, "num", 0)
        if num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            delta = getattr(event, "delta", 0)
            if platform.system() == "Darwin":
                # Adjust macOS scroll speed factor
                self.canvas.yview_scroll(int(-3 * delta), "units")
            else:
                self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")


# ==============================================================================
# 4. MAIN APP IMPLEMENTATION
# ==============================================================================
class DietPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("30일 다이어트 다이어리")
        
        # Center the window
        width = 1100
        height = 760
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        # File paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, "diet_data.json")
        self.photos_dir = os.path.join(self.base_dir, "diet_photos")
        
        if not os.path.exists(self.photos_dir):
            os.makedirs(self.photos_dir)

        # Application state
        self.start_date = None
        self.dates = []
        self.selected_date = None
        self.diet_data = {}
        self.image_cache = {}

        self.load_data()
        self.target_calories = self.diet_data.get("target_calories", 1800)
        self.generate_dates()

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        if today_str in self.dates:
            self.selected_date = today_str
        else:
            self.selected_date = self.dates[0]

        self.build_ui()
        self.refresh_ui()
        self.root.after(100, self.scroll_to_selected)

    # --------------------------------------------------------------------------
    # DATA & FILE MANAGEMENT
    # --------------------------------------------------------------------------
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.diet_data = json.load(f)
                    self.start_date = datetime.datetime.strptime(
                        self.diet_data.get("start_date"), "%Y-%m-%d"
                    ).date()
            except Exception as e:
                print(f"Error loading JSON data: {e}")
                self.initialize_empty_data()
        else:
            self.initialize_empty_data()

    def initialize_empty_data(self):
        self.start_date = datetime.date.today()
        self.diet_data = {
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "target_calories": 1800,
            "days": {}
        }
        self.save_data()

    def save_data(self):
        try:
            self.diet_data["target_calories"] = self.target_calories
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.diet_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("오류", f"데이터 저장에 실패했습니다:\n{e}")

    def generate_dates(self):
        self.dates = []
        today = datetime.date.today()
        # Generate 180 days before today and 180 days after today (total 361 days)
        for i in range(-180, 181):
            d = today + datetime.timedelta(days=i)
            self.dates.append(d.strftime("%Y-%m-%d"))
            
        # Also ensure any dates that have data in JSON are included
        if "days" in self.diet_data:
            for date_str in self.diet_data["days"]:
                if date_str not in self.dates:
                    self.dates.append(date_str)
                    
        # Sort dates chronologically
        self.dates.sort()

    # --------------------------------------------------------------------------
    # CALORIE & PHOTO HELPER LOGIC
    # --------------------------------------------------------------------------
    def get_day_total_calories(self, date_str):
        day_data = self.diet_data.get("days", {}).get(date_str, {})
        meals = day_data.get("meals", {})
        total = 0
        for meal in ("breakfast", "lunch", "dinner"):
            for item in meals.get(meal, []):
                total += item.get("calories", 0)
        return total

    def add_food_item(self, meal_type, food_name, calories):
        if not food_name.strip():
            messagebox.showwarning("입력 오류", "음식 이름을 입력해 주세요.")
            return

        try:
            calories = int(calories)
        except ValueError:
            messagebox.showwarning("입력 오류", "칼로리는 숫자 형식이어야 합니다.")
            return

        days_data = self.diet_data.setdefault("days", {})
        day_data = days_data.setdefault(self.selected_date, {})
        meals = day_data.setdefault("meals", {})
        meal_items = meals.setdefault(meal_type, [])

        meal_items.append({
            "food": food_name.strip(),
            "calories": calories
        })

        self.save_data()
        self.refresh_ui()

    def delete_food_item(self, meal_type, idx):
        try:
            meal_items = self.diet_data["days"][self.selected_date]["meals"][meal_type]
            meal_items.pop(idx)
            self.save_data()
            self.refresh_ui()
        except Exception as e:
            print(f"Error deleting item: {e}")

    def update_photo(self):
        file_path = filedialog.askopenfilename(
            title="식단 이미지 파일 선택",
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()
        dest_filename = f"{self.selected_date}{ext}"
        dest_path = os.path.join(self.photos_dir, dest_filename)

        try:
            shutil.copy2(file_path, dest_path)
            
            days_data = self.diet_data.setdefault("days", {})
            day_data = days_data.setdefault(self.selected_date, {})
            day_data["photo_path"] = os.path.relpath(dest_path, self.base_dir)
            
            if self.selected_date in self.image_cache:
                del self.image_cache[self.selected_date]

            self.save_data()
            self.refresh_ui()
        except Exception as e:
            messagebox.showerror("오류", f"사진 복사에 실패했습니다:\n{e}")

    def delete_photo(self):
        day_data = self.diet_data.get("days", {}).get(self.selected_date, {})
        photo_rel_path = day_data.get("photo_path")
        if not photo_rel_path:
            return

        photo_abs_path = os.path.join(self.base_dir, photo_rel_path)
        if os.path.exists(photo_abs_path):
            try:
                os.remove(photo_abs_path)
            except Exception as e:
                print(f"Failed to remove file: {e}")

        day_data["photo_path"] = None
        if self.selected_date in self.image_cache:
            del self.image_cache[self.selected_date]

        self.save_data()
        self.refresh_ui()

    def update_target_calories(self):
        try:
            val = int(self.target_entry.get())
            if val <= 0:
                raise ValueError
            self.target_calories = val
            self.save_data()
            self.refresh_ui()
            messagebox.showinfo("알림", f"하루 목표 칼로리가 {val} kcal로 변경되었습니다.")
        except ValueError:
            messagebox.showwarning("입력 오류", "칼로리는 양의 정수로 입력해 주세요.")
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, str(self.target_calories))

    # --------------------------------------------------------------------------
    # UI CONSTRUCTION
    # --------------------------------------------------------------------------
    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            troughcolor=COLOR_SIDEBAR,
            background=COLOR_BORDER,
            bordercolor=COLOR_SIDEBAR,
            arrowcolor=COLOR_TEXT_MUTED
        )

        # 1. Sidebar Frame
        self.sidebar_frame = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=280)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Typographic Logo Label
        logo_label = tk.Label(
            self.sidebar_frame,
            text="3 0   D A Y   D I E T",
            font=(FONT_FAMILY, 14, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_SIDEBAR,
            pady=20
        )
        logo_label.pack(fill="x")

        # Target Calorie Config
        target_panel = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR, padx=18, pady=10)
        target_panel.pack(fill="x")
        
        target_lbl = tk.Label(
            target_panel,
            text="일일 목표 권장 칼로리",
            font=(FONT_FAMILY, 9, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SIDEBAR
        )
        target_lbl.pack(anchor="w", pady=(0, 5))

        target_input_sub = tk.Frame(target_panel, bg=COLOR_SIDEBAR)
        target_input_sub.pack(fill="x")

        # Subtle elegant border for target entry
        target_border = tk.Frame(target_input_sub, bg=COLOR_BORDER)
        target_border.pack(side="left", fill="x", expand=True)

        self.target_entry = tk.Entry(
            target_border,
            bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_TEXT_PRIMARY,
            relief="flat",
            bd=5,
            width=12,
            font=(FONT_FAMILY, 10, "bold")
        )
        self.target_entry.pack(fill="both", expand=True, padx=1, pady=1)
        self.target_entry.insert(0, str(self.target_calories))

        target_btn = tk.Button(
            target_input_sub,
            text="설정",
            bg=COLOR_ACCENT,
            fg=COLOR_CARD,
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_CARD,
            relief="flat",
            font=(FONT_FAMILY, 9, "bold"),
            bd=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.update_target_calories
        )
        target_btn.pack(side="right", padx=(8, 0))

        # Fine divider line
        separator = tk.Frame(self.sidebar_frame, bg=COLOR_BORDER, height=1)
        separator.pack(fill="x", padx=18, pady=12)

        # Dates List Header
        days_title = tk.Label(
            self.sidebar_frame,
            text="식단 일지 타임라인",
            font=(FONT_FAMILY, 10, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SIDEBAR,
            anchor="w",
            padx=18
        )
        days_title.pack(fill="x", pady=(0, 6))

        # Scrollable Sidebar list
        self.scroll_sidebar = ScrollableFrame(self.sidebar_frame, bg=COLOR_SIDEBAR)
        self.scroll_sidebar.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        self.day_buttons = {}
        self.refresh_sidebar_days()

        # 2. Right Main Panel
        self.main_panel = tk.Frame(self.root, bg=COLOR_BG, padx=22, pady=18)
        self.main_panel.pack(side="right", fill="both", expand=True)

        # Date Label Header
        self.header_frame = tk.Frame(self.main_panel, bg=COLOR_BG)
        self.header_frame.pack(fill="x", pady=(0, 15))

        self.date_label = tk.Label(
            self.header_frame,
            text="2026년 06월 02일 (화요일)",
            font=(FONT_FAMILY, 16, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG
        )
        self.date_label.pack(side="left", anchor="w")

        # Two Columns
        self.cols_frame = tk.Frame(self.main_panel, bg=COLOR_BG)
        self.cols_frame.pack(fill="both", expand=True)

        # Left Column (Borderless Photo Card + Progress statistics)
        self.left_col = tk.Frame(self.cols_frame, bg=COLOR_BG, width=340)
        self.left_col.pack(side="left", fill="both", padx=(0, 15))
        self.left_col.pack_propagate(False)

        # --- ELEGANT MODERN GALLERY IMAGE CONTAINER ---
        self.polaroid_frame = tk.Frame(
            self.left_col,
            bg=COLOR_CARD,
            bd=1,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=12,
            pady=12
        )
        self.polaroid_frame.pack(fill="x", pady=(0, 15))

        # Borderless modern photo canvas/label
        self.photo_display = tk.Label(
            self.polaroid_frame,
            bg=COLOR_INPUT_BG,
            cursor="hand2"
        )
        self.photo_display.pack(fill="x")
        self.photo_display.bind("<Button-1>", lambda _: self.update_photo())

        # Polaroid Footer with clean uppercase text
        self.polaroid_footer = tk.Label(
            self.polaroid_frame,
            text="2026 . 06 . 02  |  DAILY LOG",
            font=(FONT_FAMILY, 10, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD,
            pady=10
        )
        self.polaroid_footer.pack(fill="x")

        # Photo control buttons
        photo_btn_frame = tk.Frame(self.left_col, bg=COLOR_BG)
        photo_btn_frame.pack(fill="x", pady=(0, 15))

        self.btn_upload_photo = tk.Button(
            photo_btn_frame,
            text="이미지 선택",
            bg=COLOR_ACCENT,
            fg=COLOR_CARD,
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_CARD,
            relief="flat",
            bd=0,
            font=(FONT_FAMILY, 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.update_photo
        )
        self.btn_upload_photo.pack(side="left", expand=True, fill="x", padx=(0, 4))

        self.btn_delete_photo = tk.Button(
            photo_btn_frame,
            text="삭제",
            bg="#ECE8E1",
            fg=COLOR_RED,
            activebackground="#ECE8E1",
            activeforeground=COLOR_RED,
            relief="flat",
            bd=0,
            font=(FONT_FAMILY, 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.delete_photo
        )
        self.btn_delete_photo.pack(side="right", expand=True, fill="x", padx=(4, 0))

        # Progress Calorie Card (Sophisticated clean frame)
        self.progress_card = tk.Frame(
            self.left_col,
            bg=COLOR_CARD,
            bd=1,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=16,
            pady=16
        )
        self.progress_card.pack(fill="both", expand=True)

        self.cal_stat_title = tk.Label(
            self.progress_card,
            text="섭취량 및 진척도 통계",
            font=(FONT_FAMILY, 10, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_CARD
        )
        self.cal_stat_title.pack(anchor="w", pady=(0, 4))

        self.cal_ratio_label = tk.Label(
            self.progress_card,
            text="0 / 1800 kcal",
            font=(FONT_FAMILY, 14, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_CARD
        )
        self.cal_ratio_label.pack(anchor="w", pady=(0, 10))

        # Minimalist thin line Progress bar Canvas
        self.progress_canvas = tk.Canvas(
            self.progress_card,
            height=14,
            bg=COLOR_CARD,
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="x", pady=6)

        self.cal_feedback_label = tk.Label(
            self.progress_card,
            text="오늘 하루의 건강한 식단을 기록해 보세요.",
            font=(FONT_FAMILY, 9),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD,
            wraplength=280,
            justify="left"
        )
        self.cal_feedback_label.pack(anchor="w", pady=(12, 0))

        # Right Column (Breakfast, Lunch, Dinner scroll logs)
        self.right_col = tk.Frame(self.cols_frame, bg=COLOR_BG)
        self.right_col.pack(side="right", fill="both", expand=True)

        self.meals_scroll = ScrollableFrame(self.right_col, bg=COLOR_BG)
        self.meals_scroll.pack(fill="both", expand=True)

        self.meal_widgets = {}
        self.build_meal_cards(self.meals_scroll.scrollable_frame)

    def refresh_sidebar_days(self):
        """Draws clean timeline items dynamically."""
        for child in self.scroll_sidebar.scrollable_frame.winfo_children():
            child.destroy()
        self.day_buttons.clear()

        for date_str in self.dates:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            day_name = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
            display_date = f"{dt.month:02d}월 {dt.day:02d}일 ({day_name})"
            
            # Setup colors based on selection state
            is_selected = (date_str == self.selected_date)
            bg_col = COLOR_ACCENT if is_selected else COLOR_CARD
            border_col = COLOR_ACCENT if is_selected else COLOR_BORDER
            fg_primary = COLOR_CARD if is_selected else COLOR_TEXT_PRIMARY

            card = tk.Frame(
                self.scroll_sidebar.scrollable_frame,
                bg=bg_col,
                bd=1,
                highlightbackground=border_col,
                highlightthickness=1,
                padx=10,
                pady=10,
                cursor="hand2"
            )
            card.pack(fill="x", pady=4, padx=4)
            
            lbl_date = tk.Label(
                card,
                text=display_date,
                font=(FONT_FAMILY, 9, "bold"),
                fg=fg_primary,
                bg=bg_col,
                anchor="w",
                cursor="hand2"
            )
            lbl_date.pack(fill="x", side="top")

            info_frame = tk.Frame(card, bg=bg_col)
            info_frame.pack(fill="x", side="bottom", pady=(3, 0))

            lbl_cal = tk.Label(
                info_frame,
                text="",
                font=(FONT_FAMILY, 8),
                bg=bg_col,
                anchor="w",
                cursor="hand2"
            )
            lbl_cal.pack(side="left")

            lbl_photo = tk.Label(
                info_frame,
                text="",
                font=(FONT_FAMILY, 8),
                bg=bg_col,
                cursor="hand2"
            )
            lbl_photo.pack(side="right")

            # Bind hover events
            card.bind("<Enter>", lambda e, c=card: self._on_card_hover(c, True))
            card.bind("<Leave>", lambda e, c=card: self._on_card_hover(c, False))
            
            click_cb = lambda e, d=date_str: self.select_date(d)
            card.bind("<Button-1>", click_cb)
            lbl_date.bind("<Button-1>", click_cb)
            lbl_cal.bind("<Button-1>", click_cb)
            lbl_photo.bind("<Button-1>", click_cb)

            self.day_buttons[date_str] = {
                "card": card,
                "lbl_date": lbl_date,
                "lbl_cal": lbl_cal,
                "lbl_photo": lbl_photo
            }

            # Recursively bind mouse wheel scroll to the card and all its children
            self.scroll_sidebar.bind_mousewheel_recursive(card)

        self.scroll_sidebar.canvas.configure(scrollregion=self.scroll_sidebar.canvas.bbox("all"))

    def scroll_to_selected(self):
        """Scrolls the sidebar list to keep the selected date visible in focus."""
        self.root.update_idletasks()
        if self.selected_date in self.day_buttons:
            card = self.day_buttons[self.selected_date]["card"]
            y = card.winfo_y()
            total_height = self.scroll_sidebar.scrollable_frame.winfo_height()
            canvas_height = self.scroll_sidebar.canvas.winfo_height()
            
            if total_height > canvas_height:
                fraction = (y - canvas_height / 2 + card.winfo_height() / 2) / total_height
                fraction = max(0.0, min(1.0, fraction))
                self.scroll_sidebar.canvas.yview_moveto(fraction)

    def _on_card_hover(self, card_widget, is_hover):
        active_date_card = self.day_buttons[self.selected_date]["card"]
        if card_widget == active_date_card:
            return
        
        if is_hover:
            card_widget.configure(bg=COLOR_CARD_HOVER)
            for child in card_widget.winfo_children():
                child.configure(bg=COLOR_CARD_HOVER)
                for subchild in child.winfo_children():
                    subchild.configure(bg=COLOR_CARD_HOVER)
        else:
            card_widget.configure(bg=COLOR_CARD)
            for child in card_widget.winfo_children():
                child.configure(bg=COLOR_CARD)
                for subchild in child.winfo_children():
                    subchild.configure(bg=COLOR_CARD)

    def select_date(self, date_str):
        old_sel = self.selected_date
        self.selected_date = date_str
        
        # Restore old selected day styles to standard memo format
        if old_sel in self.day_buttons:
            self.day_buttons[old_sel]["card"].configure(bg=COLOR_CARD, highlightbackground=COLOR_BORDER)
            self.day_buttons[old_sel]["lbl_date"].configure(bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY)
            self.day_buttons[old_sel]["lbl_cal"].configure(bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
            self.day_buttons[old_sel]["lbl_photo"].configure(bg=COLOR_CARD, fg=COLOR_ACCENT)
            for child in self.day_buttons[old_sel]["card"].winfo_children():
                child.configure(bg=COLOR_CARD)
                for subchild in child.winfo_children():
                    subchild.configure(bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)

        # Highlight new day card with organic sage green theme
        self.day_buttons[date_str]["card"].configure(bg=COLOR_ACCENT, highlightbackground=COLOR_ACCENT)
        self.day_buttons[date_str]["lbl_date"].configure(bg=COLOR_ACCENT, fg=COLOR_CARD)
        self.day_buttons[date_str]["lbl_cal"].configure(bg=COLOR_ACCENT, fg=COLOR_CARD)
        self.day_buttons[date_str]["lbl_photo"].configure(bg=COLOR_ACCENT, fg=COLOR_CARD)
        for child in self.day_buttons[date_str]["card"].winfo_children():
            child.configure(bg=COLOR_ACCENT)
            for subchild in child.winfo_children():
                subchild.configure(bg=COLOR_ACCENT, fg=COLOR_CARD)

        self.refresh_ui()

    def build_meal_cards(self, parent):
        """Constructs Breakfast, Lunch, and Dinner logger cards with minimalist chic layout."""
        meal_types = [
            ("breakfast", "아 침 식 사", "#F3EFE9", COLOR_ACCENT), 
            ("lunch", "점 심 식 사", "#F3EFE9", COLOR_ACCENT),     
            ("dinner", "저 녁 식 사", "#F3EFE9", COLOR_ACCENT)     
        ]

        for meal_key, title, bg_col, text_col in meal_types:
            card = tk.Frame(
                parent,
                bg=COLOR_CARD,
                bd=1,
                highlightbackground=COLOR_BORDER,
                highlightthickness=1,
                padx=14,
                pady=14
            )
            card.pack(fill="x", pady=(0, 15))

            # Minimal Header band
            header = tk.Frame(card, bg=bg_col, padx=10, pady=6)
            header.pack(fill="x", pady=(0, 6))

            lbl_title = tk.Label(
                header,
                text=title,
                font=(FONT_FAMILY, 10, "bold"),
                fg=COLOR_TEXT_PRIMARY,
                bg=bg_col
            )
            lbl_title.pack(side="left")

            lbl_total = tk.Label(
                header,
                text="0 kcal",
                font=(FONT_FAMILY, 9, "bold"),
                fg=COLOR_TEXT_PRIMARY,
                bg=bg_col
            )
            lbl_total.pack(side="right")

            # Food items list
            items_frame = tk.Frame(card, bg=COLOR_CARD)
            items_frame.pack(fill="x", pady=4)

            # Input fields container
            input_frame = tk.Frame(card, bg=COLOR_CARD, pady=6)
            input_frame.pack(fill="x")

            lbl_food = tk.Label(input_frame, text="음식:", font=(FONT_FAMILY, 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
            lbl_food.grid(row=0, column=0, sticky="w", padx=(0, 4))
            
            on_select = lambda food, cals, mk=meal_key: self._on_food_suggested(mk, food, cals)
            entry_food = AutocompleteEntry(input_frame, FOOD_DICT, on_select, width=18)
            entry_food.grid(row=0, column=1, sticky="we", padx=(0, 8))

            lbl_cal = tk.Label(input_frame, text="kcal:", font=(FONT_FAMILY, 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
            lbl_cal.grid(row=0, column=2, sticky="w", padx=(0, 4))

            cal_border = tk.Frame(input_frame, bg=COLOR_BORDER)
            cal_border.grid(row=0, column=3, sticky="we", padx=(0, 8))

            entry_cal = tk.Entry(
                cal_border,
                bg=COLOR_INPUT_BG,
                fg=COLOR_TEXT_PRIMARY,
                insertbackground=COLOR_TEXT_PRIMARY,
                relief="flat",
                bd=6,
                width=6,
                font=(FONT_FAMILY, 10)
            )
            entry_cal.pack(fill="both", expand=True, padx=1, pady=1)

            # Minimal Add button
            btn_add = tk.Button(
                input_frame,
                text="추가",
                bg=COLOR_ACCENT,
                fg=COLOR_CARD,
                activebackground=COLOR_ACCENT_HOVER,
                activeforeground=COLOR_CARD,
                relief="flat",
                bd=0,
                font=(FONT_FAMILY, 9, "bold"),
                cursor="hand2",
                padx=12,
                pady=5,
                command=lambda mk=meal_key: self._on_add_clicked(mk)
            )
            btn_add.grid(row=0, column=4, sticky="e")

            # Bind Return key on calorie input box
            entry_cal.bind("<Return>", lambda e, mk=meal_key: self._on_add_clicked(mk))

            input_frame.columnconfigure(1, weight=3)
            input_frame.columnconfigure(3, weight=1)

            self.meal_widgets[meal_key] = {
                "lbl_total": lbl_total,
                "items_frame": items_frame,
                "entry_food": entry_food,
                "entry_cal": entry_cal
            }

            # Recursively bind mouse wheel scroll to the meal card and all its children
            self.meals_scroll.bind_mousewheel_recursive(card)

    def _on_food_suggested(self, meal_key, food_name, calories):
        widget_set = self.meal_widgets[meal_key]
        widget_set["entry_cal"].delete(0, tk.END)
        widget_set["entry_cal"].insert(0, str(calories))

    def _on_add_clicked(self, meal_key):
        widget_set = self.meal_widgets[meal_key]
        food = widget_set["entry_food"].get()
        cals = widget_set["entry_cal"].get()
        
        self.add_food_item(meal_key, food, cals)
        
        widget_set["entry_food"].delete(0, tk.END)
        widget_set["entry_cal"].delete(0, tk.END)

    # --------------------------------------------------------------------------
    # REFRESH / DYNAMIC UPDATE FUNCTIONS
    # --------------------------------------------------------------------------
    def refresh_ui(self):
        dt = datetime.datetime.strptime(self.selected_date, "%Y-%m-%d").date()
        day_name = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][dt.weekday()]
        
        is_today_str = ""
        if dt == datetime.date.today():
            is_today_str = " (오늘)"
        self.date_label.configure(text=f"{dt.year}년 {dt.month:02d}월 {dt.day:02d}일 {day_name}{is_today_str}")
        self.polaroid_footer.configure(text=f"{dt.year} . {dt.month:02d} . {dt.day:02d}  |  DAILY LOG")

        # Update sidebar items
        for date_str in self.dates:
            total_cal = self.get_day_total_calories(date_str)
            day_data = self.diet_data.get("days", {}).get(date_str, {})
            has_photo = day_data.get("photo_path") is not None
            
            if date_str == self.selected_date:
                self.day_buttons[date_str]["lbl_cal"].configure(text=f"{total_cal} / {self.target_calories} kcal", fg=COLOR_CARD)
                self.day_buttons[date_str]["lbl_photo"].configure(text="[사진]" if has_photo else "", fg=COLOR_CARD)
            else:
                self.day_buttons[date_str]["lbl_cal"].configure(text=f"{total_cal} / {self.target_calories} kcal", fg=COLOR_TEXT_MUTED)
                self.day_buttons[date_str]["lbl_photo"].configure(text="[사진]" if has_photo else "", fg=COLOR_ACCENT)

        self.refresh_photo_widget()
        self.refresh_meal_widgets()
        self.refresh_progress_canvas()

    def refresh_photo_widget(self):
        day_data = self.diet_data.get("days", {}).get(self.selected_date, {})
        photo_rel_path = day_data.get("photo_path")
        
        if photo_rel_path:
            photo_abs_path = os.path.join(self.base_dir, photo_rel_path)
            if os.path.exists(photo_abs_path):
                if self.selected_date in self.image_cache:
                    tk_img = self.image_cache[self.selected_date]
                else:
                    try:
                        img = Image.open(photo_abs_path)
                        img = ImageOps.exif_transpose(img)
                        img.thumbnail((290, 180), Image.Resampling.LANCZOS)
                        tk_img = ImageTk.PhotoImage(img)
                        self.image_cache[self.selected_date] = tk_img
                    except Exception as e:
                        print(f"Error loading image: {e}")
                        photo_rel_path = None
            else:
                photo_rel_path = None
        
        if photo_rel_path and self.selected_date in self.image_cache:
            self.photo_display.configure(
                image=self.image_cache[self.selected_date],
                text=""
            )
            self.photo_display.pack_configure(ipady=0)
            self.btn_delete_photo.configure(state="normal", bg="#ECE8E1", fg=COLOR_RED)
        else:
            self.photo_display.configure(
                image="",
                text="식단 이미지를 등록해 주세요.\n(마우스 클릭)",
                font=(FONT_FAMILY, 9),
                fg=COLOR_TEXT_MUTED,
                justify="center"
            )
            self.photo_display.pack_configure(ipady=60)
            self.btn_delete_photo.configure(state="disabled", bg="#ECE8E1", fg=COLOR_TEXT_MUTED)

    def refresh_meal_widgets(self):
        day_data = self.diet_data.get("days", {}).get(self.selected_date, {})
        meals = day_data.get("meals", {})

        for meal_key in ("breakfast", "lunch", "dinner"):
            widget_set = self.meal_widgets[meal_key]
            
            items_frame = widget_set["items_frame"]
            for child in items_frame.winfo_children():
                child.destroy()

            meal_items = meals.get(meal_key, [])
            total_meal_cals = sum(item.get("calories", 0) for item in meal_items)
            
            widget_set["lbl_total"].configure(text=f"{total_meal_cals} kcal")

            if not meal_items:
                lbl_empty = tk.Label(
                    items_frame,
                    text="기록된 식단이 없습니다.",
                    font=(FONT_FAMILY, 9, "italic"),
                    fg=COLOR_TEXT_MUTED,
                    bg=COLOR_CARD,
                    anchor="w"
                )
                lbl_empty.pack(fill="x", pady=4)
            else:
                for idx, item in enumerate(meal_items):
                    item_row = tk.Frame(items_frame, bg=COLOR_CARD)
                    item_row.pack(fill="x", pady=3)

                    lbl_name = tk.Label(
                        item_row,
                        text=f"  {item['food']}",
                        font=(FONT_FAMILY, 10),
                        fg=COLOR_TEXT_PRIMARY,
                        bg=COLOR_CARD,
                        anchor="w"
                    )
                    lbl_name.pack(side="left")

                    del_btn_cb = lambda mk=meal_key, i=idx: self.delete_food_item(mk, i)
                    btn_del = tk.Button(
                        item_row,
                        text="✕",
                        font=(FONT_FAMILY, 8),
                        fg=COLOR_TEXT_MUTED,
                        activeforeground=COLOR_RED,
                        bg=COLOR_CARD,
                        activebackground=COLOR_CARD,
                        relief="flat",
                        bd=0,
                        padx=6,
                        pady=2,
                        cursor="hand2",
                        command=del_btn_cb
                    )
                    btn_del.pack(side="right")

                    lbl_cal = tk.Label(
                        item_row,
                        text=f"{item['calories']} kcal",
                        font=(FONT_FAMILY, 9, "bold"),
                        fg=COLOR_ACCENT,
                        bg=COLOR_CARD
                    )
                    lbl_cal.pack(side="right", padx=8)

                    # Recursively bind mouse wheel scroll to the dynamic food item row and all its children
                    self.meals_scroll.bind_mousewheel_recursive(item_row)

    def refresh_progress_canvas(self):
        """Draws a sleek, modern wellness line progress bar on Canvas."""
        total_cals = self.get_day_total_calories(self.selected_date)
        target = self.target_calories
        
        pct = (total_cals / target) if target > 0 else 0
        pct_display = min(1.0, pct)
        
        # Muted sophisticated colors
        if pct == 0:
            bar_color = COLOR_BORDER
        elif pct <= 0.85:
            bar_color = COLOR_BLUE      # Pale sage green
        elif pct <= 1.05:
            bar_color = COLOR_ACCENT    # Muted organic sage green
        else:
            bar_color = COLOR_RED       # Muted dusty rose-red

        self.cal_ratio_label.configure(text=f"{total_cals} / {target} kcal  ({int(pct*100)}%)")

        # Sophisticated & formal feedback warnings
        if pct == 0:
            feedback = "오늘 하루의 건강한 식단을 기록해 보세요."
            self.cal_feedback_label.configure(fg=COLOR_TEXT_MUTED)
        elif pct < 0.85:
            feedback = f"권장 칼로리 도달을 위해 {target - total_cals} kcal 더 섭취 가능합니다."
            self.cal_feedback_label.configure(fg=COLOR_ACCENT)
        elif pct <= 1.05:
            feedback = "목표 칼로리 섭취량 범위에 정확히 도달했습니다. 훌륭한 식단입니다."
            self.cal_feedback_label.configure(fg=COLOR_ACCENT)
        else:
            feedback = f"주의: 일일 섭취 기준량을 초과했습니다. ({total_cals - target} kcal 초과)"
            self.cal_feedback_label.configure(fg=COLOR_RED)
            
        self.cal_feedback_label.configure(text=feedback)

        # Draw line progress bar on Canvas
        self.progress_canvas.delete("all")
        self.root.update_idletasks()
        w = self.progress_canvas.winfo_width()
        h = self.progress_canvas.winfo_height()

        if w <= 1:
            w = 260
        if h <= 1:
            h = 14

        # Background track (thick rounded line)
        self.progress_canvas.create_line(
            8, h/2, w - 8, h/2,
            width=6,
            fill=COLOR_BORDER,
            capstyle="round"
        )
        
        # Progress track (thick rounded line)
        if pct_display > 0:
            self.progress_canvas.create_line(
                8, h/2, 8 + (w - 16) * pct_display, h/2,
                width=6,
                fill=bar_color,
                capstyle="round"
            )


# ==============================================================================
# 5. EXECUTION ENTRY POINT
# ==============================================================================
def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "windowingsystem")
    except Exception:
        pass
    app = DietPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
