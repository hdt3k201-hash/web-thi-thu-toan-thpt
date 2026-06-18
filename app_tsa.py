import streamlit as st

# Cấu hình giao diện trang web trải rộng toàn màn hình
st.set_page_config(page_title="Phòng Thi TSA - Toán Thầy Tùng", layout="wide")

# =========================================================================
# BỘ ĐÁP ÁN CHUẨN (KEY) - Thầy sửa lại đáp án thực tế của đề vào đây nhé
# =========================================================================
KEY_TSA = {
    # Đáp án Phần 1 (Câu 1 đến 15)
    "p1": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C"],
    
    # Đáp án Phần 2 (Câu 16 đến 20 - Mỗi câu 4 ý a,b,c,d)
    "p2": {
        16: {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
        17: {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        18: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Sai"},
        19: {"a": "Sai", "b": "Sai", "c": "Đúng", "d": "Đúng"},
        20: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
    },
    
    # Đáp án Phần 3 (Câu 21 đến 30 - Điền số)
    "p3": ["15", "0", "-2", "3.14", "10", "5", "100", "0.5", "-1", "7"],
    
    # Đáp án Phần 4 (Câu 31 đến 40 - Chọn từ danh sách)
    "p4": [
        "Đồng biến trên R", "Tiệm cận đứng x = 1", "Tập xác định D = R \ {1}", 
        "Có cực đại và cực tiểu", "Nghịch biến trên R", "Tiệm cận ngang y = 2",
        "Đồng biến trên R", "Tiệm cận đứng x = 1", "Tập xác định D = R \ {1}", "Có cực đại và cực tiểu"
    ]
}

st.title("🎯 PHÒNG THI ĐÁNH GIÁ TƯ DUY (TSA) MÔN TOÁN")
st.markdown("---")

query_params = st.query_params
pdf_id = query_params.get("de", "ID_FILE_DE_TSA_CUA_THAY") 
pdf_link = f"https://drive.google.com/file/d/{pdf_id}/preview"

col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Nội dung Đề thi TSA")
    st.components.v1.iframe(pdf_link, height=1400)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # Đồng hồ đếm ngược 120 phút
    timer_code = """
    <div id="timer_tsa" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; margin-bottom: 15px;">
        ⏳ 120:00
    </div>
    <script>
    var time_in_minutes = 120;
    var deadline = new Date(Date.parse(new Date()) + time_in_minutes * 60 * 1000);
    function update_clock(){
        var t = Date.parse(deadline) - Date.parse(new Date());
        var seconds = Math.floor( (t/1000) % 60 );
        var total_minutes = Math.floor(t / 1000 / 60);
        var clock = document.getElementById('timer_tsa');
        if(!clock) return;
        if(t <= 0){
            clock.innerHTML = "HẾT GIỜ LÀM BÀI!";
            clock.style.backgroundColor = "black";
        } else {
            var m = total_minutes < 10 ? "0" + total_minutes : total_minutes;
            var s = seconds < 10 ? "0" + seconds : seconds;
            clock.innerHTML = "⏳ " + m + ":" + s;
        }
    }
    setInterval(update_clock, 1000);
    </script>
    """
    st.components.v1.html(timer_code, height=75)
    
    with st.form(key="form_tsa"):
        # PHẦN I
        st.markdown("### **PHẦN I. Trắc nghiệm nhiều phương án (Câu 1 - 15)**")
        p1_answers = {}
        for i in range(1, 16):
            p1_answers[i] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None)
        
        st.markdown("---")
        
        # PHẦN II
        st.markdown("### **PHẦN II. Trắc nghiệm Đúng / Sai (Câu 16 - 20)**")
        p2_answers = {}
        for i in range(16, 21):
            st.markdown(f"**Câu {i}:**")
            p2_answers[i] = {}
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a: p2_answers[i]["a"] = st.radio("Ý a)", ["Đúng", "Sai"], index=None, key=f"tsa_c{i}_a")
            with col_b: p2_answers[i]["b"] = st.radio("Ý b)", ["Đúng", "Sai"], index=None, key=f"tsa_c{i}_b")
            with col_c: p2_answers[i]["c"] = st.radio("Ý c)", ["Đúng", "Sai"], index=None, key=f"tsa_c{i}_c")
            with col_d: p2_answers[i]["d"] = st.radio("Ý d)", ["Đúng", "Sai"], index=None, key=f"tsa_c{i}_d")
            st.write("")
        
        st.markdown("---")
        
        # PHẦN III
        st.markdown("### **PHẦN III. Điền đáp án (Câu 21 - 30)**")
        p3_answers = {}
        for i in range(21, 31):
            p3_answers[i] = st.text_input(f"Câu {i}: Nhập kết quả của bạn", key=f"tsa_c{i}")
            
        st.markdown("---")
        
        # PHẦN IV
        st.markdown("### **PHẦN IV. Hoàn thành chỗ trống (Câu 31 - 40)**")
        danh_sach_phuong_an = [
            "--- Bấm để chọn phương án ---",
            "Đồng biến trên R", 
            "Nghịch biến trên R", 
            "Có cực đại và cực tiểu", 
            "Tập xác định D = R \ {1}",
            "Tiệm cận đứng x = 1",
            "Tiệm cận ngang y = 2"
        ]
        
        p4_answers = {}
        for i in range(31, 41):
            p4_answers[i] = st.selectbox(f"Vị trí ô trống Câu {i}:", options=danh_sach_phuong_an, key=f"tsa_c{i}")

        st.markdown("---")
        submitted = st.form_submit_button("NỘP BÀI TỚI HỆ THỐNG", use_container_width=True)

    # ==========================================
    # LOGIC CHẤM ĐIỂM SAU KHI NỘP BÀI
    # ==========================================
    if submitted:
        correct_p1 = 0
        correct_p2_y = 0  # Đếm số ý Đúng/Sai đúng
        correct_p3 = 0
        correct_p4 = 0
        
        # Chấm Phần I (15 câu)
        for i in range(1, 16):
            if p1_answers[i] == KEY_TSA["p1"][i-1]:
                correct_p1 += 1
                
        # Chấm Phần II (5 câu x 4 ý = 20 ý)
        for i in range(16, 21):
            for branch in ["a", "b", "c", "d"]:
                if p2_answers[i][branch] == KEY_TSA["p2"][i][branch]:
                    correct_p2_y += 1
                    
        # Chấm Phần III (10 câu)
        for i in range(21, 31):
            # Dùng strip() để xóa khoảng trắng thừa nếu học sinh lỡ tay bấm phím cách
            if p3_answers[i].strip() == str(KEY_TSA["p3"][i-21]):
                correct_p3 += 1
                
        # Chấm Phần IV (10 câu)
        for i in range(31, 41):
            if p4_answers[i] == KEY_TSA["p4"][i-31]:
                correct_p4 += 1
                
        # TỔNG KẾT
        total_correct_items = correct_p1 + correct_p2_y + correct_p3 + correct_p4
        total_items = 15 + 20 + 10 + 10 # Tổng cộng 55 thao tác chọn/điền
        
        st.success("🎉 Bạn đã hoàn thành bài thi! Dưới đây là thống kê kết quả của bạn:")
        st.balloons()
        
        # Hiển thị bảng điểm trực quan
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Phần I (Trắc nghiệm)", f"{correct_p1} / 15 câu")
            st.metric("Phần III (Điền đáp án)", f"{correct_p3} / 10 câu")
        with col_res2:
            st.metric("Phần II (Đúng/Sai)", f"{correct_p2_y} / 20 ý")
            st.metric("Phần IV (Kéo thả)", f"{correct_p4} / 10 câu")
            
        st.markdown(f"### 🏆 TỔNG CỘNG: Đạt {total_correct_items} / {total_items} thao tác đúng!")