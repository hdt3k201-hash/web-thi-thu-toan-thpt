import streamlit as st
import time

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(page_title="Hệ Thống Thi Thử THPT Quốc Gia", layout="wide")

# ==================== MENU CHỌN ĐỀ & ĐỒNG HỒ (SIDEBAR) ====================
with st.sidebar:
    st.header("📂 DANH SÁCH ĐỀ THI")
    
    # 1. Menu chọn đề thi
    danh_sach_de = [
        "Đề số 01: Ôn tập Hàm số",
        "Đề số 02: Ôn tập Khối đa diện"
    ]
    de_thi_chon = st.selectbox("Chọn đề để bắt đầu thi:", danh_sach_de)
    
    # Reset trạng thái nộp bài nếu học sinh đổi đề khác
    key_nop_bai = f"submitted_{de_thi_chon}"
    if key_nop_bai not in st.session_state:
        st.session_state[key_nop_bai] = False
        
    st.markdown("---")
    st.header("⏱️ THỜI GIAN LÀM BÀI")
    
    # 2. Đồng hồ 90 phút chạy ngầm bằng HTML/JS
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

# ==================== CẤU TRÚC ĐỀ THI SỐ 01 ====================
if de_thi_chon == "Đề số 01: Ôn tập Hàm số":
    st.title("ĐỀ SỐ 01: ÔN TẬP HÀM SỐ (CẤU TRÚC MỚI)")
    
    # KHI HỌC SINH CHƯA NỘP BÀI -> HIỂN THỊ FORM LÀM BÀI
    if not st.session_state[key_nop_bai]:
        with st.form("form_de_01"):
            
            # ---------------- PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN (12 CÂU) ----------------
            st.header("PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn")
            st.caption("Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi thí sinh chỉ chọn 1 phương án. (Mỗi câu đúng 0.25 điểm)")
            
            # Ví dụ CÂU 1
            st.markdown("**Câu 1:** Cho hàm số $y=f(x)$ có bảng biến thiên như hình vẽ. Hàm số đồng biến trên khoảng nào?")
            # st.image("hinh_cau1.png") # Bỏ comment dòng này để chèn ảnh
            p1_q1 = st.radio("C1:", [r"A. $(-\infty; 0)$", r"B. $(0; 2)$", r"C. $(2; +\infty)$", r"D. $(-2; 2)$"], key="p1_q1", label_visibility="collapsed")
            st.divider()

            # Sử dụng vòng lặp để tạo nhanh các câu từ 2 đến 12 (giúp code gọn gàng)
            # Bạn có thể tách riêng từng câu như Câu 1 ở trên để dễ chèn đề chi tiết
            p1_ans = {}
            for i in range(2, 13):
                st.markdown(f"**Câu {i}:** (Nội dung câu hỏi {i} điền vào đây...)")
                p1_ans[i] = st.radio(f"C{i}:", [r"A. Đáp án A", r"B. Đáp án B", r"C. Đáp án C", r"D. Đáp án D"], key=f"p1_q{i}", label_visibility="collapsed")
                st.divider()

            # ---------------- PHẦN II: TRẮC NGHIỆM ĐÚNG / SAI (4 CÂU) ----------------
            st.header("PHẦN II. Câu trắc nghiệm đúng sai")
            st.caption("Thí sinh trả lời từ câu 1 đến câu 4. Trong mỗi ý a, b, c, d ở mỗi câu, chọn Đúng hoặc Sai.")
            
            p2_ans = {}
            for i in range(1, 5):
                st.markdown(f"**Câu {i} (Phần 2):** Cho hàm số $y = \\frac{{x^2 - 2x + 1}}{{x - 2}}$. Các mệnh đề sau đây đúng hay sai?")
                # Layout chia cột để hiển thị chữ "Đúng/Sai" thẳng hàng đẹp mắt
                col1, col2 = st.columns([3, 1])
                with col1: st.markdown("a) Hàm số có tập xác định $D = \\mathbb{R} \\setminus \\{2\\}$")
                with col2: p2_ans[f"{i}_a"] = st.radio(f"C{i}a", ["Đúng", "Sai"], key=f"p2_q{i}a", horizontal=True, label_visibility="collapsed")
                
                col1, col2 = st.columns([3, 1])
                with col1: st.markdown("b) Đồ thị hàm số có tiệm cận đứng $x = 2$")
                with col2: p2_ans[f"{i}_b"] = st.radio(f"C{i}b", ["Đúng", "Sai"], key=f"p2_q{i}b", horizontal=True, label_visibility="collapsed")
                
                col1, col2 = st.columns([3, 1])
                with col1: st.markdown("c) Hàm số đạt cực tiểu tại $x = 1$")
                with col2: p2_ans[f"{i}_c"] = st.radio(f"C{i}c", ["Đúng", "Sai"], key=f"p2_q{i}c", horizontal=True, label_visibility="collapsed")
                
                col1, col2 = st.columns([3, 1])
                with col1: st.markdown("d) Giá trị cực đại của hàm số là $y = 0$")
                with col2: p2_ans[f"{i}_d"] = st.radio(f"C{i}d", ["Đúng", "Sai"], key=f"p2_q{i}d", horizontal=True, label_visibility="collapsed")
                st.divider()

            # ---------------- PHẦN III: TRẢ LỜI NGẮN (6 CÂU) ----------------
            st.header("PHẦN III. Câu trắc nghiệm trả lời ngắn")
            st.caption("Thí sinh trả lời từ câu 1 đến câu 6. Điền kết quả dạng số vào ô trống. (Mỗi câu đúng 0.5 điểm)")
            
            p3_ans = {}
            for i in range(1, 7):
                st.markdown(f"**Câu {i} (Phần 3):** Tìm giá trị lớn nhất của hàm số $f(x) = -x^2 + 4x$ trên đoạn $[0; 3]$.")
                p3_ans[i] = st.text_input("Nhập đáp án của bạn:", key=f"p3_q{i}")
                st.divider()

            # Nút Nộp Bài
            submitted = st.form_submit_button("Nộp Bài Thi", type="primary")
            
            if submitted:
                st.session_state[key_nop_bai] = True
                # Lưu toàn bộ dữ liệu làm bài vào session để lát chấm điểm
                st.session_state["p1_q1_ans"] = p1_q1
                st.session_state["p2_ans"] = p2_ans
                st.session_state["p3_ans"] = p3_ans
                st.rerun()

    # KHI HỌC SINH ĐÃ NỘP BÀI -> HIỂN THỊ ĐIỂM & ĐÁP ÁN CHI TIẾT
    else:
        # TÍNH ĐIỂM THEO LUẬT MỚI
        total_score = 0.0
        
        # Điểm Phần 1 (12 câu x 0.25 điểm = 3.0 điểm)
        if st.session_state.p1_q1_ans.startswith("B."): total_score += 0.25
        # (Cộng điểm các câu tiếp theo của Phần 1 ở đây...)
        
        # Điểm Phần 2 (4 câu x 1.0 điểm = 4.0 điểm)
        # Barem: Đúng 1 ý (0.1), 2 ý (0.25), 3 ý (0.5), 4 ý (1.0)
        p2_responses = st.session_state["p2_ans"]
        for i in range(1, 5):
            dung_bao_nhieu_y = 0
            # Giả sử đáp án chuẩn của 4 ý là: a-Đúng, b-Đúng, c-Sai, d-Sai
            if p2_responses[f"{i}_a"] == "Đúng": dung_bao_nhieu_y += 1
            if p2_responses[f"{i}_b"] == "Đúng": dung_bao_nhieu_y += 1
            if p2_responses[f"{i}_c"] == "Sai": dung_bao_nhieu_y += 1
            if p2_responses[f"{i}_d"] == "Sai": dung_bao_nhieu_y += 1
            
            if dung_bao_nhieu_y == 1: total_score += 0.1
            elif dung_bao_nhieu_y == 2: total_score += 0.25
            elif dung_bao_nhieu_y == 3: total_score += 0.5
            elif dung_bao_nhieu_y == 4: total_score += 1.0

        # Điểm Phần 3 (6 câu x 0.5 điểm = 3.0 điểm)
        p3_responses = st.session_state["p3_ans"]
        for i in range(1, 7):
            # Giả sử đáp án đúng là "4"
            if p3_responses[i].strip() == "4": 
                total_score += 0.5

        # Hiển thị kết quả
        st.balloons()
        st.success(f"🎉 BẠN ĐÃ HOÀN THÀNH BÀI THI! Tổng điểm: **{total_score:.2f} / 10.0**")
        
        if st.button("🔄 Làm lại đề này"):
            st.session_state[key_nop_bai] = False
            st.rerun()
            
        st.markdown("---")
        st.header("📖 ĐÁP ÁN & LỜI GIẢI CHI TIẾT")
        
        # Bảng Tra Cứu Lời Giải 
        st.subheader("Phần I. Trắc nghiệm 4 lựa chọn")
        with st.expander("🔍 Câu 1: Xem lời giải chi tiết"):
            st.markdown("**Đáp án đúng:** **B. $(0; 2)$**")
            st.markdown("**Hướng dẫn giải:** Dựa vào đồ thị, hàm số đi lên trên khoảng $(0; 2)$, suy ra hàm số đồng biến trên khoảng này.")

        st.subheader("Phần II. Trắc nghiệm Đúng/Sai")
        with st.expander("🔍 Câu 1: Xem lời giải chi tiết"):
            st.markdown("**Đáp án chuẩn:** a - Đúng | b - Đúng | c - Sai | d - Sai")
            st.markdown("**Hướng dẫn giải:** \n- TXĐ $D = \\mathbb{R} \\setminus \\{2\\}$ (Đúng).\n- Đạo hàm $y' = \\frac{x^2 - 4x + 3}{(x-2)^2}$, $y'=0$ tại $x=1, x=3$. Cực đại tại $x=1$, cực tiểu tại $x=3$ (Ý c sai).")

        st.subheader("Phần III. Trắc nghiệm Trả lời ngắn")
        with st.expander("🔍 Câu 1: Xem lời giải chi tiết"):
            st.markdown("**Đáp án đúng:** **4**")
            st.markdown("**Hướng dẫn giải:** Đạo hàm $f'(x) = -2x + 4$. Giải $f'(x) = 0 \\Leftrightarrow x = 2 \\in [0; 3]$. Ta có $f(0)=0, f(2)=4, f(3)=3$. Max là 4.")

# ==================== CẤU TRÚC ĐỀ SỐ 02 ====================
elif de_thi_chon == "Đề số 02: Ôn tập Khối đa diện":
    st.title("ĐỀ SỐ 02: ÔN TẬP KHỐI ĐA DIỆN")
    st.info("💡 Nội dung đề 02 đang được cập nhật. Bạn vui lòng copy cấu trúc từ Đề 01 xuống đây để nhập câu hỏi mới nhé!")
    # Thầy chỉ cần copy nguyên cụm "if not st.session_state..." của Đề 01 xuống đây và đổi text là xong.
