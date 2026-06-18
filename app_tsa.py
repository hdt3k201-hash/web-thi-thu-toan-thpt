import streamlit as st

# Cấu hình giao diện trang web trải rộng toàn màn hình
st.set_page_config(page_title="Hệ Thống Thi TSA - Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI TSA (Thầy thêm đề 3, 4, 5... tương tự cấu trúc này)
# =========================================================================
TSA_EXAMS_BANK = {
    "de_tsa_1": {
        "title": "Đề TSA 01: Khảo sát chất lượng Toán Tư Duy",
        "pdf_id": "ID_FILE_DE_TSA_1",  # Thay bằng ID file đề 1 trên Drive
        "giai_id": "ID_FILE_GIAI_TSA_1", # Thay bằng ID file giải 1
        "key_p1": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C"],
        "key_p2": {
            16: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
            17: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            18: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Sai"},
            19: {"a": "Sai", "b": "Sai", "c": "Đúng", "d": "Đúng"},
            20: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["15", "0", "-2", "3.14", "10", "5", "100", "0.5", "-1", "7"],
        "options_p4": [ # Kho từ khóa của đề số 1
            "--- Bấm để chọn phương án ---",
            "Đồng biến trên R", "Nghịch biến trên R", "Có cực đại và cực tiểu", 
            "Tập xác định D = R \ {1}", "Tiệm cận đứng x = 1", "Tiệm cận ngang y = 2"
        ],
        "key_p4": [
            "Đồng biến trên R", "Tiệm cận đứng x = 1", "Tập xác định D = R \ {1}", 
            "Có cực đại và cực tiểu", "Nghịch biến trên R", "Tiệm cận ngang y = 2",
            "Đồng biến trên R", "Tiệm cận đứng x = 1", "Tập xác định D = R \ {1}", "Có cực đại và cực tiểu"
        ]
    },
    "de_tsa_2": {
        "title": "Đề TSA 02: Luyện đề Đánh giá Tư duy Bách Khoa",
        "pdf_id": "ID_FILE_DE_TSA_2",  # Thay bằng ID file đề 2 trên Drive
        "giai_id": "ID_FILE_GIAI_TSA_2", # Thay bằng ID file giải 2
        "key_p1": ["B", "C", "A", "D", "B", "C", "A", "D", "B", "C", "A", "D", "B", "C", "A"],
        "key_p2": {
            16: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            17: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
            18: {"a": "Sai", "b": "Sai", "c": "Đúng", "d": "Đúng"},
            19: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Sai"},
            20: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["5", "10", "1", "0", "-5", "2", "50", "0.25", "3", "8"],
        "options_p4": [ # Kho từ khóa của đề số 2 (có thể hoàn toàn khác đề 1)
            "--- Bấm để chọn phương án ---",
            "Hình chóp tam giác đều", "Mặt cầu ngoại tiếp", "Thể tích khối lăng trụ", 
            "Bán kính R = 5", "Đường cao h = 3"
        ],
        "key_p4": [
            "Hình chóp tam giác đều", "Mặt cầu ngoại tiếp", "Thể tích khối lăng trụ", 
            "Bán kính R = 5", "Đường cao h = 3", "Hình chóp tam giác đều",
            "Mặt cầu ngoại tiếp", "Thể tích khối lăng trụ", "Bán kính R = 5", "Đường cao h = 3"
        ]
    }
}

st.title("🎯 HỆ THỐNG THI ĐÁNH GIÁ TƯ DUY (TSA) MÔN TOÁN")
st.markdown("---")

# MENU CHỌN ĐỀ THI
st.sidebar.header("🗂️ DANH SÁCH ĐỀ THI TSA")
selected_exam_key = st.sidebar.selectbox(
    "Học sinh chọn đề thi tại đây:",
    options=list(TSA_EXAMS_BANK.keys()),
    format_func=lambda x: TSA_EXAMS_BANK[x]["title"]
)

# Lấy dữ liệu của đề đang được chọn
current_exam = TSA_EXAMS_BANK[selected_exam_key]
pdf_link = f"https://drive.google.com/file/d/{current_exam['pdf_id']}/preview"
giai_link = f"https://drive.google.com/file/d/{current_exam['giai_id']}/view"

col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Nội dung Đề thi TSA")
    st.components.v1.iframe(pdf_link, height=1400)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # Đồng hồ đếm ngược 120 phút tự động reset khi đổi đề
    timer_code = f"""
    <div id="timer_{selected_exam_key}" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; margin-bottom: 15px;">
        ⏳ 60:00
    </div>
    <script>
    var time_in_minutes = 60;
    var deadline = new Date(Date.parse(new Date()) + time_in_minutes * 60 * 1000);
    function update_clock(){{
        var t = Date.parse(deadline) - Date.parse(new Date());
        var seconds = Math.floor( (t/1000) % 60 );
        var total_minutes = Math.floor(t / 1000 / 60);
        var clock = document.getElementById('timer_{selected_exam_key}');
        if(!clock) return;
        if(t <= 0){{
            clock.innerHTML = "HẾT GIỜ LÀM BÀI!";
            clock.style.backgroundColor = "black";
        }} else {{
            var m = total_minutes < 10 ? "0" + total_minutes : total_minutes;
            var s = seconds < 10 ? "0" + seconds : seconds;
            clock.innerHTML = "⏳ " + m + ":" + s;
        }}
    }}
    setInterval(update_clock, 1000);
    </script>
    """
    st.components.v1.html(timer_code, height=75)
    
    with st.form(key=f"form_{selected_exam_key}"):
        
        # PHẦN I
        st.markdown("### **PHẦN I. Trắc nghiệm nhiều phương án (Câu 1 - 15)**")
        p1_answers = {}
        for i in range(1, 16):
            p1_answers[i] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None, key=f"p1_c{i}_{selected_exam_key}")
        
        st.markdown("---")
        
        # PHẦN II
        st.markdown("### **PHẦN II. Trắc nghiệm Đúng / Sai (Câu 16 - 20)**")
        p2_answers = {}
        for i in range(16, 21):
            st.markdown(f"**Câu {i}:**")
            p2_answers[i] = {}
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a: p2_answers[i]["a"] = st.radio("Ý a)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_a_{selected_exam_key}")
            with col_b: p2_answers[i]["b"] = st.radio("Ý b)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_b_{selected_exam_key}")
            with col_c: p2_answers[i]["c"] = st.radio("Ý c)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_c_{selected_exam_key}")
            with col_d: p2_answers[i]["d"] = st.radio("Ý d)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_d_{selected_exam_key}")
            st.write("")
        
        st.markdown("---")
        
        # PHẦN III
        st.markdown("### **PHẦN III. Điền đáp án (Câu 21 - 30)**")
        p3_answers = {}
        for i in range(21, 31):
            p3_answers[i] = st.text_input(f"Câu {i}: Nhập kết quả của bạn", key=f"p3_c{i}_{selected_exam_key}")
            
        st.markdown("---")
        
        # PHẦN IV
        st.markdown("### **PHẦN IV. Kéo thả phương án (Câu 31 - 40)**")
        p4_answers = {}
        for i in range(31, 41):
            p4_answers[i] = st.selectbox(f"Vị trí ô trống Câu {i}:", options=current_exam["options_p4"], key=f"p4_c{i}_{selected_exam_key}")

        st.markdown("---")
        submitted = st.form_submit_button("NỘP BÀI & CHẤM ĐIỂM TỰ ĐỘNG", use_container_width=True)

    # ==========================================
    # LOGIC CHẤM ĐIỂM TỰ ĐỘNG
    # ==========================================
    if submitted:
        correct_p1 = sum(1 for i in range(1, 16) if p1_answers[i] == current_exam["key_p1"][i-1])
        
        correct_p2_y = 0
        for i in range(16, 21):
            for branch in ["a", "b", "c", "d"]:
                if p2_answers[i][branch] == current_exam["key_p2"][i][branch]:
                    correct_p2_y += 1
                    
        correct_p3 = sum(1 for i in range(21, 31) if p3_answers[i].strip() == str(current_exam["key_p3"][i-21]))
        correct_p4 = sum(1 for i in range(31, 41) if p4_answers[i] == current_exam["key_p4"][i-31])
                
        total_correct_items = correct_p1 + correct_p2_y + correct_p3 + correct_p4
        total_items = 15 + 20 + 10 + 10 # Tổng 55 thao tác
        
        st.success("🎉 Bạn đã hoàn thành bài thi! Dưới đây là thống kê kết quả của bạn:")
        st.balloons()
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Phần I (Trắc nghiệm)", f"{correct_p1} / 15 câu")
            st.metric("Phần III (Điền đáp án)", f"{correct_p3} / 10 câu")
        with col_res2:
            st.metric("Phần II (Đúng/Sai)", f"{correct_p2_y} / 20 ý")
            st.metric("Phần IV (Kéo thả)", f"{correct_p4} / 10 câu")
            
        st.markdown(f"### 🏆 TỔNG CỘNG: Đạt {total_correct_items} / {total_items} thao tác đúng!")
        
        if current_exam['giai_id']:
            st.info(f"👉 [BẤM VÀO ĐÂY ĐỂ XEM FILE LỜI GIẢI CHI TIẾT PDF]({giai_link})")
