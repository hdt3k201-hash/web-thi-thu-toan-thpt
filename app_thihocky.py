import streamlit as st
import time

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(page_title="Hệ Thống Thi Thử Môn Toán", layout="wide")

# ==================== MENU CHỌN ĐỀ VÀ ĐỒNG HỒ (SIDEBAR) ====================
with st.sidebar:
    st.header("📂 DANH SÁCH ĐỀ THI")
    
    # Tạo menu thả xuống để học sinh chọn đề
    danh_sach_de = [
        "Đề số 01: Sự biến thiên và cực trị",
        "Đề số 02: Khối đa diện và Thể tích"
    ]
    de_thi_chon = st.selectbox("Học sinh chọn đề thi tại đây:", danh_sach_de)
    
    st.markdown("---")
    st.header("⏱️ THỜI GIAN LÀM BÀI")
    
    # Nhúng đồng hồ JS (Đồng hồ sẽ reset khi chọn đề mới)
    from streamlit.components.v1 import html
    dong_ho_html = """
    <div style="font-family: monospace; font-size: 28px; font-weight: bold; color: #d9534f; background-color: #f8f9fa; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #ddd;">
        <span id="timer">90:00</span>
    </div>
    <script>
        var totalSeconds = 90 * 60;
        var timerElement = document.getElementById('timer');
        var timer = setInterval(function() {
            var minutes = Math.floor(totalSeconds / 60);
            var seconds = totalSeconds % 60;
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            timerElement.textContent = minutes + ":" + seconds;
            if (totalSeconds <= 0) {
                clearInterval(timer);
                timerElement.textContent = "HẾT GIỜ!";
            } else {
                totalSeconds--;
            }
        }, 1000);
    </script>
    """
    html(dong_ho_html, height=70)
    
    st.info("💡 **Lưu ý:** Chuyển đổi đề thi sẽ làm mới lại toàn bộ thời gian và bài làm hiện tại.")

# ==================== KHU VỰC XỬ LÝ TRẠNG THÁI NỘP BÀI ====================
# Tạo session_state riêng cho từng đề để tránh lỗi học sinh nộp đề này nhưng hiện điểm đề kia
key_nop_bai = f"submitted_{de_thi_chon}"
if key_nop_bai not in st.session_state:
    st.session_state[key_nop_bai] = False

# ==================== NỘI DUNG: ĐỀ SỐ 01 ====================
if de_thi_chon == "Đề số 01: Sự biến thiên và cực trị":
    st.title("BÀI 1. SỰ BIẾN THIÊN VÀ CỰC TRỊ CỦA HÀM SỐ")
    st.markdown("---")
    
    if not st.session_state[key_nop_bai]:
        with st.form("form_de_01"):
            st.markdown("**Câu 1:** Hàm số $y=f(x)$ liên tục trên $\\mathbb{R}$ có bảng biến thiên hàm số $y=f'(x)$ như hình dưới:")
            q1_d1 = st.radio("C1:", [r"A. $4$", r"B. $1$", r"C. $2$", r"D. $3$"], key="q1_d1", label_visibility="collapsed")
            st.divider()
            
            st.markdown("**Câu 2:** Cho hàm số bậc bốn $y=f(x)$ có đồ thị là đường cong trong hình dưới đây. Hàm số đã cho đồng biến trên khoảng nào?")
            q2_d1 = st.radio("C2:", [r"A. $(7; +\infty)$", r"B. $(-2; 3)$", r"C. $(-\infty; -2)$", r"D. $(-2; 0)$"], key="q2_d1", label_visibility="collapsed")
            st.divider()
            
            submitted_1 = st.form_submit_button("Nộp Bài Thi Đề 01")
            if submitted_1:
                st.session_state[key_nop_bai] = True
                st.session_state.q1_d1_ans = q1_d1
                st.session_state.q2_d1_ans = q2_d1
                st.rerun()
    else:
        # Chấm điểm Đề 01
        score = 0
        if st.session_state.q1_d1_ans.startswith("C."): score += 1
        if st.session_state.q2_d1_ans.startswith("C."): score += 1
        
        st.success(f"🎉 Bạn đã hoàn thành Đề 01! Điểm: **{score}/2**")
        if st.button("🔄 Làm lại Đề 01"):
            st.session_state[key_nop_bai] = False
            st.rerun()

# ==================== NỘI DUNG: ĐỀ SỐ 02 ====================
elif de_thi_chon == "Đề số 02: Khối đa diện và Thể tích":
    st.title("BÀI 2. KHỐI ĐA DIỆN VÀ THỂ TÍCH")
    st.markdown("---")
    
    if not st.session_state[key_nop_bai]:
        with st.form("form_de_02"):
            st.markdown("**Câu 1:** Cho khối chóp $S.ABC$ có đáy $ABC$ là tam giác vuông cân tại $A$, $AB = a$. Cạnh bên $SA$ vuông góc với mặt phẳng đáy và $SA = a\sqrt{2}$. Thể tích khối chóp $S.ABC$ là:")
            q1_d2 = st.radio("C1:", [r"A. $\frac{a^3\sqrt{2}}{2}$", r"B. $\frac{a^3\sqrt{2}}{6}$", r"C. $a^3\sqrt{2}$", r"D. $\frac{a^3\sqrt{2}}{3}$"], key="q1_d2", label_visibility="collapsed")
            st.divider()
            
            st.markdown("**Câu 2:** Thể tích của khối lăng trụ đứng tam giác đều có tất cả các cạnh bằng $a$ là:")
            q2_d2 = st.radio("C2:", [r"A. $\frac{a^3\sqrt{3}}{4}$", r"B. $\frac{a^3\sqrt{3}}{2}$", r"C. $\frac{a^3\sqrt{3}}{12}$", r"D. $\frac{a^3\sqrt{3}}{6}$"], key="q2_d2", label_visibility="collapsed")
            st.divider()
            
            submitted_2 = st.form_submit_button("Nộp Bài Thi Đề 02")
            if submitted_2:
                st.session_state[key_nop_bai] = True
                st.session_state.q1_d2_ans = q1_d2
                st.session_state.q2_d2_ans = q2_d2
                st.rerun()
    else:
        # Chấm điểm Đề 02
        score = 0
        if st.session_state.q1_d2_ans.startswith("B."): score += 1
        if st.session_state.q2_d2_ans.startswith("A."): score += 1
        
        st.success(f"🎉 Bạn đã hoàn thành Đề 02! Điểm: **{score}/2**")
        if st.button("🔄 Làm lại Đề 02"):
            st.session_state[key_nop_bai] = False
            st.rerun()
