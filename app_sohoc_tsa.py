import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="Ngân hàng câu hỏi", layout="centered")

# 1. Đọc thông số từ URL (do WordPress truyền sang)
params = st.query_params

# Nếu trên URL có chứa tham số 'auth_status=success', tự động cho phép xem lời giải
if params.get("auth_status") == "success":
    st.session_state['logged_in'] = True
    st.sidebar.success("✅ Đã đồng bộ tài khoản từ Website!")
else:
    # Nếu không có tham số từ web, hiển thị form đăng nhập dự phòng như cũ
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

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



# 2. Giao diện chính hiển thị câu hỏi
# Tiêu đề chuyên đề căn giữa màn hình, màu xanh đậm (Dark Blue)
st.markdown(
    '<h2 style="text-align: center; color: red;">CHUYÊN ĐỀ: SỐ HỌC TSA</h2>',
    unsafe_allow_html=True
)
st.markdown("---")


import streamlit as st

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 1. [Trả lời ngắn ]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Cho số tự nhiên $N = 202600$. Có bao nhiêu ước số nguyên dương của $N$ chia hết cho $10$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập số lượng ước số:", key="q1_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q1_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng thừa)
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 12
    if normalized_user_answer == "12":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy cẩn thận phân tích số $N$ ra thừa số nguyên tố và nhớ áp dụng quy tắc nhân nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q1_solution_shown' not in st.session_state:
    st.session_state['q1_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q1_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q1_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q1_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q1_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Hướng dẫn chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích số $N$ ra thừa số nguyên tố:**
    
    Ta có:
    $$N = 202600 = 2026 \times 100$$
    $$N = (2 \times 1013) \times (2^2 \times 5^2)$$
    $$N = 2^3 \times 5^2 \times 1013^1$$
    
    **Bước 2: Tìm điều kiện của các ước số chia hết cho $10$:**
    
    Để một ước số $d$ của $N$ chia hết cho $10$ (tức là chia hết cho $2 \times 5$), thì $d$ phải có dạng $d = 2^x \times 5^y \times 1013^z$ trong đó:
    
    *   Số mũ $x \in \{1, 2, 3\}$ (có $3$ cách chọn, do $d$ phải chứa ít nhất thừa số $2^1$).
    *   Số mũ $y \in \{1, 2\}$ (có $2$ cách chọn, do $d$ phải chứa ít nhất thừa số $5^1$).
    *   Số mũ $z \in \{0, 1\}$ (có $2$ cách chọn).
    
    **Bước 3: Tính toán kết quả**
    
    Áp dụng quy tắc nhân, số lượng ước số thỏa mãn yêu cầu bài toán là:
    $$3 \times 2 \times 2 = 12 \text{ (ước số)}$$
    
    **Đáp số:** $12$
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 2. [Trả lời ngắn ]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh
st.markdown(r"""
Tìm số dư khi chia biểu thức $P = 2025^{2026} + 2026^{2025}$ cho $7$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập số dư:", key="q2_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q2_check"):
    # Chuẩn hóa đầu vào 
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 1
    if normalized_user_answer == "1":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy sử dụng tính chất của đồng dư thức để tìm số dư của từng số hạng nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q2_solution_shown' not in st.session_state:
    st.session_state['q2_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q2_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q2_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q2_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q2_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm số dư của $2025^{2026}$ khi chia cho $7$**
    
    Ta có: $2025 = 7 \cdot 289 + 2$, do đó $2025 \equiv 2 \pmod 7$.
    Suy ra: $2025^{2026} \equiv 2^{2026} \pmod 7$.
    
    Ta lại có: $2^3 = 8 \equiv 1 \pmod 7$.
    Mặt khác, $2026 = 3 \cdot 675 + 1$.
    Do đó: $2^{2026} = 2^{3 \cdot 675 + 1} = (2^3)^{675} \cdot 2 \equiv 1^{675} \cdot 2 \equiv 2 \pmod 7$.
    
    Vậy $2025^{2026}$ chia $7$ dư $2$.
    
    **Bước 2: Tìm số dư của $2026^{2025}$ khi chia cho $7$**
    
    Ta có: $2026 = 7 \cdot 289 + 3$, do đó $2026 \equiv 3 \pmod 7$.
    Suy ra: $2026^{2025} \equiv 3^{2025} \pmod 7$.
    
    Ta lại có: $3^6 = 729 = 7 \cdot 104 + 1 \equiv 1 \pmod 7$.
    Mặt khác, $2025 = 6 \cdot 337 + 3$.
    Do đó: $3^{2025} = 3^{6 \cdot 337 + 3} = (3^6)^{337} \cdot 3^3 \equiv 1^{337} \cdot 27 \pmod 7$.
    Vì $27 = 7 \cdot 3 + 6 \equiv 6 \pmod 7$, nên $3^{2025} \equiv 6 \pmod 7$.
    
    Vậy $2026^{2025}$ chia $7$ dư $6$.
    
    **Bước 3: Tìm số dư của tổng $P$**
    
    Ta có $P = 2025^{2026} + 2026^{2025}$.
    Theo các kết quả trên, $P \equiv 2 + 6 = 8 \pmod 7$.
    Vì $8 \equiv 1 \pmod 7$, nên $P \equiv 1 \pmod 7$.
    
    **Kết luận:** Số dư khi chia biểu thức $P = 2025^{2026} + 2026^{2025}$ cho $7$ là **$1$**.
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 3. [Trả lời ngắn - Vận dụng Mô hình hóa (Diophantine)]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh
st.markdown(r"""
Một đoàn khách du lịch gồm người lớn và trẻ em mua vé tham quan một khu di tích. Giá vé người lớn là $50$ nghìn đồng/vé, giá vé trẻ em là $30$ nghìn đồng/vé. Tổng số tiền đoàn phải trả là $470$ nghìn đồng. Biết rằng số lượng người lớn trong đoàn nhiều hơn số lượng trẻ em. Hỏi đoàn khách du lịch đó có tổng cộng bao nhiêu người?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập tổng số người trong đoàn:", key="q3_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q3_check"):
    # Chuẩn hóa đầu vào 
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 11
    if normalized_user_answer == "11":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy lập phương trình số tiền và kết hợp với điều kiện số lượng người lớn nhiều hơn trẻ em để thử chọn các giá trị nguyên nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q3_solution_shown' not in st.session_state:
    st.session_state['q3_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q3_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q3_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q3_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q3_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Lập phương trình**
    
    Gọi $x$ là số lượng người lớn và $y$ là số lượng trẻ em trong đoàn khách.
    Điều kiện: $x, y \in \mathbb{N}^*$ và $x > y$ (số người lớn nhiều hơn trẻ em).
    
    Tổng số tiền vé đoàn phải trả là $470$ nghìn đồng, ta có phương trình:
    $$50x + 30y = 470$$
    $$\Leftrightarrow 5x + 3y = 47 \quad (1)$$
    
    **Bước 2: Giải phương trình nghiệm nguyên (Diophantine)**
    
    Từ phương trình $(1)$, ta suy ra:
    $$3y = 47 - 5x$$
    $$\Rightarrow y = \dfrac{47 - 5x}{3} = 15 - x + \dfrac{2 - 2x}{3}$$
    
    Để $y \in \mathbb{N}^*$ thì $(47 - 5x)$ phải chia hết cho $3$ và $47 - 5x > 0 \Rightarrow x < \dfrac{47}{5} = 9,4$.
    Vì $x \in \mathbb{N}^*$ nên $x \in \{1, 2, 3, 4, 5, 6, 7, 8, 9\}$.
    
    Ta thử lần lượt các giá trị của $x$ để tìm $y$ tương ứng:
    
    *   Nếu $x = 1 \Rightarrow y = \dfrac{42}{3} = 14$ (Loại vì $x < y$)
    *   Nếu $x = 2 \Rightarrow y = \dfrac{37}{3}$ (Loại vì không nguyên)
    *   Nếu $x = 3 \Rightarrow y = \dfrac{32}{3}$ (Loại)
    *   Nếu $x = 4 \Rightarrow y = \dfrac{27}{3} = 9$ (Loại vì $x < y$)
    *   Nếu $x = 5 \Rightarrow y = \dfrac{22}{3}$ (Loại)
    *   Nếu $x = 6 \Rightarrow y = \dfrac{17}{3}$ (Loại)
    *   Nếu $x = 7 \Rightarrow y = \dfrac{12}{3} = 4$ (Nhận vì $x > y$, tức là $7 > 4$)
    *   Nếu $x = 8 \Rightarrow y = \dfrac{7}{3}$ (Loại)
    *   Nếu $x = 9 \Rightarrow y = \dfrac{2}{3}$ (Loại)
    
    Vậy đoàn khách có $7$ người lớn và $4$ trẻ em.
    
    **Bước 3: Tính tổng số người**
    
    Tổng số người trong đoàn khách du lịch là:
    $$x + y = 7 + 4 = 11 \text{ (người)}$$
    
    **Kết luận:** Đoàn khách du lịch đó có tổng cộng **$11$** người.
    """)
    
st.markdown("---")
