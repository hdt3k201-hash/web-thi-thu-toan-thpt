import streamlit as st

# Cấu hình giao diện trang web trải rộng toàn màn hình
st.set_page_config(page_title="Phòng Thi Ảo - Lớp Toán Thầy Tùng", layout="wide")

st.title("THI THỬ MÔN TOÁN LỚP 12 - ĐỊNH DẠNG 2025")
st.markdown("---")

# Chia màn hình làm 2 cột: Cột trái (6 phần) để xem đề, Cột phải (4 phần) để làm bài
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📑 Đề thi")
    st.info("Học sinh đọc đề thi tại đây. Thầy dán link file PDF đề thi trên Google Drive vào dòng bên dưới.")
    
    # Nơi thầy dán link file PDF đề thi (nhớ đổi chữ /view ở cuối link thành /preview)
    pdf_link = "https://drive.google.com/file/d/1okC2WNLymDzTD66rtvaw5uiNp9TeVVpO/preview"
    
    # Nhúng khung nhìn PDF (Để chiều cao 1200 cho vừa với độ dài của phiếu điền đáp án)
    st.components.v1.iframe(pdf_link, height=1200)

with col2:
    st.subheader("✍️ Phiếu Điền Đáp Án")
    
    # Tạo Form nộp bài
    with st.form("answer_sheet"):
        
        # --- PHẦN I: 12 CÂU TRẮC NGHIỆM ---
        st.markdown("**PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn**")
        st.caption("Thí sinh chọn 1 đáp án đúng duy nhất cho mỗi câu.")
        
        phan1_answers = {}
        for i in range(1, 13): # Vòng lặp chạy từ câu 1 đến câu 12
            phan1_answers[f"cau_{i}"] = st.radio(f"Câu {i}:", ["A", "B", "C", "D"], horizontal=True, index=None)
        
        st.markdown("---")
        
        # --- PHẦN II: 4 CÂU ĐÚNG/SAI ---
        st.markdown("**PHẦN II. Câu trắc nghiệm đúng sai**")
        st.caption("Trong mỗi ý a), b), c), d) ở mỗi câu, thí sinh chọn Đúng hoặc Sai.")
        
        phan2_answers = {}
        for i in range(1, 5): # Vòng lặp chạy từ câu 1 đến câu 4
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
            st.write("") # Tạo khoảng trắng nhỏ giữa các câu
        
        st.markdown("---")
        
        # --- PHẦN III: 6 CÂU TRẢ LỜI NGẮN ---
        st.markdown("**PHẦN III. Câu trắc nghiệm trả lời ngắn**")
        st.caption("Thí sinh điền đáp số vào ô trống.")
        
        phan3_answers = {}
        for i in range(1, 7): # Vòng lặp chạy từ câu 1 đến câu 6
            phan3_answers[f"cau_{i}"] = st.text_input(f"Câu {i}: Nhập đáp số của bạn", key=f"p3_c{i}")
        
        st.markdown("---")
        # Nút nộp bài
        submitted = st.form_submit_button("NỘP BÀI TỚI HỆ THỐNG", use_container_width=True)

    # Logic sau khi bấm nộp bài
    if submitted:
        st.success("Hệ thống đã ghi nhận bài làm của bạn!")
        st.balloons()
        st.info("Bài làm đã được lưu lại. 👉 [Bấm vào đây để xem File giải chi tiết] (Thầy gắn link PDF giải vào đây)")
