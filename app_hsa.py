import streamlit as st

# Cấu hình giao diện trang web trải rộng toàn màn hình
st.set_page_config(page_title="Hệ Thống Thi HSA - Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI HSA (Thầy thêm đề 3, 4, 5... tương tự cấu trúc này)
# =========================================================================
HSA_EXAMS_BANK = {
    "de_hsa_1": {
        "title": "Đề HSA 01: Đề thi minh họa Đánh giá năng lực ĐHQG Hà Nội",
        "pdf_id": "ID_FILE_DE_HSA_1",  # Thay bằng ID file đề 1 trên Drive của thầy
        "giai_id": "ID_FILE_GIAI_HSA_1", # Thay bằng ID file giải 1 trên Drive của thầy
        # Bộ đáp án chuẩn 35 câu Phần I (A, B, C, D)
        "key_p1": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C"],
        # Bộ đáp án chuẩn 15 câu Phần II (Điền số)
        "key_p2": ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "0", "-5", "1.5", "2", "3"]
    },
    "de_hsa_2": {
        "title": "Đề HSA 02: Luyện đề Đột phá tư duy HSA - Điểm 100+",
        "pdf_id": "ID_FILE_DE_HSA_2",  # Thay bằng ID file đề 2 trên Drive của thầy
        "giai_id": "ID_FILE_GIAI_HSA_2", # Thay bằng ID file giải 2 trên Drive của thầy
        "key_p1": ["B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"],
        "key_p2": ["5", "15", "25", "35", "45", "55", "65", "75", "85", "95", "1", "-1", "0.5", "4", "8"]
    }
}

st.title("🎯 HỆ THỐNG THI ĐÁNH GIÁ NĂNG LỰC (HSA) MÔN TOÁN")
st.markdown("---")

# MENU CHỌN ĐỀ THI ĐỘNG Ở THANH SIDEBAR TRÁI
st.sidebar.header("🗂️ DANH SÁCH ĐỀ THI HSA")
selected_exam_key = st.sidebar.selectbox(
    "Học sinh chọn đề thi tại đây:",
    options=list(HSA_EXAMS_BANK.keys()),
    format_func=lambda x: HSA_EXAMS_BANK[x]["title"]
)

# Lấy dữ liệu của đề đang được học sinh chọn
current_exam = HSA_EXAMS_BANK[selected_exam_key]
pdf_link = f"https://drive.google.com/file/d/{current_exam['pdf_id']}/preview"
giai_link = f"https://drive.google.com/file/d/{current_exam['giai_id']}/view"

# Chia đôi màn hình: Đề bên trái (6 phần), Phiếu làm bài bên phải (4 phần)
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Nội dung Đề thi HSA")
    st.components.v1.iframe(pdf_link, height=1400)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # Đồng hồ đếm ngược 90 phút (Tự reset về lại 90:00 khi học sinh bấm đổi đề thi)
    timer_code = f"""
    <div id="timer_{selected_exam_key}" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; margin-bottom: 15px; font-family: Arial, sans-serif;">
        ⏳ 90:00
    </div>
    <script>
    var time_in_minutes = 90;
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
        
        # PHẦN I: 35 CÂU TRẮC NGHIỆM
        st.markdown("### **PHẦN I. Câu hỏi trắc nghiệm nhiều phương án (Câu 1 - 35)**")
        p1_answers = {}
        for i in range(1, 36):
            p1_answers[i] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None, key=f"p1_c{i}_{selected_exam_key}")
        
        st.markdown("---")
        
        # PHẦN II: 15 CÂU ĐIỀN ĐÁP ÁN
        st.markdown("### **PHẦN II. Câu hỏi điền đáp án ngắn (Câu 36 - 50)**")
        p2_answers = {}
        for i in range(36, 51):
            p2_answers[i] = st.text_input(f"Câu {i}: Nhập kết quả điền số của bạn", key=f"p2_c{i}_{selected_exam_key}")

        st.markdown("---")
        submitted = st.form_submit_button("NỘP BÀI & CHẤM ĐIỂM TỰ ĐỘNG", use_container_width=True)

    # =========================================================================
    # LOGIC CHẤM ĐIỂM TỰ ĐỘNG & XUẤT ĐÁP ÁN ĐÚNG SAI
    # =========================================================================
    if submitted:
        correct_p1 = sum(1 for i in range(1, 36) if p1_answers[i] == current_exam["key_p1"][i-1])
        correct_p2 = sum(1 for i in range(36, 51) if p2_answers[i].strip() == str(current_exam["key_p2"][i-36]).strip())
                
        total_correct = correct_p1 + correct_p2
        total_questions = 50
        total_wrong = total_questions - total_correct
        
        st.success("🎉 Bạn đã hoàn thành bài thi HSA! Dưới đây là kết quả chi tiết:")
        st.balloons()
        
        # Thống kê nhanh số câu đúng sai
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("✅ SỐ CÂU ĐÚNG", f"{total_correct} / 50 câu")
        with col_res2:
            st.metric("❌ SỐ CÂU SAI / BỎ TRỐNG", f"{total_wrong} câu")
        with col_res3:
            # Quy đổi tạm tính sang thang điểm 150 chuẩn của HSA ĐHQGHN (mỗi câu đúng = 3 điểm)
            st.metric("📊 ĐIỂM SỐ ĐỔI THEO HSA", f"{total_correct * 3} / 150 điểm")
            
        if current_exam['giai_id']:
            st.info(f"👉 [BẤM VÀO ĐÂY ĐỂ XEM FILE LỜI GIẢI CHI TIẾT PDF]({giai_link})")
            
        # HIỂN THỊ CHI TIẾT BẢNG SO SÁNH ĐÁP ÁN ĐÚNG SAI TỪNG CÂU
        with st.expander("🔍 XEM CHI TIẾT BẢNG ĐỐI CHIẾU ĐÁP ÁN ĐÚNG SAI TỪNG CÂU"):
            st.markdown("#### **Chi tiết Phần I (Trắc nghiệm 4 lựa chọn):**")
            for i in range(1, 36):
                is_correct = p1_answers[i] == current_exam["key_p1"][i-1]
                status_icon = "✅ Đúng" if is_correct else "❌ Sai"
                student_choice = p1_answers[i] if p1_answers[i] else "Bỏ trống"
                st.write(f"Câu {i}: Bạn chọn: **{student_choice}** | Đáp án đúng: **{current_exam['key_p1'][i-1]}** -> {status_icon}")
                
            st.markdown("#### **Chi tiết Phần II (Điền đáp án ngắn):**")
            for i in range(36, 51):
                is_correct = p2_answers[i].strip() == str(current_exam["key_p2"][i-36]).strip()
                status_icon = "✅ Đúng" if is_correct else "❌ Sai"
                student_input = p2_answers[i] if p2_answers[i].strip() else "Bỏ trống"
                st.write(f"Câu {i}: Bạn nhập: **{student_input}** | Đáp án đúng: **{current_exam['key_p2'][i-36]}** -> {status_icon}")