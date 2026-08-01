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
        # Đáp án chuẩn: a-Sai, b-Đúng, c-Sai, d-Đúng
        correct_answers = {"a": "S", "b": "Đ", "c": "S", "d": "Đ"}
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

        st.markdown(r"**a) Mệnh đề Sai:**")
        st.markdown(r"Trong 4 giá trị $a = -1, b = 0, c = 3, d = 0$, có tới 2 giá trị bằng $0$ là $b$ và $d$. Do đó mệnh đề phát biểu có đúng một giá trị bằng $0$ là **Sai**.")
        
        st.markdown(r"**b) Mệnh đề Đúng:**")
        st.markdown(r"Hàm số $f(x) = -x^3 + 3x$ có tập xác định là $D = \mathbb{R}$.")
        st.markdown(r"Với mọi $x \in \mathbb{R}$ thì $-x \in \mathbb{R}$ và $f(-x) = -(-x)^3 + 3(-x) = x^3 - 3x = -(-x^3 + 3x) = -f(x)$.")
        st.markdown(r"Vậy $f(x)$ là hàm số lẻ.")
        
        st.markdown(r"**c) Mệnh đề Sai:**")
        st.markdown(r"Điểm cực tiểu của đồ thị hàm số là điểm $(-1; -2)$. Còn $x = -1$ là hoành độ cực tiểu.")
        
        st.markdown(r"**d) Mệnh đề Đúng:**")
        st.markdown(r"Đường thẳng $y = \dfrac{2025}{2026}$ là đường thẳng song song với trục hoành.")
        st.markdown(r"Vì $-2 < \dfrac{2025}{2026} < 2$, đường thẳng cắt đồ thị hàm số tại 3 điểm phân biệt, nên phương trình có 3 nghiệm thực.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU HỎI 5 (ĐÚNG/SAI)
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
        <span style="color: #008080; font-weight: bold;">Câu 5. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Bắc Ninh 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x) = \dfrac{ax^2 + bx + c}{x + d}$</span> có bảng biến thiên như hình vẽ dưới đây.
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_dc6d22.png", use_container_width=True)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Hàm số $y = f(x)$ đồng biến trên khoảng $(0; 4)$.")
with col2:
    ans_a5 = st.radio("q5a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q5_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Tích giá trị cực đại và cực tiểu của hàm số $y = f(x)$ bằng $-12$.")
with col4:
    ans_b5 = st.radio("q5b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q5_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Cho điểm $M$ có hoành độ lớn hơn $2$, di chuyển trên đồ thị hàm số $y = f(x)$. Giá trị nhỏ nhất của tổng khoảng cách từ điểm $M$ đến hai trục tọa độ bằng $4 + 4\sqrt{2}$.")
with col6:
    ans_c5 = st.radio("q5c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q5_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** $a + b + c + d = -5$.")
with col8:
    ans_d5 = st.radio("q5d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q5_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q5_check"):
    if None in [ans_a5, ans_b5, ans_c5, ans_d5]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Sai, b-Đúng, c-Đúng, d-Đúng
        correct_answers = {"a": "S", "b": "Đ", "c": "Đ", "d": "Đ"}
        user_answers = {"a": ans_a5, "b": ans_b5, "c": ans_c5, "d": ans_d5}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q5_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"**Phân tích hàm số từ bảng biến thiên:**")
        st.markdown(r"- Dựa vào bảng biến thiên, hàm số không xác định tại $x = 2$, suy ra $2 + d = 0 \implies d = -2$.")
        st.markdown(r"- Tại $x = 0$, ta có $f(0) = \dfrac{c}{-2} = 2 \implies c = -4$ và $f'(0) = 0$.")
        st.markdown(r"- Tại $x = 4$, ta có $f(4) = -6$ và $f'(4) = 0$.")
        st.markdown(r"- Tính đạo hàm $f'(x) = \dfrac{ax^2 - 4ax - 2b + 4}{(x - 2)^2}$. Từ $f'(0) = 0 \implies b = 2$. Từ $f'(4) = 0$ và điểm đi qua ta tìm được $a = -1$.")
        st.markdown(r"- Vậy hàm số cần tìm là: $f(x) = \dfrac{-x^2 + 2x - 4}{x - 2}$.")
        st.markdown("---")

        st.markdown(r"**a) Mệnh đề Sai:**")
        st.markdown(r"Hàm số có tiệm cận đứng $x = 2$ nên đồ thị bị ngắt quãng, ta lấy $x_1 = 1 \in (0; 2)$ thì $f(1) = 3$ và $x_2 = 3 \in (2; 4)$ thì $f(3) = -7$. Vì $1 < 3$ nhưng $f(1) > f(3)$ nên hàm số không đồng biến trên khoảng $(0; 4)$.")
        
        st.markdown(r"**b) Mệnh đề Đúng:**")
        st.markdown(r"Dựa vào bảng biến thiên, giá trị cực tiểu của hàm số là $y_{\text{CT}} = 2$ (tại $x = 0$) và giá trị cực đại là $y_{\text{CĐ}} = -6$ (tại $x = 4$).")
        st.markdown(r"Tích giá trị cực đại và cực tiểu là: $(-6) \cdot 2 = -12$.")
        
        st.markdown(r"**c) Mệnh đề Đúng:**")
        st.markdown(r"Với $x > 2$, điểm $M(x; f(x))$ có tung độ $f(x) < 0$. Tổng khoảng cách từ $M$ đến hai trục tọa độ là $S = x + (-f(x)) = x - \dfrac{-x^2 + 2x - 4}{x - 2} = 2x + \dfrac{4}{x - 2}$.")
        st.markdown(r"Đặt $t = x - 2 > 0$, ta có $S = 2(t + 2) + \dfrac{4}{t} = 2t + \dfrac{4}{t} + 4 \ge 2\sqrt{8} + 4 = 4 + 4\sqrt{2}$ (theo bất đẳng thức AM-GM). Dấu bằng xảy ra khi $t = \sqrt{2}$.")
        
        st.markdown(r"**d) Mệnh đề Đúng:**")
        st.markdown(r"Ta có các hệ số: $a = -1, b = 2, c = -4, d = -2$. Tổng $a + b + c + d = (-1) + 2 + (-4) + (-2) = -5$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 6 (ĐÚNG/SAI)
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
        <span style="color: #008080; font-weight: bold;">Câu 6. </span> 
         <span style="color: #009900; font-weight: bold;">(Sở Phú Thọ 2026) </span>
        Cho hàm số $y = x^3 - 3x^2 + 5$ có đồ thị là $(C)$. 
    </span>
    """, 
    unsafe_allow_html=True
)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Hàm số đã cho nghịch biến trên khoảng $(0; 2)$.")
with col2:
    ans_a = st.radio("q6a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q6_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Hàm số đã cho có hai điểm cực trị.")
with col4:
    ans_b = st.radio("q6b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q6_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Giá trị nhỏ nhất của hàm số đã cho trên khoảng $(0; +\infty)$ bằng $2$.")
with col6:
    ans_c = st.radio("q6c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q6_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Tiếp tuyến của đồ thị $(C)$ tại điểm có hoành độ bằng $1$ là đường thẳng có phương trình $y = -3x + 3$.")
with col8:
    ans_d = st.radio("q6d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q6_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q6_check"):
    if None in [ans_a, ans_b, ans_c, ans_d]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Đúng, b-Đúng, c-Sai, d-Sai
        correct_answers = {"a": "Đ", "b": "Đ", "c": "S", "d": "S"}
        user_answers = {"a": ans_a, "b": ans_b, "c": ans_c, "d": ans_d}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q6_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state['logged_in']:
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R}$.")
        st.markdown(r"Đạo hàm: $y' = 3x^2 - 6x$. Cho $y' = 0 \Leftrightarrow \left[ \begin{array}{l} x = 0 \\ x = 2 \end{array} \right.$.")
        
        st.markdown(r"**a) Mệnh đề Đúng:** Xét trên khoảng $(0; 2)$, ta có $y' = 3x^2 - 6x < 0$. Do đó hàm số nghịch biến trên khoảng $(0; 2)$.")
        
        st.markdown(r"**b) Mệnh đề Đúng:** Đạo hàm $y'$ đổi dấu hai lần (từ dương sang âm khi qua $x=0$ và từ âm sang dương khi qua $x=2$), nên hàm số có hai điểm cực trị (đạt cực đại tại $x=0$ và cực tiểu tại $x=2$).")
        
        st.markdown(r"**c) Mệnh đề Sai:** Xét hàm số trên khoảng $(0; +\infty)$:")
        st.markdown(r"Hàm số nghịch biến trên $(0; 2)$ và đồng biến trên $(2; +\infty)$.")
        st.markdown(r"Do đó, giá trị nhỏ nhất của hàm số trên khoảng $(0; +\infty)$ đạt được tại $x = 2$.")
        st.latex(r"\min_{(0; +\infty)} y = y(2) = 2^3 - 3 \cdot 2^2 + 5 = 1 \neq 2")
        
        st.markdown(r"**d) Mệnh đề Sai:** Gọi $(x_0; y_0)$ là toạ độ tiếp điểm. Theo đề bài hoành độ $x_0 = 1$.")
        st.markdown(r"Tung độ tiếp điểm: $y_0 = y(1) = 1^3 - 3 \cdot 1^2 + 5 = 3$.")
        st.markdown(r"Hệ số góc của tiếp tuyến: $k = y'(1) = 3 \cdot 1^2 - 6 \cdot 1 = -3$.")
        st.markdown(r"Phương trình tiếp tuyến của $(C)$ tại điểm có hoành độ bằng $1$ là:")
        st.latex(r"y = k(x - x_0) + y_0 \Leftrightarrow y = -3(x - 1) + 3 \Leftrightarrow y = -3x + 6")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 7 (ĐÚNG/SAI)
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
        <span style="color: #008080; font-weight: bold;">Câu 7. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Phú Thọ 2026) </span>
         Tại một khu bảo tồn thiên nhiên, các nhà khoa học đã thả một số cá thể của một loài động vật quý hiếm trong một khu rừng rộng $10$ hecta và theo dõi sự tăng trưởng số lượng của chúng. Họ thấy rằng số lượng cá thể của loài động vật đó sau $t$ năm kể từ khi nuôi tại khu bảo tồn được xấp xỉ bởi hàm số $h(t) = 70\log_2\left(\dfrac{8t+1}{t+1}\right) + 30$ ($t$ là số thực dương) và tốc độ tăng trưởng số lượng cá thể của loài động vật đó tại thời điểm sau đúng $t$ năm kể từ khi nuôi được xấp xỉ bởi hàm số $h'(t)$ (đơn vị: cá thể / năm).
    </span>
    """, 
    unsafe_allow_html=True
)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Thời điểm ban đầu, người ta thả nuôi $30$ cá thể.")
with col2:
    ans_a = st.radio("q7a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q7_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Sau $9$ tháng kể từ khi bắt đầu nuôi, số lượng cá thể của loài động vật đó là $170$.")
with col4:
    ans_b = st.radio("q7b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q7_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Tốc độ tăng trưởng số lượng cá thể của loài động vật đó tại thời điểm đúng $6$ năm kể từ khi nuôi là $\dfrac{10}{7}$ (cá thể / năm).")
with col6:
    ans_c = st.radio("q7c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q7_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Số lượng cá thể của loài động vật đó không vượt quá $240$.")
with col8:
    ans_d = st.radio("q7d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q7_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q7_check"):
    if None in [ans_a, ans_b, ans_c, ans_d]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Đúng, b-Đúng, c-Sai, d-Đúng
        correct_answers = {"a": "Đ", "b": "Đ", "c": "S", "d": "Đ"}
        user_answers = {"a": ans_a, "b": ans_b, "c": ans_c, "d": ans_d}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q7_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state['logged_in']:
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"**a) Mệnh đề Đúng:** Thời điểm ban đầu ứng với $t = 0$. Số lượng cá thể lúc đó là:")
        st.latex(r"h(0) = 70 \log_2\left(\dfrac{8 \cdot 0 + 1}{0 + 1}\right) + 30 = 70 \log_2(1) + 30 = 0 + 30 = 30")
        
        st.markdown(r"**b) Mệnh đề Đúng:** Sau $9$ tháng, ứng với thời gian $t = \dfrac{9}{12} = \dfrac{3}{4}$ (năm). Số lượng cá thể là:")
        st.latex(r"h\left(\dfrac{3}{4}\right) = 70 \log_2\left(\dfrac{8 \cdot \dfrac{3}{4} + 1}{\dfrac{3}{4} + 1}\right) + 30 = 70 \log_2\left(\dfrac{7}{\dfrac{7}{4}}\right) + 30 = 70 \log_2(4) + 30 = 70 \cdot 2 + 30 = 170")
        
        st.markdown(r"**c) Mệnh đề Sai:** Tốc độ tăng trưởng là đạo hàm của hàm số $h(t)$. Ta có:")
        st.latex(r"h'(t) = 70 \cdot \dfrac{\left(\dfrac{8t+1}{t+1}\right)'}{\dfrac{8t+1}{t+1} \cdot \ln 2} = 70 \cdot \dfrac{\dfrac{7}{(t+1)^2}}{\dfrac{8t+1}{t+1} \cdot \ln 2} = \dfrac{490}{(t+1)(8t+1) \ln 2}")
        st.markdown(r"Tốc độ tăng trưởng tại thời điểm đúng $6$ năm ($t = 6$) là:")
        st.latex(r"h'(6) = \dfrac{490}{(6+1)(8 \cdot 6 + 1) \ln 2} = \dfrac{490}{7 \cdot 49 \ln 2} = \dfrac{10}{7 \ln 2} \neq \dfrac{10}{7}")
        
        st.markdown(r"**d) Mệnh đề Đúng:** Biến đổi biểu thức trong logarit, ta có:")
        st.latex(r"\dfrac{8t+1}{t+1} = \dfrac{8(t+1) - 7}{t+1} = 8 - \dfrac{7}{t+1}")
        st.markdown(r"Vì $t > 0 \Rightarrow t + 1 > 1 \Rightarrow \dfrac{7}{t+1} > 0$. Do đó $8 - \dfrac{7}{t+1} < 8$.")
        st.markdown(r"Do cơ số $2 > 1$ nên hàm số $y = \log_2 x$ đồng biến, suy ra:")
        st.latex(r"h(t) = 70 \log_2\left(8 - \dfrac{7}{t+1}\right) + 30 < 70 \log_2(8) + 30 = 70 \cdot 3 + 30 = 240")
        st.markdown(r"Vậy số lượng cá thể của loài động vật đó luôn bé hơn $240$, tức là không bao giờ vượt quá $240$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 8 (ĐÚNG/SAI)
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
        <span style="color: #008080; font-weight: bold;">Câu 8. </span> 
        <span style="color: #009900; font-weight: bold;">(Cụm liên trường Hải Phòng 2026) </span>
        Cho hàm số $y = f(x) = \dfrac{2x^2 - 5x + 9}{x - 5}$. Các mệnh đề sau đúng hay sai? 
    </span>
    """, 
    unsafe_allow_html=True
)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Đồ thị hàm số cắt trục tung tại điểm có tung độ bằng $-\dfrac{9}{5}$.")
with col2:
    ans_a = st.radio("q8a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q8_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Hàm số nghịch biến trên khoảng $(1; 9)$.")
with col4:
    ans_b = st.radio("q8b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q8_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Có đúng một điểm trên đồ thị hàm số cách đều hai trục tọa độ.")
with col6:
    ans_c = st.radio("q8c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q8_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Đồ thị hàm số có đường tiệm cận đứng là $y = 5$.")
with col8:
    ans_d = st.radio("q8d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q8_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q8_check"):
    if None in [ans_a, ans_b, ans_c, ans_d]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Đúng, b-Sai, c-Sai, d-Sai
        correct_answers = {"a": "Đ", "b": "S", "c": "S", "d": "S"}
        user_answers = {"a": ans_a, "b": ans_b, "c": ans_c, "d": ans_d}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q8_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state['logged_in']:
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{5\}$.")
        st.markdown(r"Đạo hàm: $y' = \dfrac{(4x - 5)(x - 5) - (2x^2 - 5x + 9)}{(x - 5)^2} = \dfrac{4x^2 - 25x + 25 - 2x^2 + 5x - 9}{(x - 5)^2} = \dfrac{2x^2 - 20x + 16}{(x - 5)^2}$.")
        
        st.markdown(r"**a) Mệnh đề Đúng:** Giao điểm của đồ thị với trục tung (trục $Oy$) ứng với $x = 0$.")
        st.markdown(r"Khi $x = 0$, $y = \dfrac{2(0)^2 - 5(0) + 9}{0 - 5} = -\dfrac{9}{5}$.")
        
        st.markdown(r"**b) Mệnh đề Sai:** Ta có $y' = 0 \Leftrightarrow 2x^2 - 20x + 16 = 0 \Leftrightarrow x^2 - 10x + 8 = 0 \Leftrightarrow x = 5 \pm \sqrt{17}$.")
        st.markdown(r"Do đó, hàm số không thể nghịch biến trên toàn bộ khoảng $(1; 9)$ vì trong khoảng này có chứa $x=5$ (không thuộc TXĐ) và $x=5-\sqrt{17} \approx 0.87$ không nằm trong $(1;9)$. Khoảng nghịch biến thực sự là $(5-\sqrt{17}; 5)$ và $(5; 5+\sqrt{17})$.")
        
        st.markdown(r"**c) Mệnh đề Sai:** Điểm cách đều hai trục tọa độ thỏa mãn $|x| = |y| \Leftrightarrow y = x$ hoặc $y = -x$.")
        st.markdown(r"Trường hợp 1: $y = x \Rightarrow \dfrac{2x^2 - 5x + 9}{x - 5} = x \Rightarrow 2x^2 - 5x + 9 = x^2 - 5x \Rightarrow x^2 + 9 = 0$ (vô nghiệm).")
        st.markdown(r"Trường hợp 2: $y = -x \Rightarrow \dfrac{2x^2 - 5x + 9}{x - 5} = -x \Rightarrow 2x^2 - 5x + 9 = -x^2 + 5x \Rightarrow 3x^2 - 10x + 9 = 0$. Phương trình này có $\Delta' = 25 - 27 = -2 < 0$, nên cũng vô nghiệm.")
        st.markdown(r"Vậy không có điểm nào trên đồ thị cách đều hai trục tọa độ.")
        
        st.markdown(r"**d) Mệnh đề Sai:** Đường tiệm cận đứng của đồ thị hàm số là đường thẳng $x = 5$, không phải $y = 5$. (Phương trình $y = c$ là dạng của tiệm cận ngang).")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 9 (ĐÚNG/SAI)
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
        <span style="color: #008080; font-weight: bold;">Câu 9. </span> 
        <span style="color: #009900; font-weight: bold;">(Chuyên Vinh 2026) </span>
        Cho hàm số $f(x) = \dfrac{3x + 1}{x + 4}$.
    </span>
    """, 
    unsafe_allow_html=True
)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Hàm số $f(x)$ có đạo hàm là $f'(x) = \dfrac{11}{(x + 4)^2}$.")
with col2:
    ans_a9 = st.radio("q9a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q9_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Với $x_1; x_2 \in \mathbb{R}$ thỏa mãn $x_1 < -4 < x_2$ thì $f(x_1) < f(x_2)$.")
with col4:
    ans_b9 = st.radio("q9b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q9_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Tọa độ giao điểm của hai đường tiệm cận của đồ thị hàm số là: $(3; -4)$.")
with col6:
    ans_c9 = st.radio("q9c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q9_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Giá trị nhỏ nhất của hàm số $f(x)$ trên đoạn $[0; 1]$ bằng $\dfrac{1}{4}$.")
with col8:
    ans_d9 = st.radio("q9d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q9_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q9_check"):
    if None in [ans_a9, ans_b9, ans_c9, ans_d9]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Đúng, b-Sai, c-Sai, d-Đúng
        correct_answers = {"a": "Đ", "b": "S", "c": "S", "d": "Đ"}
        user_answers = {"a": ans_a9, "b": ans_b9, "c": ans_c9, "d": ans_d9}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q9_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"**a) Mệnh đề Đúng:**")
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{-4\}$.")
        st.markdown(r"Tính đạo hàm: $f'(x) = \dfrac{3 \cdot 4 - 1 \cdot 1}{(x + 4)^2} = \dfrac{11}{(x + 4)^2}$.")
        
        st.markdown(r"**b) Mệnh đề Sai:**")
        st.markdown(r"Ta có $f'(x) > 0, \forall x \neq -4$, nên hàm số đồng biến trên các khoảng $(-\infty; -4)$ và $(-4; +\infty)$. Tuy nhiên, nó không đồng biến trên $\mathbb{R} \setminus \{-4\}$.")
        st.markdown(r"Giới hạn tại tiệm cận: $\lim\limits_{x \to -4^-} f(x) = +\infty$ và $\lim\limits_{x \to -4^+} f(x) = -\infty$.")
        st.markdown(r"Vì vậy, khi $x_1 < -4 < x_2$, ta có thể thấy $f(x_1)$ mang giá trị rất lớn (dương) và $f(x_2)$ mang giá trị rất bé (âm).")
        st.markdown(r"Ví dụ: Chọn $x_1 = -5 \Rightarrow f(-5) = \dfrac{3(-5) + 1}{-5 + 4} = 14$. Chọn $x_2 = 0 \Rightarrow f(0) = \dfrac{1}{4}$. Rõ ràng $f(-5) > f(0)$.")
        
        st.markdown(r"**c) Mệnh đề Sai:**")
        st.markdown(r"Đồ thị hàm số có đường tiệm cận đứng là $x = -4$ (nghiệm của mẫu).")
        st.markdown(r"Đường tiệm cận ngang là $y = \dfrac{3}{1} = 3$ (tỉ số các hệ số của $x$).")
        st.markdown(r"Tọa độ giao điểm của hai đường tiệm cận là $I(-4; 3)$, không phải $(3; -4)$.")
        
        st.markdown(r"**d) Mệnh đề Đúng:**")
        st.markdown(r"Hàm số xác định và liên tục trên đoạn $[0; 1]$.")
        st.markdown(r"Vì $f'(x) > 0$ với mọi $x \in [0; 1]$ nên hàm số đồng biến trên đoạn này.")
        st.markdown(r"Do đó, giá trị nhỏ nhất của hàm số đạt được tại đầu mút bên trái: $\min\limits_{[0; 1]} f(x) = f(0) = \dfrac{3(0) + 1}{0 + 4} = \dfrac{1}{4}$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU HỎI 10 (ĐÚNG/SAI)
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
        <span style="color: #008080; font-weight: bold;">Câu 10. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Thị Minh Khai - Hà Nội 2026) </span>
        Cho hàm số $y = \dfrac{2x - 1}{x + 1}$ có đồ thị $(C)$.
    </span>
    """, 
    unsafe_allow_html=True
)



st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Hàm số đồng biến trên tập xác định.")
with col2:
    ans_a10 = st.radio("q10a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q10_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Đồ thị hàm số $(C)$ có tâm đối xứng là điểm $I(-1; 2)$.")
with col4:
    ans_b10 = st.radio("q10b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q10_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Tiếp tuyến của đồ thị hàm số $(C)$ tại giao điểm của đồ thị hàm số $(C)$ với trục tung có phương trình là $y = 3x - 1$.")
with col6:
    ans_c10 = st.radio("q10c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q10_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Số điểm thuộc đồ thị hàm số có tọa độ nguyên là $2$.")
with col8:
    ans_d10 = st.radio("q10d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q10_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q10_check"):
    if None in [ans_a10, ans_b10, ans_c10, ans_d10]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Sai, b-Đúng, c-Đúng, d-Sai
        correct_answers = {"a": "S", "b": "Đ", "c": "Đ", "d": "S"}
        user_answers = {"a": ans_a10, "b": ans_b10, "c": ans_c10, "d": ans_d10}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q10_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True):
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{-1\}$.")
        st.markdown(r"Đạo hàm: $y' = \dfrac{2 \cdot 1 - (-1) \cdot 1}{(x + 1)^2} = \dfrac{3}{(x + 1)^2}$.")
        
        st.markdown(r"**a) Mệnh đề Sai:**")
        st.markdown(r"Ta có $y' = \dfrac{3}{(x + 1)^2} > 0, \forall x \neq -1$.")
        st.markdown(r"Do đó hàm số đồng biến trên các khoảng $(-\infty; -1)$ và $(-1; +\infty)$.")
        st.markdown(r"Cách diễn đạt \"đồng biến trên tập xác định\" (tức là trên $D = \mathbb{R} \setminus \{-1\}$) là sai về mặt khái niệm (hàm số không liên tục trên toàn bộ $D$).")
        
        st.markdown(r"**b) Mệnh đề Đúng:**")
        st.markdown(r"Đường tiệm cận đứng là $x = -1$ và đường tiệm cận ngang là $y = 2$.")
        st.markdown(r"Giao điểm của hai đường tiệm cận là $I(-1; 2)$.")
        st.markdown(r"Đối với hàm phân thức bậc nhất trên bậc nhất $y = \dfrac{ax+b}{cx+d}$, giao điểm của hai tiệm cận chính là tâm đối xứng của đồ thị hàm số.")
        
        st.markdown(r"**c) Mệnh đề Đúng:**")
        st.markdown(r"Giao điểm của đồ thị hàm số với trục tung là điểm có hoành độ $x_0 = 0$.")
        st.markdown(r"Tung độ tiếp điểm là $y_0 = \dfrac{2(0) - 1}{0 + 1} = -1$.")
        st.markdown(r"Hệ số góc của tiếp tuyến là $k = y'(0) = \dfrac{3}{(0 + 1)^2} = 3$.")
        st.markdown(r"Phương trình tiếp tuyến: $y = k(x - x_0) + y_0 \Leftrightarrow y = 3(x - 0) - 1 \Leftrightarrow y = 3x - 1$.")
        
        st.markdown(r"**d) Mệnh đề Sai:**")
        st.markdown(r"Ta có $y = \dfrac{2x - 1}{x + 1} = \dfrac{2(x + 1) - 3}{x + 1} = 2 - \dfrac{3}{x + 1}$.")
        st.markdown(r"Để điểm thuộc đồ thị có tọa độ nguyên thì $x$ và $y$ đều phải là số nguyên.")
        st.markdown(r"Suy ra $\dfrac{3}{x + 1}$ phải là số nguyên, tức là $x + 1$ là ước của $3$.")
        st.markdown(r"Các ước của $3$ là: $\pm 1, \pm 3$.")
        st.markdown(r"Ta có các trường hợp:")
        st.markdown(r"- $x + 1 = 1 \Rightarrow x = 0 \Rightarrow y = -1$ (nhận)")
        st.markdown(r"- $x + 1 = -1 \Rightarrow x = -2 \Rightarrow y = 5$ (nhận)")
        st.markdown(r"- $x + 1 = 3 \Rightarrow x = 2 \Rightarrow y = 1$ (nhận)")
        st.markdown(r"- $x + 1 = -3 \Rightarrow x = -4 \Rightarrow y = 3$ (nhận)")
        st.markdown(r"Vậy có tất cả $4$ điểm thuộc đồ thị có tọa độ nguyên. Số điểm là $4$, không phải $2$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")
