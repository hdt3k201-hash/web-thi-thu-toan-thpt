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
