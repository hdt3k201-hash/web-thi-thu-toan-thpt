import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Đề Thi Thử Môn Toán - 90 Phút", layout="wide")

# ==================== ĐỒNG HỒ ĐẾM NGƯỢC 90 PHÚT (HTML/JS) ====================
with st.sidebar:
    st.header("⏱️ THỜI GIAN LÀM BÀI")
    
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
    
    st.markdown("---")
    st.info("💡 **Quy chế phòng thi:**\n- Thời gian làm bài: **90 phút**.\n- Sau khi nộp bài, học sinh có thể xem lại lời giải chi tiết từng câu.")

# ==================== NỘI DUNG CHÍNH ====================
st.title("BÀI 1. SỰ BIẾN THIÊN VÀ CỰC TRỊ CỦA HÀM SỐ")
st.caption("Phần I. Trắc nghiệm nhiều phương án lựa chọn (Thí sinh chọn 1 đáp án đúng)")
st.markdown("---")

# Kiểm tra trạng thái đã nộp bài hay chưa thông qua st.session_state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Nếu CHƯA nộp bài thì hiển thị form làm bài
if not st.session_state.submitted:
    with st.form("de_thi_so_1"):
        
        # CÂU 1
        st.markdown("**Câu 1:** Hàm số $y=f(x)$ liên tục trên $\\mathbb{R}$ có bảng biến thiên hàm số $y=f'(x)$ như hình dưới:")
        try: st.image("cau1.png", caption="Bảng biến thiên f'(x)")
        except: st.warning("⚠️ Thiếu file ảnh cau1.png")
        st.markdown("Số điểm cực trị của hàm số $y=f(x)$ là:")
        q1 = st.radio("C1:", [r"A. $4$", r"B. $1$", r"C. $2$", r"D. $3$"], key="q1_in", label_visibility="collapsed")
        st.divider()

        # CÂU 2
        st.markdown("**Câu 2:** Cho hàm số bậc bốn $y=f(x)$ có đồ thị là đường cong trong hình dưới đây:")
        try: st.image("cau2.png", caption="Đồ thị hàm số y = f(x)")
        except: st.warning("⚠️ Thiếu file ảnh cau2.png")
        st.markdown("Hàm số đã cho đồng biến trên khoảng nào dưới đây?")
        q2 = st.radio("C2:", [r"A. $(7; +\infty)$", r"B. $(-2; 3)$", r"C. $(-\infty; -2)$", r"D. $(-2; 0)$"], key="q2_in", label_visibility="collapsed")
        st.divider()

        # CÂU 3
        st.markdown("**Câu 3:** Cho hàm số $y=f(x)$ có bảng biến thiên như sau:")
        try: st.image("cau3.png", caption="Bảng biến thiên y = f(x)")
        except: st.warning("⚠️ Thiếu file ảnh cau3.png")
        st.markdown("Hàm số đã cho nghịch biến trên khoảng nào dưới đây?")
        q3 = st.radio("C3:", [r"A. $(-2; 0)$", r"B. $(-\infty; 0)$", r"C. $(1; 3)$", r"D. $(3; +\infty)$"], key="q3_in", label_visibility="collapsed")
        st.divider()

        # CÂU 4
        st.markdown("**Câu 4:** Cho hàm số $y=f'(x)$ có đồ thị là đường cong trong hình vẽ dưới đây:")
        try: st.image("cau4.png", caption="Đồ thị y = f'(x)")
        except: st.warning("⚠️ Thiếu file ảnh cau4.png")
        st.markdown("Hàm số $y=f(x)$ đồng biến trên khoảng nào sau đây?")
        q4 = st.radio("C4:", [r"A. $(-\infty; -1)$", r"B. $(-1; 1)$", r"C. $(1; 4)$", r"D. $(1; +\infty)$"], key="q4_in", label_visibility="collapsed")
        st.divider()

        # CÂU 5
        st.markdown("**Câu 5:** Hàm số nào sau đây nghịch biến trên $\\mathbb{R}$?")
        q5 = st.radio("C5:", [r"A. $y = -x^3 + 3x^2 - 9x$", r"B. $y = -x^3 + x + 1$", r"C. $y = \frac{x-1}{x-2}$", r"D. $y = 2x^2 + 3x + 2$"], key="q5_in", label_visibility="collapsed")
        st.divider()

        # CÂU 6
        st.markdown("**Câu 6:** Cho hàm số $y=f(x)$ có đồ thị là đường cong như hình vẽ bên dưới:")
        try: st.image("cau6.png", caption="Đồ thị y = f(x)")
        except: st.warning("⚠️ Thiếu file ảnh cau6.png")
        st.markdown("Hàm số $f(x)$ đạt cực đại tại điểm nào sau đây?")
        q6 = st.radio("C6:", [r"A. $x = 1$", r"B. $x = -1$", r"C. $y = 3$", r"D. $M(-1; 3)$"], key="q6_in", label_visibility="collapsed")
        st.divider()

        # CÂU 7
        st.markdown("**Câu 7:** Cho hàm số $y=f(x)$ xác định trên $\\mathbb{R}$ và có bảng biến thiên như hình vẽ sau:")
        try: st.image("cau7.png", caption="Bảng biến thiên câu 7")
        except: st.warning("⚠️ Thiếu file ảnh cau7.png")
        st.markdown("Giá trị cực tiểu của hàm số $y=f(x)$ là:")
        q7 = st.radio("C7:", [r"A. $-10$", r"B. $11$", r"C. $6$", r"D. $-20$"], key="q7_in", label_visibility="collapsed")
        st.divider()

        # CÂU 8
        st.markdown(r"**Câu 8:** Cho hàm số $y=\frac{x-2}{x+1}$. Khẳng định nào sau đây là đúng?")
        q8 = st.radio("C8:", [
            r"A. Hàm số đồng biến trên $(-\infty; -1) \cup (-1; +\infty)$",
            r"B. Hàm số đồng biến trên $(-\infty; -1)$ và $(-1; +\infty)$",
            r"C. Hàm số đồng biến trên $\mathbb{R} \setminus \{-1\}$",
            r"D. Hàm số đồng biến trên $(-\infty; 1)$"
        ], key="q8_in", label_visibility="collapsed")
        st.divider()

        # CÂU 9
        st.markdown(r"**Câu 9:** Cho hàm số $y=\frac{x^2-3x+5}{x+1}$ nghịch biến trên các khoảng nào?")
        q9 = st.radio("C9:", [
            r"A. $(-4; 2)$",
            r"B. $(-\infty; -2)$",
            r"C. $(-\infty; -1)$ và $(-1; +\infty)$",
            r"D. $(-4; -1)$ và $(-1; 2)$"
        ], key="q9_in", label_visibility="collapsed")
        st.divider()

        # CÂU 10
        st.markdown(r"**Câu 10:** Cho hàm số $y=f(x)$ xác định trên $\mathbb{R}$ và có đạo hàm $f'(x)=12x^{2025}(x+1)(3-x)$, $\forall x \in \mathbb{R}$. Hàm số đã cho đồng biến trên khoảng nào sau đây?")
        q10 = st.radio("C10:", [
            r"A. $(-1; 3)$",
            r"B. $(-\infty; -1)$",
            r"C. $(3; +\infty)$",
            r"D. $(-\infty; 0)$"
        ], key="q10_in", label_visibility="collapsed")
        st.divider()

        # Nút nộp bài
        submitted = st.form_submit_button("Nộp Bài Thi")

        if submitted:
            # Lưu lại đáp án học sinh chọn vào session_state để dùng sau khi nộp
            st.session_state.submitted = True
            st.session_state.q1 = q1
            st.session_state.q2 = q2
            st.session_state.q3 = q3
            st.session_state.q4 = q4
            st.session_state.q5 = q5
            st.session_state.q6 = q6
            st.session_state.q7 = q7
            st.session_state.q8 = q8
            st.session_state.q9 = q9
            st.session_state.q10 = q10
            st.rerun()

# Nếu ĐÃ NỘP BÀI thì hiển thị kết quả và bảng tra cứu lời giải chi tiết
else:
    # Tính điểm dựa trên các đáp án đã lưu
    score = 0
    if st.session_state.q1.startswith("C."): score += 1
    if st.session_state.q2.startswith("C."): score += 1
    if st.session_state.q3.startswith("C."): score += 1
    if st.session_state.q4.startswith("B."): score += 1
    if st.session_state.q5.startswith("A."): score += 1
    if st.session_state.q6.startswith("B."): score += 1
    if st.session_state.q7.startswith("D."): score += 1
    if st.session_state.q8.startswith("B."): score += 1
    if st.session_state.q9.startswith("D."): score += 1
    if st.session_state.q10.startswith("B."): score += 1

    st.balloons()
    st.success(f"🎉 Bạn đã hoàn thành bài thi! Tổng điểm của bạn: **{score}/10**")
    
    if st.button("🔄 Làm lại bài thi từ đầu"):
        st.session_state.submitted = False
        st.rerun()

    st.markdown("---")
    st.header("📖 XEM LỜI GIẢI CHI TIẾT TỪNG CÂU")

    # Tạo các khung hiển thị lời giải chi tiết cho từng câu
    with st.expander("🔍 Câu 1: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **C. 2**")
        st.markdown("**Hướng dẫn giải:** Dựa vào bảng biến thiên của $f'(x)$, ta thấy $f'(x)$ đổi dấu 2 lần (từ âm sang dương và ngược lại) nên hàm số có 2 điểm cực trị.")

    with st.expander("🔍 Câu 2: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **C. $(-\infty; -2)$**")
        st.markdown("**Hướng dẫn giải:** Quan sát đồ thị hàm bậc bốn, nhánh đi xuống tương ứng với khoảng nghịch biến $(-\infty; -2)$ và $(0; 2)$, nhánh đi lên tương ứng với khoảng đồng biến $(-2; 0)$ và $(2; +\infty)$.")

    with st.expander("🔍 Câu 3: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **C. $(1; 3)$**")
        st.markdown("**Hướng dẫn giải:** Trên bảng biến thiên, tại khoảng $(1; 3)$ thì $y' < 0$, do đó hàm số nghịch biến trên khoảng này.")

    with st.expander("🔍 Câu 4: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **B. $(-1; 1)$**")
        st.markdown("**Hướng dẫn giải:** Hàm số $y=f(x)$ đồng biến khi $f'(x) \ge 0$. Dựa vào đồ thị $f'(x)$, đồ thị nằm phía trên trục hoành (mang dấu dương) trên các khoảng $(-1; 1)$ và $(4; +\infty)$.")

    with st.expander("🔍 Câu 5: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **A. $y = -x^3 + 3x^2 - 9x$**")
        st.markdown("**Hướng dẫn giải:** Ta tính đạo hàm $y' = -3x^2 + 6x - 9 = -3(x-1)^2 - 6 < 0, \forall x \in \mathbb{R}$. Do đó hàm số nghịch biến trên toàn bộ tập số thực $\mathbb{R}$.")

    with st.expander("🔍 Câu 6: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **B. $x = -1$**")
        st.markdown("**Hướng dẫn giải:** Dựa vào đồ thị, tại điểm $x = -1$ thì đồ thị đạt giá trị cao nhất trong một lân cận, tức là hàm số đạt cực đại tại hoành độ $x = -1$.")

    with st.expander("🔍 Câu 7: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **D. $-20$**")
        st.markdown("**Hướng dẫn giải:** Giá trị cực tiểu ($y_{CT}$) của hàm số chính là giá trị của tung độ tại điểm cực tiểu. Dựa vào bảng biến thiên, giá trị cực tiểu là $-20$.")

    with st.expander("🔍 Câu 8: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **B. Hàm số đồng biến trên $(-\infty; -1)$ và $(-1; +\infty)$**")
        st.markdown("**Hướng dẫn giải:** Tập xác định $D = \mathbb{R} \setminus \{-1\}$. Ta có $y' = \frac{3}{(x+1)^2} > 0, \forall x \neq -1$. Vậy hàm số đồng biến trên từng khoảng xác định.")

    with st.expander("🔍 Câu 9: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **D. $(-4; -1)$ và $(-1; 2)$**")
        st.markdown("**Hướng dẫn giải:** Tính đạo hàm $y' = \frac{x^2 + 2x - 8}{(x+1)^2}$. Cho $y' < 0 \Leftrightarrow x^2 + 2x - 8 < 0 \Leftrightarrow -4 < x < 2$ (kết hợp điều kiện $x \neq -1$).")

    with st.expander("🔍 Câu 10: Xem đáp án và lời giải chi tiết"):
        st.markdown("**Đáp án đúng:** **B. $(-\infty; -1)$**")
        st.markdown("**Hướng dẫn giải:** Ta có phương trình $f'(x) = 0$ tại $x = 0$, $x = -1$, $x = 3$ (trong đó $x = 0 nghiệm bội lẻ/chẵn tùy cấu trúc, xét dấu khoảng ta thu được khoảng đồng biến là $(-\infty; -1)$).")
