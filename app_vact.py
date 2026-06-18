import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(page_title="Hệ Thống Thi VACT - Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI VACT (Thầy thêm đề 3, 4, 5... tương tự cấu trúc này)
# =========================================================================
VACT_EXAMS_BANK = {
    "de_vact_1": {
        "title": "Đề VACT 01: Khảo sát năng lực Toán học",
        "pdf_id": "ID_FILE_DE_VACT_1",  # Thay bằng ID file đề 1 trên Drive của thầy
        "giai_id": "ID_FILE_GIAI_VACT_1", # Thay bằng ID file giải 1 trên Drive
        # Bộ đáp án chuẩn 42 câu trắc nghiệm
        "key_p1": [
            "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
            "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", 
            "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
            "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", 
            "A", "B"
        ]
    },
    "de_vact_2": {
        "title": "Đề VACT 02: Luyện tập tổng hợp",
        "pdf_id": "ID_FILE_DE_VACT_2",  # Thay bằng ID file đề 2 trên Drive
        "giai_id": "ID_FILE_GIAI_VACT_2", # Thay bằng ID file giải 2 trên Drive
        "key_p1": [
            "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", 
            "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", 
            "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", 
            "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", 
            "B", "C"
        ]
    }
}

st.title("🎯 HỆ THỐNG THI VACT MÔN TOÁN")
st.markdown("---")

# MENU CHỌN ĐỀ THI ĐỘNG
st.sidebar.header("🗂️ DANH SÁCH ĐỀ THI VACT")
selected_exam_key = st.sidebar.selectbox(
    "Học sinh chọn đề thi tại đây:",
    options=list(VACT_EXAMS_BANK.keys()),
    format_func=lambda x: VACT_EXAMS_BANK[x]["title"]
)

# Lấy dữ liệu của đề đang được chọn
current_exam = VACT_EXAMS_BANK[selected_exam_key]
pdf_link = f"https://drive.google.com/file/d/{current_exam['pdf_id']}/preview"
giai_link = f"https://drive.google.com/file/d/{current_exam['giai_id']}/view"

col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Nội dung Đề thi VACT")
    st.components.v1.iframe(pdf_link, height=1200)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # Đồng hồ đếm ngược 55 phút (Tự reset khi đổi đề)
    timer_code = f"""
    <div id="timer_{selected_exam_key}" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; margin-bottom: 15px; font-family: Arial, sans-serif;">
        ⏳ 55:00
    </div>
    <script>
    var time_in_minutes = 55;
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
        
        st.markdown("### **Trắc nghiệm nhiều phương án (Câu 1 - 42)**")
        p1_answers = {}
        for i in range(1, 43):
            p1_answers[i] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None, key=f"p1_c{i}_{selected_exam_key}")
        
        st.markdown("---")
        submitted = st.form_submit_button("NỘP BÀI & CHẤM ĐIỂM TỰ ĐỘNG", use_container_width=True)

    # =========================================================================
    # LOGIC CHẤM ĐIỂM TỰ ĐỘNG
    # =========================================================================
    if submitted:
        correct_p1 = sum(1 for i in range(1, 43) if p1_answers[i] == current_exam["key_p1"][i-1])
        total_questions = 42
        total_wrong = total_questions - correct_p1
        
        st.success("🎉 Bạn đã hoàn thành bài thi VACT! Dưới đây là kết quả chi tiết:")
        st.balloons()
        
        # Thống kê nhanh
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("✅ SỐ CÂU ĐÚNG", f"{correct_p1} / 42 câu")
        with col_res2:
            st.metric("❌ SỐ CÂU SAI / BỎ TRỐNG", f"{total_wrong} câu")
            
        if current_exam['giai_id']:
            st.info(f"👉 [BẤM VÀO ĐÂY ĐỂ XEM FILE LỜI GIẢI CHI TIẾT PDF]({giai_link})")
            
        # HIỂN THỊ CHI TIẾT BẢNG SO SÁNH ĐÁP ÁN ĐÚNG SAI
        with st.expander("🔍 XEM CHI TIẾT BẢNG ĐỐI CHIẾU ĐÁP ÁN TỪNG CÂU"):
            for i in range(1, 43):
                is_correct = p1_answers[i] == current_exam["key_p1"][i-1]
                status_icon = "✅ Đúng" if is_correct else "❌ Sai"
                student_choice = p1_answers[i] if p1_answers[i] else "Bỏ trống"
                st.write(f"Câu {i}: Bạn chọn: **{student_choice}** | Đáp án chuẩn: **{current_exam['key_p1'][i-1]}** -> {status_icon}")