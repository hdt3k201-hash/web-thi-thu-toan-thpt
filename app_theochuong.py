import streamlit as st

# Cấu hình giao diện trang web trải rộng toàn màn hình
st.set_page_config(page_title="Hệ Thống Thi Thử - Lớp Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI & ĐÁP ÁN (Thầy có thể thêm đề số 3, 4, 5... tương tự bên dưới)
# =========================================================================
EXAMS_BANK = {
    "de_số_1": {
        "title": "Đề số 01: Ôn tập đơn điệu và cực trị của hàm số 2026",
        "pdf_id": "1u07mDClzYGhdjGmdziBm0Xbwqg6OxmMn",  # Thay bằng ID file ĐỀ trên Google Drive của thầy
        "giai_id": "19iIiwKO5bOyTWQq4g8Hh6c9d5nPlTVlD",  # Thay bằng ID file GIẢI CHI TIẾT trên Drive
        "key_p1": ["C", "C", "C", "B", "A", "B", "D", "B", "D", "A", "C", "B"],  # Đáp án 12 câu Phần I
        "key_p2": {  # Đáp án 4 câu Phần II (Đúng hoặc Sai cho các ý a, b, c, d)
            1: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            2: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Sai"},
            3: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
            4: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
        },
        "key_p3": ["6", "-35", "3", "3", "20", "1.61"]  # Đáp số chuẩn của 6 câu Phần III
    },
    "de_số_2": {
        "title": "Đề số 02: Ôn tập đơn điệu và cực trị của hàm số 2026",
        "pdf_id": "1IJNKbYvKU0ZfjYl6JRL4vouz24XHF0mQ",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "1b_i9-y1RyoUwkvqKyc51TrCHXlA6uj-8",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["B", "D", "B", "D", "A", "D", "C", "B", "A", "C", "A", "C"],
        "key_p2": {
            1: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            2: {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Sai"},
            3: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            4: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Sai"},
        },
        "key_p3": ["-3", "1.41", "6.71", "52", "0", "158"]
    },
    "de_số_3": {
        "title": "Đề số 03: Ôn tập đơn điệu và cực trị của hàm số 2026",
        "pdf_id": "1UMbuWIPvaMN3IXN9i94QYTlzGwq1UzYx",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "12CCEAEbGRu04xJUYvYyK89eMJndmRyPz",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["A", "C", "C", "A", "B", "B", "A", "A", "B", "C", "C", "B"],
        "key_p2": {
            1: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            2: {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Sai"},
            3: {"a": "Đúng", "b": "Đúng", "c": "Đúng", "d": "Sai"},
            4: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["2", "2", "28", "52", "10.6", "80"]
    },
    "de_số_4": {
        "title": "Đề số 04: Giá trị lớn nhất ; nhỏ nhất của hàm số 2026",
        "pdf_id": "1bH_wKqKQ1dqEpot9RPlK_9AiEm8xttsn",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "1aVISUkmQvC6ui6tTMZfDGbl9c0rpcFWT",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["D", "B", "A", "A", "D", "D", "D", "B", "A", "A", "A", "B"],
        "key_p2": {
            1: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            2: {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Đúng"},
            3: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
            4: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["3", "0.37", "1.125", "2.4", "7200", "2.34"]
    },
    "de_số_5": {
        "title": "Đề số 05: Giá trị lớn nhất ; nhỏ nhất của hàm số 2026",
        "pdf_id": "1e4cljNfSpxItFbAOuDAsWVBCjFDJ6TA1",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "1r8C2pi4-NdrJQzXwZ4WyOXT4J5AJOcwW",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["D", "A", "A", "A", "A", "B", "C", "B", "D", "C", "B", "A"],
        "key_p2": {
            1: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
            2: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            3: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
            4: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["15", "11.3", "59", "3", "7200", "30"]
    },
    "de_số_6": {
        "title": "Đề số 06: Giá trị lớn nhất ; nhỏ nhất của hàm số 2026",
        "pdf_id": "16WPFLqC5AE98daLiVf_XmgWXaH-jZA2Q",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "1CBsmjE7L3uB9VeeUe8y6_Po4eHl1Pmv1",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["C", "D", "A", "A", "D", "A", "C", "A", "D", "C", "B", "A"],
        "key_p2": {
            1: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
            2: {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Đúng"},
            3: {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Sai"},
            4: {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Sai"},
        },
        "key_p3": ["2.4", "7200", "2.34", "3", "2", "100"]
    },
     "de_số_7": {
        "title": "Đề số 07:Đường tiệm cận của hàm số 2026",
        "pdf_id": "1CBsmjE7L3uB9VeeUe8y6_Po4eHl1Pmv1",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "1ZXtgPr6dFBwoUV_-nQBEtjG_6mCFq2YN",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["C", "D", "A", "C", "C", "A", "A", "B", "C", "D", "D", "C"],
        "key_p2": {
            1: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            2: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Sai"},
            3: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Sai"},
            4: {"a": "Đúng", "b": "Đúng", "c": "Đúng", "d": "Sai"},
        },
        "key_p3": ["-298", "150", "2", "2", "2", "29"]
    },
     "de_số_8": {
        "title": "Đề số 08:Đường tiệm cận của hàm số 2026",
        "pdf_id": "1P7YxIDaMuKS2ztT__FcrsvjHIv1MhHK9",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "1XY21SD_m9mvtFwQc0lSi_Jhm_rPyZAio",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["B", "C", "B", "A", "B", "A", "D", "D", "D", "B", "C", "A"],
        "key_p2": {
            1: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
            2: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Sai"},
            3: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            4: {"a": "Sai", "b": "Sai", "c": "Đúng", "d": "Sai"},
        },
        "key_p3": ["5", "1", "3", "-9", "2", "1"]
    },
    "de_số_9": {
        "title": "Đề số 09:Đường tiệm cận của hàm số 2026",
        "pdf_id": "1P3NhBQEcdivqpwLfrLw1tlbOn5Wvz5GD",  # Thay bằng ID file ĐỀ số 2
        "giai_id": "16Zp86CeBnft4rNXoe1YQ8deqZK3KXEAB",  # Thay bằng ID file GIẢI số 2
        "key_p1": ["A", "B", "D", "C", "B", "B", "B", "A", "A", "A", "B", "B"],
        "key_p2": {
            1: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
            2: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Sai"},
            3: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Đúng"},
            4: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["2025", "4", "3", "3", "2", "3"]
    },
}

# Giao diện chính
st.title("🎯 PHÒNG THI THỬ TOÁN THEO CHƯƠNG ")
st.markdown("---")

# MENU CHỌN ĐỀ THI ĐỘNG
st.sidebar.header("🗂️ DANH SÁCH ĐỀ THI")
selected_key = st.sidebar.selectbox(
    "Học sinh chọn đề thi tại đây:",
    options=list(EXAMS_BANK.keys()),
    format_func=lambda x: EXAMS_BANK[x]["title"]
)

# Lấy dữ liệu của đề được chọn
current_exam = EXAMS_BANK[selected_key]
pdf_link = f"https://drive.google.com/file/d/{current_exam['pdf_id']}/preview"
giai_link = f"https://drive.google.com/file/d/{current_exam['giai_id']}/view"

# Chia màn hình làm 2 cột: Đề thi (6) và Phiếu trả lời (4)
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Nội dung Đề thi")
    # Khung nhúng PDF tự động thay đổi theo đề chọn
    st.components.v1.iframe(pdf_link, height=1200)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # Đồng hồ đếm ngược 90 phút (Sẽ tự động reset lại từ đầu khi học sinh chuyển đề mới)
    timer_code = f"""
    <div id="timer_{selected_key}" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; font-family: Arial, sans-serif; margin-bottom: 15px;">
        ⏳ 90:00
    </div>
    <script>
    var time_in_minutes = 90;
    var deadline = new Date(Date.parse(new Date()) + time_in_minutes * 60 * 1000);
    function update_clock(){{
        var t = Date.parse(deadline) - Date.parse(new Date());
        var seconds = Math.floor( (t/1000) % 60 );
        var total_minutes = Math.floor(t / 1000 / 60);
        var clock = document.getElementById('timer_{selected_key}');
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
    
    # Form điền đáp án
    with st.form(key=f"form_{selected_key}"):
        
        # --- PHẦN I ---
        st.markdown("### **PHẦN I. Trắc nghiệm nhiều phương án lựa chọn**")
        p1_answers = {}
        for i in range(1, 13):
            p1_answers[i] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None, key=f"p1_c{i}_{selected_key}")
        
        st.markdown("---")
        
        # --- PHẦN II ---
        st.markdown("### **PHẦN II. Trắc nghiệm Đúng / Sai**")
        p2_answers = {}
        for i in range(1, 5):
            st.markdown(f"**Câu {i}:**")
            p2_answers[i] = {}
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a: p2_answers[i]["a"] = st.radio("Ý a)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_a_{selected_key}")
            with col_b: p2_answers[i]["b"] = st.radio("Ý b)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_b_{selected_key}")
            with col_c: p2_answers[i]["c"] = st.radio("Ý c)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_c_{selected_key}")
            with col_d: p2_answers[i]["d"] = st.radio("Ý d)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_d_{selected_key}")
            st.write("")
        
        st.markdown("---")
        
        # --- PHẦN III ---
        st.markdown("### **PHẦN III. Trắc nghiệm Trả lời ngắn**")
        p3_answers = {}
        for i in range(1, 7):
            p3_answers[i] = st.text_input(f"Câu {i}: Nhập đáp số của bạn", key=f"p3_c{i}_{selected_key}")
        
        st.markdown("---")
        submitted = st.form_submit_button("NỘP BÀI & CHẤM ĐIỂM TỰ ĐỘNG", use_container_width=True)

    # =========================================================================
    # LOGIC XỬ LÝ CHẤM ĐIỂM VÀ HIỂN THỊ ĐÁP ÁN CHI TIẾT KHI BẤM NỘP BÀI
    # =========================================================================
    if submitted:
        score_p1 = 0.0
        score_p2 = 0.0
        score_p3 = 0.0
        
        # 1. Chấm điểm Phần I (Mỗi câu đúng 0.25đ)
        for i in range(1, 13):
            if p1_answers[i] == current_exam["key_p1"][i-1]:
                score_p1 += 0.25
                
        # 2. Chấm điểm Phần II (Barem điểm chéo chuẩn Bộ GD)
        p2_score_matrix = {1: 0.1, 2: 0.2, 3: 0.5, 4: 1.0}
        for i in range(1, 5):
            correct_branches = 0
            for branch in ["a", "b", "c", "d"]:
                if p2_answers[i][branch] == current_exam["key_p2"][i][branch]:
                    correct_branches += 1
            if correct_branches > 0:
                score_p2 += p2_score_matrix[correct_branches]
                
        # 3. Chấm điểm Phần III (Mỗi câu đúng 0.5đ)
        for i in range(1, 7):
            if p3_answers[i].strip() == str(current_exam["key_p3"][i-1]).strip():
                score_p3 += 0.5
                
        # Tính tổng điểm tổng kết
        total_score = round(score_p1 + score_p2 + score_p3, 2)
        
        # Xuất kết quả hoành tráng ra màn hình
        st.markdown("---")
        st.success(f"🎉 Bạn đã hoàn thành bài thi! HỆ THỐNG CHẤM ĐIỂM ĐÃ HOÀN TẤT.")
        st.metric(label="📊 ĐIỂM SỐ CỦA BẠN:", value=f"{total_score} / 10.0 Điểm")
        st.balloons()
        
        # Cung cấp link file giải chi tiết
        st.info(f"👉 [BẤM VÀO ĐÂY ĐỂ XEM FILE LỜI GIẢI CHI TIẾT PDF]({giai_link})")
        
        # HIỂN THỊ ĐÁP ÁN CHI TIẾT TỪNG CÂU ĐỂ TRA CỨU LỖI SAI
        with st.expander("🔍 BẢNG ĐỐI CHIẾU ĐÁP ÁN CHI TIẾT TỪNG CÂU"):
            st.markdown("#### **Phần I:**")
            for i in range(1, 13):
                st.write(f"Câu {i}: Bạn chọn: **{p1_answers[i]}** | Đáp án đúng: **{current_exam['key_p1'][i-1]}**")
                
            st.markdown("#### **Phần II:**")
            for i in range(1, 5):
                st.write(f"**Câu {i}:**")
                for branch in ["a", "b", "c", "d"]:
                    st.write(f" - Ý {branch}): Bạn chọn: {p2_answers[i][branch]} | Đúng chuẩn: {current_exam['key_p2'][i][branch]}")
                    
            st.markdown("#### **Phần III:**")
            for i in range(1, 7):
                st.write(f"Câu {i}: Bạn điền: **{p3_answers[i]}** | Đáp số đúng: **{current_exam['key_p3'][i-1]}**")
