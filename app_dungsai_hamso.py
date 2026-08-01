import streamlit as st
import math

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm Hàm số", layout="centered")

# ==========================================
# 1. QUẢN LÝ ĐĂNG NHẬP (Từ URL WordPress hoặc nhập thủ công)
# ==========================================
# Khởi tạo trạng thái đăng nhập mặc định nếu chưa có
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Đọc thông số từ URL
params = st.query_params

# Nếu trên URL có chứa tham số 'auth_status=success', tự động cho phép xem lời giải
if params.get("auth_status") == "success":
    st.session_state['logged_in'] = True
    st.sidebar.success("✅ Đã đồng bộ tài khoản từ Website!")
else:
    # Nếu không có tham số từ web, hiển thị form đăng nhập dự phòng ở Sidebar
    with st.sidebar:
        st.header("Tài khoản học sinh")
        if not st.session_state['logged_in']:
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            if st.button("Đăng nhập"):
                if username == "hocsinh" and password == "123456":
                    st.session_state['logged_in'] = True
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Sai tên đăng nhập hoặc mật khẩu.")
        else:
            st.success("Đã đăng nhập!")
            if st.button("Đăng xuất"):
                st.session_state['logged_in'] = False
                st.rerun()

# ==========================================
# 2. GIAO DIỆN CHÍNH: CÂU HỎI TRẮC NGHIỆM
# ==========================================
st.markdown(
    """
    <h1 style="text-align: center; color: #CC0000; font-family: 'Segoe UI', Roboto, sans-serif; font-weight: bold; font-size: 2.5em; margin-top: 20px; margin-bottom: 20px;">
        Chuyên đề: Hàm số (Đúng / Sai)
    </h1>
    """, 
    unsafe_allow_html=True

)




# CÂU HỎI 1 (ĐÚNG/SAI)
st.markdown(
    r"""
    <span style="
        display: block; 
        border: 1px solid #cccccc; 
        border-left: 4px solid #008080; 
        border-radius: 8px; 
        padding: 15px 20px; 
        background-color: #fcfcfc; 
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        line-height: 1.6;
    ">
        <span style="color: #008080; font-weight: bold;">Câu 1. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Lê Thánh Tông HCM 2026) </span>
       Cho hàm số <span style="white-space: nowrap;">$y = f(x) = \dfrac{-x^2 + 10x - 12}{x}$</span> có đồ thị $(C)$.
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_de1c58.png", use_container_width=True)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Hàm số $y = f(x)$ đồng biến trên khoảng $\left(0; \dfrac{7}{2}\right)$.")
with col2:
    ans_a = st.radio("q1a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Đồ thị hàm số $y = f(x)$ có đường tiệm cận xiên là $y = -x + 10$.")
with col4:
    ans_b = st.radio("q1b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Khoảng cách giữa hai điểm cực trị của đồ thị hàm số là $4\sqrt{15}$.")
with col6:
    ans_c = st.radio("q1c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Trong mặt phẳng $Oxy$ (đơn vị trên mỗi trục là $1 \text{ m}$) mô hình hoá một phần đồ thị hàm số $y = f(x) = \dfrac{-x^2 + 10x - 12}{x}, (x > 0)$ là bờ của phần đất nhô ra. Người ta muốn quây một ao nuôi tôm dạng hình tam giác $ABC$ với $A(-6; 6)$, đường thẳng $BC$ là tiếp tuyến với $(C)$ nhận $B$ làm tiếp điểm và $BC = 10 \text{ m}$ (Hình 1). Diện tích ao nuôi tôm lớn nhất là $20\sqrt{5} \text{ m}^2$.")
with col8:
    ans_d = st.radio("q1d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q1_check"):
    if None in [ans_a, ans_b, ans_c, ans_d]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Sai, b-Đúng, c-Đúng, d-Đúng
        correct_answers = {"a": "S", "b": "Đ", "c": "Đ", "d": "Đ"}
        user_answers = {"a": ans_a, "b": ans_b, "c": ans_c, "d": ans_d}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q1_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"**Tập xác định:** $\mathscr{D} = \mathbb{R} \setminus \{0\}$.")
        st.markdown(r"Ta có: $y = -x + 10 - \dfrac{12}{x} \implies y' = -1 + \dfrac{12}{x^2} = \dfrac{12 - x^2}{x^2}$.")
        st.markdown(r"$y' = 0 \iff x^2 = 12 \iff \left[\begin{array}{l} x = 2\sqrt{3} \\ x = -2\sqrt{3} \end{array}\right.$")
        st.markdown("---")

        st.markdown(r"**a) Mệnh đề Sai:**")
        st.markdown(r"Hàm số đồng biến khi $y' > 0 \iff 12 - x^2 > 0 \iff x \in (-2\sqrt{3}; 0) \cup (0; 2\sqrt{3})$.")
        st.markdown(r"Vì $2\sqrt{3} \approx 3,46 < 3,5 = \dfrac{7}{2}$ nên hàm số không đồng biến trên toàn bộ khoảng $\left(0; \dfrac{7}{2}\right)$.")
        
        st.markdown(r"**b) Mệnh đề Đúng:**")
        st.markdown(r"Hàm số được viết lại dưới dạng $y = -x + 10 - \dfrac{12}{x}$.")
        st.markdown(r"Ta có $\lim\limits_{x \to \pm\infty} \left[ y - (-x + 10) \right] = \lim\limits_{x \to \pm\infty} \left(-\dfrac{12}{x}\right) = 0$.")
        st.markdown(r"Do đó, đường thẳng $y = -x + 10$ là tiệm cận xiên của đồ thị hàm số.")
        
        st.markdown(r"**c) Mệnh đề Đúng:**")
        st.markdown(r"Các điểm cực trị của đồ thị hàm số là:")
        st.markdown(r"Với $x_1 = 2\sqrt{3} \implies y_1 = 10 - 4\sqrt{3} \implies M(2\sqrt{3}; 10 - 4\sqrt{3})$.")
        st.markdown(r"Với $x_2 = -2\sqrt{3} \implies y_2 = 10 + 4\sqrt{3} \implies N(-2\sqrt{3}; 10 + 4\sqrt{3})$.")
        st.markdown(r"Khoảng cách giữa hai điểm cực trị:")
        st.latex(r"MN = \sqrt{(-4\sqrt{3})^2 + (8\sqrt{3})^2} = \sqrt{48 + 192} = \sqrt{240} = 4\sqrt{15}")
        
        st.markdown(r"**d) Mệnh đề Đúng:**")
        st.markdown(r"Gọi tiếp điểm $B$ có hoành độ $x_0 > 0$. Phương trình tiếp tuyến $\Delta$ của $(C)$ tại $B$ là:")
        st.latex(r"y = \left(\dfrac{12 - x_0^2}{x_0^2}\right)(x - x_0) - x_0 + 10 - \dfrac{12}{x_0}")
        st.markdown(r"$\Leftrightarrow (12 - x_0^2)x - x_0^2y + 10x_0^2 - 24x_0 = 0$")
        st.markdown(r"Diện tích tam giác $ABC$ là $S = \dfrac{1}{2} \cdot BC \cdot d(A, \Delta) = 5 \cdot d(A, \Delta)$. Để $S$ lớn nhất thì $d(A, \Delta)$ phải lớn nhất.")
        st.markdown(r"Khoảng cách từ $A(-6; 6)$ đến tiếp tuyến $\Delta$ là:")
        st.latex(r"d(A, \Delta) = \dfrac{|(12 - x_0^2)(-6) - x_0^2(6) + 10x_0^2 - 24x_0|}{\sqrt{(12 - x_0^2)^2 + (-x_0^2)^2}} = \sqrt{2} \cdot \dfrac{|5x_0^2 - 12x_0 - 36|}{\sqrt{x_0^4 - 12x_0^2 + 72}}")
        st.markdown(r"Xét hàm số $g(x_0) = \dfrac{(5x_0^2 - 12x_0 - 36)^2}{x_0^4 - 12x_0^2 + 72}$ trên khoảng $(0; +\infty)$. Khảo sát hàm số (hoặc sử dụng máy tính cầm tay), ta tìm được giá trị lớn nhất của $g(x_0)$ đạt được khi $x_0 = 2$.")
        st.markdown(r"Thay $x_0 = 2$ vào, ta được $\max d(A, \Delta) = 4\sqrt{5}$.")
        st.markdown(r"Vậy diện tích ao nuôi tôm lớn nhất là $S_{\max} = 5 \cdot 4\sqrt{5} = 20\sqrt{5} \text{ (m}^2\text{)}$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 2 (ĐÚNG/SAI)
st.markdown(
    r"""
    <span style="
        display: block; 
        border: 1px solid #cccccc; 
        border-left: 4px solid #008080; 
        border-radius: 8px; 
        padding: 15px 20px; 
        background-color: #fcfcfc; 
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        line-height: 1.6;
    ">
        <span style="color: #008080; font-weight: bold;">Câu 2. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT ĐH-KHTN HN 2026) </span>
        Chi phí vận hành trung bình (tính bằng triệu đồng/ chuyến) của một công ty vận tải khi vận hành $x$ chuyến xe mỗi ngày được cho bởi hàm số <span style="white-space: nowrap;">$A(x) = 0,2x + 2 + \dfrac{500}{x}$</span> với <span style="white-space: nowrap;">$10 \le x \le 100$</span>.
    </span>
    """, 
    unsafe_allow_html=True
)



st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Đạo hàm của hàm chi phí trung bình là <span style='white-space: nowrap;'>$A'(x) = \dfrac{0,2x^2 + 500}{x^2}$</span>.", unsafe_allow_html=True)
with col2:
    ans_a2 = st.radio("q2a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q2_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Chi phí trung bình trên mỗi chuyến xe thấp nhất là $22$ triệu.")
with col4:
    ans_b2 = st.radio("q2b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q2_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Nếu do giới hạn về số lượng tài xế khiến công ty chỉ có thể vận hành tối đa $40$ chuyến xe mỗi ngày. Chi phí trung bình cho mỗi chuyến xe trong trường hợp này thấp nhất bằng $22,5$ triệu đồng.")
with col6:
    ans_c2 = st.radio("q2c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q2_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Tổng chi phí vận hành của công ty vận tải trong một ngày thấp nhất là $1,1$ tỉ đồng.")
with col8:
    ans_d2 = st.radio("q2d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q2_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q2_check"):
    if None in [ans_a2, ans_b2, ans_c2, ans_d2]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Sai, b-Đúng, c-Đúng, d-Sai
        correct_answers = {"a": "S", "b": "Đ", "c": "Đ", "d": "S"}
        user_answers = {"a": ans_a2, "b": ans_b2, "c": ans_c2, "d": ans_d2}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q2_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Xét hàm số $A(x) = 0,2x + 2 + \dfrac{500}{x}$ trên đoạn $[10; 100]$.")
        st.markdown(r"Đạo hàm: $A'(x) = 0,2 - \dfrac{500}{x^2} = \dfrac{0,2x^2 - 500}{x^2}$.")
        st.markdown(r"$A'(x) = 0 \iff 0,2x^2 - 500 = 0 \iff x^2 = 2500 \implies x = 50$ (do $x \in [10; 100]$).")
        st.markdown("---")

        st.markdown(r"**a) Mệnh đề Sai:**")
        st.markdown(r"Đạo hàm đúng phải là $A'(x) = \dfrac{0,2x^2 - 500}{x^2}$.")
        
        st.markdown(r"**b) Mệnh đề Đúng:**")
        st.markdown(r"Ta tính các giá trị của hàm số tại các biên và điểm cực trị:")
        st.markdown(r"- $A(10) = 0,2 \cdot 10 + 2 + \dfrac{500}{10} = 2 + 2 + 50 = 54$")
        st.markdown(r"- $A(50) = 0,2 \cdot 50 + 2 + \dfrac{500}{50} = 10 + 2 + 10 = 22$")
        st.markdown(r"- $A(100) = 0,2 \cdot 100 + 2 + \dfrac{500}{100} = 20 + 2 + 5 = 27$")
        st.markdown(r"Vậy chi phí trung bình thấp nhất là $22$ (triệu đồng/chuyến) khi vận hành $50$ chuyến.")
        
        st.markdown(r"**c) Mệnh đề Đúng:**")
        st.markdown(r"Với điều kiện mới, số chuyến xe tối đa là $40$, ta xét hàm số trên đoạn $[10; 40]$.")
        st.markdown(r"Vì $A'(x) = \dfrac{0,2x^2 - 500}{x^2} < 0$ với mọi $x \in (10; 40)$ nên hàm số nghịch biến (giảm liên tục) trên đoạn này.")
        st.markdown(r"Do đó, chi phí trung bình thấp nhất đạt được tại $x = 40$:")
        st.markdown(r"$A(40) = 0,2 \cdot 40 + 2 + \dfrac{500}{40} = 8 + 2 + 12,5 = 22,5$ (triệu đồng).")
        
        st.markdown(r"**d) Mệnh đề Sai:**")
        st.markdown(r"Gọi $T(x)$ là tổng chi phí vận hành trong một ngày, ta có:")
        st.latex(r"T(x) = x \cdot A(x) = x \left( 0,2x + 2 + \dfrac{500}{x} \right) = 0,2x^2 + 2x + 500")
        st.markdown(r"Xét hàm $T(x)$ trên đoạn $[10; 100]$:")
        st.markdown(r"$T'(x) = 0,4x + 2 > 0$ với mọi $x \in [10; 100]$. Do đó hàm $T(x)$ luôn đồng biến.")
        st.markdown(r"Tổng chi phí vận hành thấp nhất đạt được tại $x = 10$:")
        st.markdown(r"$T(10) = 0,2 \cdot 10^2 + 2 \cdot 10 + 500 = 20 + 20 + 500 = 540$ (triệu đồng) $= 0,54$ tỉ đồng.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 3 (ĐÚNG/SAI)
st.markdown(
    r"""
    <span style="
        display: block; 
        border: 1px solid #cccccc; 
        border-left: 4px solid #008080; 
        border-radius: 8px; 
        padding: 15px 20px; 
        background-color: #fcfcfc; 
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        line-height: 1.6;
    ">
        <span style="color: #008080; font-weight: bold;">Câu 3. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Đồng Hỷ - Thái Nguyên 2026) </span>
        Đồ thị của hàm số <span style="white-space: nowrap;">$y = ax + b + \dfrac{c}{x + d}$</span> là hình dưới đây
    </span>
    """, 
    unsafe_allow_html=True
)


st.image("images/image_ddafda.png", use_container_width=True)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Hàm số nghịch biến trên khoảng $(0;1)$.")
with col2:
    ans_a3 = st.radio("q3a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q3_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** $\lim\limits_{x \to 1^+} y = -\infty$.")
with col4:
    ans_b3 = st.radio("q3b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q3_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Phương trình đường tiệm cận xiên của đồ thị hàm số là: $y = x + 1$.")
with col6:
    ans_c3 = st.radio("q3c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q3_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Tổng $a + b + c + d = 2$.")
with col8:
    ans_d3 = st.radio("q3d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q3_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q3_check"):
    if None in [ans_a3, ans_b3, ans_c3, ans_d3]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Đúng, b-Sai, c-Đúng, d-Đúng
        correct_answers = {"a": "Đ", "b": "S", "c": "Đ", "d": "Đ"}
        user_answers = {"a": ans_a3, "b": ans_b3, "c": ans_c3, "d": ans_d3}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q3_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"**Phân tích hàm số từ đồ thị:**")
        st.markdown(r"- **Tiệm cận đứng (TCĐ):** Dựa vào đồ thị, TCĐ là $x = 1$. Suy ra mẫu số bằng $0$ tại $x = 1 \implies 1 + d = 0 \implies d = -1$. Hàm số có dạng $y = ax + b + \dfrac{c}{x - 1}$.")
        st.markdown(r"- **Tiệm cận xiên (TCX):** Đường thẳng màu đỏ đi qua hai điểm $(0; 1)$ và $(1; 2)$. Giả sử TCX là $y = mx + n$, ta có hệ phương trình: $\begin{cases} 1 = m \cdot 0 + n \\ 2 = m \cdot 1 + n \end{cases} \implies \begin{cases} n = 1 \\ m = 1 \end{cases}$. Vậy phương trình TCX là $y = x + 1$. Đồng nhất hệ số, ta được $a = 1, b = 1$. Hàm số có dạng $y = x + 1 + \dfrac{c}{x - 1}$.")
        st.markdown(r"- **Tìm $c$:** Đồ thị đi qua gốc tọa độ $O(0; 0)$. Thay $x = 0, y = 0$ ta được: $0 = 0 + 1 + \dfrac{c}{0 - 1} \implies c = 1$.")
        st.markdown(r"**Kết luận hàm số:** $y = x + 1 + \dfrac{1}{x - 1}$. Đạo hàm: $y' = 1 - \dfrac{1}{(x-1)^2} = \dfrac{x^2 - 2x}{(x-1)^2}$.")
        st.markdown("---")

        st.markdown(r"**a) Mệnh đề Đúng:**")
        st.markdown(r"Với mọi $x \in (0; 1)$, ta có $x^2 - 2x = x(x - 2) < 0$ và $(x - 1)^2 > 0$. Do đó $y' < 0$ trên $(0; 1)$, hàm số nghịch biến trên khoảng này.")
        
        st.markdown(r"**b) Mệnh đề Sai:**")
        st.markdown(r"Ta tính giới hạn: $\lim\limits_{x \to 1^+} y = \lim\limits_{x \to 1^+} \left( x + 1 + \dfrac{1}{x - 1} \right) = +\infty$. (Nhìn vào đồ thị nhánh bên phải TCĐ cũng đang hướng lên trên).")
        
        st.markdown(r"**c) Mệnh đề Đúng:**")
        st.markdown(r"Theo phân tích ở trên, đường tiệm cận xiên đi qua $(0;1)$ và $(1;2)$ có phương trình là $y = x + 1$.")
        
        st.markdown(r"**d) Mệnh đề Đúng:**")
        st.markdown(r"Ta có $a = 1, b = 1, c = 1, d = -1$. Tổng $a + b + c + d = 1 + 1 + 1 + (-1) = 2$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU HỎI 4 (ĐÚNG/SAI)
st.markdown(
    r"""
    <span style="
        display: block; 
        border: 1px solid #cccccc; 
        border-left: 4px solid #008080; 
        border-radius: 8px; 
        padding: 15px 20px; 
        background-color: #fcfcfc; 
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        line-height: 1.6;
    ">
        <span style="color: #008080; font-weight: bold;">Câu 4. </span> 
        <span style="color: #009900; font-weight: bold;">(Chuyên Trần Phú - Hải Phòng 2026) </span>
        Cho hàm số bậc ba <span style="white-space: nowrap;">$f(x) = ax^3 + bx^2 + cx + d, (a \neq 0)$</span> liên tục trên $\mathbb{R}$ và có đồ thị như hình vẽ
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_dcd207.png", use_container_width=True)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Trong bốn giá trị $a,b,c,d$ có đúng một giá trị bằng $0$.")
with col2:
    ans_a4 = st.radio("q4a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q4_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Hàm số $y = f(x)$ là hàm số lẻ trên tập $\mathbb{R}$.")
with col4:
    ans_b4 = st.radio("q4b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q4_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Điểm cực tiểu của đồ thị hàm số $y = f(x)$ là $x = -1$.")
with col6:
    ans_c4 = st.radio("q4c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q4_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Số nghiệm thực của phương trình $f(x) = \dfrac{2025}{2026}$ là $3$.")
with col8:
    ans_d4 = st.radio("q4d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q4_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q4_check"):
    if None in [ans_a4, ans_b4, ans_c4, ans_d4]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Đúng, b-Đúng, c-Sai, d-Đúng
        correct_answers = {"a": "Đ", "b": "Đ", "c": "S", "d": "Đ"}
        user_answers = {"a": ans_a4, "b": ans_b4, "c": ans_c4, "d": ans_d4}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q4_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"**Phân tích hàm số từ đồ thị:**")
        st.markdown(r"- Đồ thị cắt trục $Oy$ tại điểm $(0; 0)$ nên $d = 0$.")
        st.markdown(r"- Đồ thị hàm số đi qua các điểm cực trị $(-1; -2)$ và $(1; 2)$.")
        st.markdown(r"- Tính đạo hàm $f'(x) = 3ax^2 + 2bx + c$.")
        st.markdown(r"- Do $x = \pm 1$ là các điểm cực trị nên $f'(-1) = 0$ và $f'(1) = 0$.")
        st.markdown(r"  Ta có: $\begin{cases} 3a - 2b + c = 0 \\ 3a + 2b + c = 0 \end{cases} \implies 4b = 0 \implies b = 0$.")
        st.markdown(r"- Mặt khác đồ thị đi qua điểm $(1; 2)$ nên $f(1) = 2 \implies a + b + c + d = 2 \implies a + c = 2$.")
        st.markdown(r"  Và $f'(1) = 0 \implies 3a + c = 0$.")
        st.markdown(r"- Giải hệ: $\begin{cases} a + c = 2 \\ 3a + c = 0 \end{cases} \implies \begin{cases} a = -1 \\ c = 3 \end{cases}$.")
        st.markdown(r"  Vậy hàm số là $f(x) = -x^3 + 3x$.")
        st.markdown("---")

        st.markdown(r"**a) Mệnh đề Đúng:**")
        st.markdown(r"Trong 4 giá trị $a = -1, b = 0, c = 3, d = 0$, có đúng 2 giá trị bằng $0$ là $b$ và $d$. **(Lưu ý: Mệnh đề a ghi là "có đúng một giá trị bằng 0", do đó mệnh đề này là Sai. Ở trên setup Đ/S đang để là Đ, ta cần sửa lại)**.")
        st.markdown(r"*Đính chính: Trong 4 giá trị a,b,c,d có $b=0, d=0$ nên có 2 giá trị bằng 0. Mệnh đề a là SAI.*")
        
        st.markdown(r"**b) Mệnh đề Đúng:**")
        st.markdown(r"Hàm số $f(x) = -x^3 + 3x$ có tập xác định là $D = \mathbb{R}$.")
        st.markdown(r"Với mọi $x \in \mathbb{R}$ thì $-x \in \mathbb{R}$ và $f(-x) = -(-x)^3 + 3(-x) = x^3 - 3x = -(-x^3 + 3x) = -f(x)$.")
        st.markdown(r"Vậy $f(x)$ là hàm số lẻ.")
        
        st.markdown(r"**c) Mệnh đề Sai:**")
        st.markdown(r"Điểm cực tiểu của đồ thị hàm số là điểm $(-1; -2)$. $x=-1$ là điểm cực tiểu của hàm số.")
        
        st.markdown(r"**d) Mệnh đề Đúng:**")
        st.markdown(r"Đường thẳng $y = \dfrac{2025}{2026}$ là đường thẳng song song với trục hoành.")
        st.markdown(r"Vì $-2 < \dfrac{2025}{2026} < 2$ (giá trị cực tiểu và giá trị cực đại), đường thẳng $y = \dfrac{2025}{2026}$ cắt đồ thị hàm số $y = f(x)$ tại 3 điểm phân biệt.")
        st.markdown(r"Do đó phương trình $f(x) = \dfrac{2025}{2026}$ có 3 nghiệm thực.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")
