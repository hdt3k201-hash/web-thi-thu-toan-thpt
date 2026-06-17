import streamlit as st

# Cấu hình giao diện trang web trải rộng toàn màn hình
st.set_page_config(page_title="Phòng Thi Ảo - Lớp Toán Thầy Tùng", layout="wide")

st.title("THI THỬ MÔN TOÁN LỚP 12 - ĐỊNH DẠNG 2025")
st.markdown("---")

# Nhận diện Đề thi và Đáp án tự động từ link web
query_params = st.query_params
pdf_id = query_params.get("de", "1A2b3C4d5E6f7G8h9I") 
pdf_link = f"https://drive.google.com/file/d/{pdf_id}/preview"

giai_id = query_params.get("giaichitiet", "")
giai_link = f"https://drive.google.com/file/d/{giai_id}/view"

# Chia màn hình làm 2 cột: Cột trái (6 phần) để xem đề, Cột phải (4 phần) để làm bài
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Đề thi")
    # Nhúng khung nhìn PDF động
    st.components.v1.iframe(pdf_link, height=1200)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # KHỐI LỆNH ĐỒNG HỒ ĐẾM NGƯỢC 90 PHÚT (Bảo mật 100% không bị lỗi text)
    timer_code = """
    <div id="timer" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; font-family: Arial, sans-serif;">
        ⏳ 90:00
    </div>
    <script>
    var time_in_minutes = 90;
    var deadline = new Date(Date.parse(new Date()) + time_in_minutes * 60 * 1000);
    function update_clock(){
        var t = Date.parse(deadline) - Date.parse(new Date());
        var seconds = Math.floor( (t/1000) % 60 );
        var total_minutes = Math.floor(t / 1000 / 60);
        var clock = document.getElementById('timer');
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
    # Hiển thị đồng hồ bằng module chuyên dụng HTML của Streamlit
    st.components.v1.html(timer_code, height=75)
    
    with st.form("answer_sheet"):
        # --- PHẦN I: 12 CÂU TRẮC NGHIỆM ---
        st.markdown("**PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn**")
        phan1_answers = {}
        for i in range(1, 13):
            phan1_answers[f"cau_{i}"] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None)
        
        st.markdown("---")
        
        # --- PHẦN II: 4 CÂU ĐÚNG/SAI ---
        st.markdown("**PHẦN II. Câu trắc nghiệm đúng sai**")
        phan2_answers = {}
        for i in range(1, 5):
            st.markdown(f"**Câu {i}:**")
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                phan2_answers[f"cau_{i}_a"] = st.radio(f"Ý a)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_a")
            with col_b:
                phan2_answers[f"cau_{i}_b"] = st.radio(f"Ý b)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_b")
            with col_c:
                phan2_answers[f"cau_{i}_c"] = st.radio(f"Ý c)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_c")
            with col_d:
                phan2_answers[f"cau_{i}_d"] = st.radio(f"Ý d)", ["Đúng", "Sai"], index=None, key=f"p2_c{i}_d")
            st.write("")
        
        st.markdown("---")
        
        # --- PHẦN III: 6 CÂU TRẢ LỜI NGẮN ---
        st.markdown("**PHẦN III. Câu trắc nghiệm trả lời ngắn**")
        phan3_answers = {}
        for i in range(1, 7):
            phan3_answers[f"cau_{i}"] = st.text_input(f"Câu {i}: Nhập đáp số của bạn", key=f"p3_c{i}")
        
        st.markdown("---")
        submitted = st.form_submit_button("NỘP BÀI TỚI HỆ THỐNG", use_container_width=True)

    # Xử lý sau khi bấm nộp bài
    if submitted:
        st.success("Hệ thống đã ghi nhận bài làm của bạn!")
        st.balloons()
        if giai_id:
            st.info(f"👉 [Bấm vào đây để xem File giải chi tiết]({giai_link})")
        else:
            st.warning("Đề thi này hiện chưa cập nhật lời giải chi tiết.")
