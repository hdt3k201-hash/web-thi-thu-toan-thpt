import streamlit as st
import time

# Cấu hình trang (sử dụng layout="wide" để tách rõ phần làm bài và đồng hồ bên phải)
st.set_page_config(page_title="Đề Thi Thử Môn Toán - 90 Phút", layout="wide")

# ==================== ĐỒNG HỒ ĐẾM NGƯỢC 90 PHÚT Ở BÊN PHẢI (SIDEBAR) ====================
with st.sidebar:
    st.header("⏱️ THỜI GIAN LÀM BÀI")
    
    # Thiết lập thời gian thi chính xác là 90 phút (90 * 60 = 5400 giây)
    thoi_gian_thi_giay = 90 * 60 
    
    # Khởi tạo đồng hồ đếm ngược hiển thị dạng chữ lớn
    khung_dong_ho = st.empty()
    
    # Thanh tiến trình thời gian
    thanh_thoi_gian = st.progress(1.0)
    
    st.markdown("---")
    st.info("💡 **Quy chế phòng thi:**\n- Thời gian làm bài: **90 phút**.\n- Hệ thống sẽ tự động ghi nhận kết quả khi học sinh bấm nút **Nộp Bài Thi** ở cuối trang.")

    # Xử lý logic đếm ngược thời gian thực
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(0, thoi_gian_thi_giay - elapsed_time)
    
    phut = remaining_time // 60
    giay = remaining_time % 60
    khung_dong_ho.markdown(f"### ⏳ **{phut:02d}:{giay:02d}**")
    
    # Cập nhật thanh progress bar theo thời gian 90 phút
    thanh_thoi_gian.progress(remaining_time / thoi_gian_thi_giay)

# ==================== NỘI DUNG CHÍNH CỦA ĐỀ THI ====================
st.title("BÀI 1. SỰ BIẾN THIÊN VÀ CỰC TRỊ CỦA HÀM SỐ")
st.caption("Phần I. Trắc nghiệm nhiều phương án lựa chọn (Thí sinh chọn 1 đáp án đúng)")
st.markdown("---")

# Khởi tạo form làm bài thi gom toàn bộ 10 câu
with st.form("de_thi_so_1"):
    
    # ------------------ CÂU 1 ------------------
    st.markdown("**Câu 1:** Hàm số $y=f(x)$ liên tục trên $\\mathbb{R}$ có bảng biến thiên hàm số $y=f'(x)$ như hình dưới:")
    try:
        st.image("cau1.png", caption="Bảng biến thiên f'(x)")
    except:
        st.warning("⚠️ Lỗi hiển thị: Hãy tải file 'cau1.png' lên cùng thư mục trên GitHub.")
        
    st.markdown("Số điểm cực trị của hàm số $y=f(x)$ là:")
    q1 = st.radio("C1:", [
        r"A. $4$", 
        r"B. $1$", 
        r"C. $2$", 
        r"D. $3$"
    ], key="q1", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 2 ------------------
    st.markdown("**Câu 2:** Cho hàm số bậc bốn $y=f(x)$ có đồ thị là đường cong trong hình dưới đây:")
    try:
        st.image("cau2.png", caption="Đồ thị hàm số y = f(x)")
    except:
        st.warning("⚠️ Lỗi hiển thị: Hãy tải file 'cau2.png' lên GitHub.")
        
    st.markdown("Hàm số đã cho đồng biến trên khoảng nào dưới đây?")
    q2 = st.radio("C2:", [
        r"A. $(7; +\infty)$", 
        r"B. $(-2; 3)$", 
        r"C. $(-\infty; -2)$", 
        r"D. $(-2; 0)$"
    ], key="q2", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 3 ------------------
    st.markdown("**Câu 3:** Cho hàm số $y=f(x)$ có bảng biến thiên như sau:")
    try:
        st.image("cau3.png", caption="Bảng biến thiên y = f(x)")
    except:
        st.warning("⚠️ Lỗi hiển thị: Hãy tải file 'cau3.png' lên GitHub.")
        
    st.markdown("Hàm số đã cho nghịch biến trên khoảng nào dưới đây?")
    q3 = st.radio("C3:", [
        r"A. $(-2; 0)$", 
        r"B. $(-\infty; 0)$", 
        r"C. $(1; 3)$", 
        r"D. $(3; +\infty)$"
    ], key="q3", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 4 ------------------
    st.markdown("**Câu 4:** Cho hàm số $y=f'(x)$ có đồ thị là đường cong trong hình vẽ dưới đây:")
    try:
        st.image("cau4.png", caption="Đồ thị y = f'(x)")
    except:
        st.warning("⚠️ Lỗi hiển thị: Hãy tải file 'cau4.png' lên GitHub.")
        
    st.markdown("Hàm số $y=f(x)$ đồng biến trên khoảng nào sau đây?")
    q4 = st.radio("C4:", [
        r"A. $(-\infty; -1)$", 
        r"B. $(-1; 1)$", 
        r"C. $(1; 4)$", 
        r"D. $(1; +\infty)$"
    ], key="q4", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 5 ------------------
    st.markdown("**Câu 5:** Hàm số nào sau đây nghịch biến trên $\\mathbb{R}$?")
    q5 = st.radio("C5:", [
        r"A. $y = -x^3 + 3x^2 - 9x$", 
        r"B. $y = -x^3 + x + 1$", 
        r"C. $y = \frac{x-1}{x-2}$", 
        r"D. $y = 2x^2 + 3x + 2$"
    ], key="q5", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 6 ------------------
    st.markdown("**Câu 6:** Cho hàm số $y=f(x)$ có đồ thị là đường cong như hình vẽ bên dưới:")
    try:
        st.image("cau6.png", caption="Đồ thị y = f(x)")
    except:
        st.warning("⚠️ Lỗi hiển thị: Hãy tải file 'cau6.png' lên GitHub.")
        
    st.markdown("Hàm số $f(x)$ đạt cực đại tại điểm nào sau đây?")
    q6 = st.radio("C6:", [
        r"A. $x = 1$", 
        r"B. $x = -1$", 
        r"C. $y = 3$", 
        r"D. $M(-1; 3)$"
    ], key="q6", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 7 ------------------
    st.markdown("**Câu 7:** Cho hàm số $y=f(x)$ xác định trên $\\mathbb{R}$ và có bảng biến thiên như hình vẽ sau:")
    try:
        st.image("cau7.png", caption="Bảng biến thiên câu 7")
    except:
        st.warning("⚠️ Lỗi hiển thị: Hãy tải file 'cau7.png' lên GitHub.")
        
    st.markdown("Giá trị cực tiểu của hàm số $y=f(x)$ là:")
    q7 = st.radio("C7:", [
        r"A. $-10$", 
        r"B. $11$", 
        r"C. $6$", 
        r"D. $-20$"
    ], key="q7", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 8 ------------------
    st.markdown(r"**Câu 8:** Cho hàm số $y=\frac{x-2}{x+1}$. Khẳng định nào sau đây là đúng?")
    q8 = st.radio("C8:", [
        r"A. Hàm số đồng biến trên $(-\infty; -1) \cup (-1; +\infty)$",
        r"B. Hàm số đồng biến trên $(-\infty; -1)$ và $(-1; +\infty)$",
        r"C. Hàm số đồng biến trên $\mathbb{R} \setminus \{-1\}$",
        r"D. Hàm số đồng biến trên $(-\infty; 1)$"
    ], key="q8", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 9 ------------------
    st.markdown(r"**Câu 9:** Cho hàm số $y=\frac{x^2-3x+5}{x+1}$ nghịch biến trên các khoảng nào?")
    q9 = st.radio("C9:", [
        r"A. $(-4; 2)$",
        r"B. $(-\infty; -2)$",
        r"C. $(-\infty; -1)$ và $(-1; +\infty)$",
        r"D. $(-4; -1)$ và $(-1; 2)$"
    ], key="q9", label_visibility="collapsed")
    st.divider()

    # ------------------ CÂU 10 ------------------
    st.markdown(r"**Câu 10:** Cho hàm số $y=f(x)$ xác định trên $\mathbb{R}$ và có đạo hàm $f'(x)=12x^{2025}(x+1)(3-x)$, $\forall x \in \mathbb{R}$. Hàm số đã cho đồng biến trên khoảng nào sau đây?")
    q10 = st.radio("C10:", [
        r"A. $(-1; 3)$",
        r"B. $(-\infty; -1)$",
        r"C. $(3; +\infty)$",
        r"D. $(-\infty; 0)$"
    ], key="q10", label_visibility="collapsed")
    st.divider()

    # Nút nộp bài
    submitted = st.form_submit_button("Nộp Bài Thi")

# ------------------ XỬ LÝ CHẤM ĐIỂM TỰ ĐỘNG ------------------
if submitted:
    score = 0
    if q1.startswith("C."): score += 1
    if q2.startswith("C."): score += 1
    if q3.startswith("C."): score += 1
    if q4.startswith("B."): score += 1
    if q5.startswith("A."): score += 1
    if q6.startswith("B."): score += 1
    if q7.startswith("D."): score += 1
    if q8.startswith("B."): score += 1
    if q9.startswith("D."): score += 1
    if q10.startswith("B."): score += 1

    st.balloons()
    st.success(f"🎉 Bạn đã hoàn thành bài thi! Kết quả: **{score}/10** điểm.")
