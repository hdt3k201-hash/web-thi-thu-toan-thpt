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
    '<b style="color: blue;">Câu 3. [Trả lời ngắn ]</b>',
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



# ==================== CÂU 4 ====================
st.markdown(
    '<b style="color: blue;">Câu 4. [Trả lời ngắn ]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một trường THPT tổ chức cho học sinh đi trải nghiệm thực tế. Nếu xếp mỗi xe $36$ học sinh, $40$ học sinh hay $45$ học sinh thì đều thừa ra $3$ học sinh. Tuy nhiên, nếu xếp mỗi xe đúng $19$ học sinh thì vừa đủ chỗ không thừa em nào. Biết số lượng học sinh của trường nằm trong khoảng từ $1000$ đến $2000$ em. Tính tổng số học sinh của trường đó.
""")

user_answer_4 = st.text_input("Nhập tổng số học sinh:", key="q4_ans")

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/cau4.PNG", width=400)
except FileNotFoundError:
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/cau4.PNG'. Vui lòng kiểm tra lại đường dẫn.")

if st.button("Kiểm tra đáp án", key="q4_check"):
    normalized_ans_4 = user_answer_4.strip().replace(',', '.')
    if normalized_ans_4 == "1083":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_4 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy tìm BCNN của $36, 40, 45$ và kết hợp điều kiện chia hết cho $19$ trong khoảng cho trước nhé!")

st.markdown("---")

if 'q4_solution_shown' not in st.session_state:
    st.session_state['q4_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q4_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q4_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q4_solution_shown'] = False 

if st.session_state.get('q4_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    st.markdown(r"""
    **Bước 1: Thiết lập biểu thức toán học**
    
    Gọi số học sinh của trường là $x$ (học sinh), điều kiện: $1000 \le x \le 2000$ và $x \in \mathbb{N}^*$.
    
    Theo đề bài, khi xếp mỗi xe $36, 40$ hay $45$ học sinh đều thừa $3$ học sinh, nên $(x - 3)$ chia hết cho cả $36, 40$ và $45$.
    
    Do đó, $(x - 3) \in \text{BC}(36, 40, 45)$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất ($\text{BCNN}$)**
    
    Ta phân tích các số ra thừa số nguyên tố:
    *   $36 = 2^2 \cdot 3^2$
    *   $40 = 2^3 \cdot 5$
    *   $45 = 3^2 \cdot 5$
    
    $\text{BCNN}(36, 40, 45) = 2^3 \cdot 3^2 \cdot 5 = 8 \cdot 9 \cdot 5 = 360$.
    
    Suy ra: $(x - 3)$ là bội của $360$, hay $x - 3 = 360k$ với $k \in \mathbb{N}$.
    
    $\Rightarrow x = 360k + 3$.
    
    **Bước 3: Kết hợp điều kiện khoảng giá trị và tính chia hết**
    
    Vì số học sinh nằm trong khoảng từ $1000$ đến $2000$:
    $$1000 \le 360k + 3 \le 2000$$
    $$\Leftrightarrow 997 \le 360k \le 1997 \Rightarrow 2,77 \le k \le 5,54$$
    Vì $k \in \mathbb{N}$ nên $k \in \{3, 4, 5\}$.
    
    Mặt khác, khi xếp mỗi xe đúng $19$ học sinh thì vừa đủ, nên $x$ phải chia hết cho $19$:
    *   Với $k = 3 \Rightarrow x = 360 \cdot 3 + 3 = 1083$. Ta thấy $1083 \div 19 = 57$ (thỏa mãn).
    *   Với $k = 4 \Rightarrow x = 360 \cdot 4 + 3 = 1443$ (không chia hết cho $19$).
    *   Với $k = 5 \Rightarrow x = 360 \cdot 5 + 3 = 1803$ (không chia hết cho $19$).
    
    **Kết luận:** Tổng số học sinh của trường là **$1083$**.
    """)

st.markdown("---")

# ==================== CÂU 5 ====================
st.markdown(
    '<b style="color: blue;">Câu 5. [Trả lời ngắn ]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Hệ thống mã khóa két sắt của một ngân hàng sử dụng một mật khẩu là số tự nhiên có $4$ chữ số. Chuyên gia bảo mật phát hiện ra rằng mật khẩu này là một số cực kỳ đặc biệt: nó có giá trị đúng bằng bình phương của số tạo bởi hai chữ số cuối cùng của chính nó. Hãy tìm mật khẩu của két sắt đó.
""")

user_answer_5 = st.text_input("Nhập mật khẩu két sắt:", key="q5_ans")

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/cau5.PNG", width=400)
except FileNotFoundError:
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/cau5.PNG'. Vui lòng kiểm tra lại đường dẫn.")

if st.button("Kiểm tra đáp án", key="q5_check"):
    normalized_ans_5 = user_answer_5.strip().replace(',', '.')
    if normalized_ans_5 == "5776":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_5 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy thiết lập phương trình đại số dựa trên hai chữ số cuối cùng và điều kiện đồng dư nhé!")

st.markdown("---")

if 'q5_solution_shown' not in st.session_state:
    st.session_state['q5_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q5_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q5_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q5_solution_shown'] = False 

if st.session_state.get('q5_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    st.markdown(r"""
    **Bước 1: Đặt ẩn và thiết lập phương trình**
    
    Gọi số cần tìm là $\overline{abcd}$ với $a \in \{1, 2, \dots, 9\}$ và $b, c, d \in \{0, 1, \dots, 9\}$.
    Số tạo bởi hai chữ số cuối cùng là $\overline{cd}$.
    
    Theo đề bài, mật khẩu có giá trị bằng bình phương của hai chữ số cuối:
    $$\overline{abcd} = \overline{cd}^{\,2}$$
    
    Vì $\overline{abcd} = 100 \cdot \overline{ab} + \overline{cd}$, ta suy ra:
    $$100 \cdot \overline{ab} + \overline{cd} = \overline{cd}^{\,2}$$
    $$\Leftrightarrow 100 \cdot \overline{ab} = \overline{cd}(\overline{cd} - 1)$$
    
    **Bước 2: Phân tích điều kiện và đồng dư thức**
    
    Phương trình trên cho thấy tích $\overline{cd}(\overline{cd} - 1)$ phải chia hết cho $100$.
    Vì số có $4$ chữ số có bình phương nằm trong đoạn từ $1000$ đến $9999$, ta có:
    $$\sqrt{1000} \le \overline{cd} \le \sqrt{9999} \Rightarrow 32 \le \overline{cd} \le 99$$
    
    Ta có điều kiện đồng dư:
    $$\overline{cd}^{\,2} \equiv \overline{cd} \pmod{100} \Leftrightarrow \overline{cd}(\overline{cd} - 1) \equiv 0 \pmod{100}$$
    
    Các nghiệm của phương trình đồng dư với số có hai chữ số là $\overline{cd} \in \{00, 01, 25, 76\}$. 
    Kết hợp với điều kiện $32 \le \overline{cd} \le 99$, ta chọn được duy nhất:
    $$\overline{cd} = 76$$
    
    **Bước 3: Tính toán giá trị mật khẩu**
    
    Thay $\overline{cd} = 76$ vào bình phương:
    $$\overline{cd}^{\,2} = 76^2 = 5776$$
    
    Số $5776$ thỏa mãn đúng yêu cầu: là số có $4$ chữ số và có hai chữ số tận cùng là $76$, bình phương lên chính bằng nó ($76^2 = 5776$).
    
    **Kết luận:** Mật khẩu của két sắt là **$5776$**.
    """)

st.markdown("---")

# ==================== CÂU 6 ====================
st.markdown(
    '<b style="color: blue;">Câu 6. [Trả lời ngắn ]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Trong dự án "Ánh sáng học đường", Đoàn thanh niên cần mua hai loại bóng đèn LED: loại $9\text{W}$ giá $45.000$ đồng/chiếc và loại $18\text{W}$ giá $70.000$ đồng/chiếc. Tổng số tiền thanh toán trên hóa đơn đúng bằng $500.000$ đồng. Biết rằng Đoàn trường đã mua số lượng bóng đèn loại $9\text{W}$ nhiều hơn số bóng đèn loại $18\text{W}$. Hỏi Đoàn trường đã mua tổng cộng bao nhiêu bóng đèn?
""")

user_answer_6 = st.text_input("Nhập tổng số bóng đèn:", key="q6_ans")

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/cau6.PNG", width=400)
except FileNotFoundError:
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/cau6.PNG'. Vui lòng kiểm tra lại đường dẫn.")

if st.button("Kiểm tra đáp án", key="q6_check"):
    normalized_ans_6 = user_answer_6.strip().replace(',', '.')
    if normalized_ans_6 == "10":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_6 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy thiết lập phương trình nghiệm nguyên tuyến tính và đối chiếu điều kiện số lượng nhé!")

st.markdown("---")

if 'q6_solution_shown' not in st.session_state:
    st.session_state['q6_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q6_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q6_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q6_solution_shown'] = False 

if st.session_state.get('q6_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    st.markdown(r"""
    **Bước 1: Lập phương trình nghiệm nguyên**
    
    Gọi $x$ là số lượng bóng đèn loại $9\text{W}$ và $y$ là số lượng bóng đèn loại $18\text{W}$ mà Đoàn trường đã mua.
    Điều kiện: $x, y \in \mathbb{N}^*$ và $x > y$.
    
    Tổng số tiền thanh toán là $500.000$ đồng, ta có phương trình:
    $$45.000x + 70.000y = 500.000$$
    $$\Leftrightarrow 45x + 70y = 500$$
    $$\Leftrightarrow 9x + 14y = 100 \quad (1)$$
    
    **Bước 2: Giải phương trình Diophantine**
    
    Từ phương trình $(1)$, ta biểu diễn ẩn $x$ theo $y$:
    $$9x = 100 - 14y \Rightarrow x = \dfrac{100 - 14y}{9} = 11 - y + \dfrac{1 - 5y}{9}$$
    
    Để $x \in \mathbb{Z}$, biểu thức $\dfrac{1 - 5y}{9}$ phải là một số nguyên, đặt $\dfrac{1 - 5y}{9} = k$ ($k \in \mathbb{Z}$).
    $$\Rightarrow 1 - 5y = 9k \Leftrightarrow 5y = 1 - 9k \Leftrightarrow y = \dfrac{1 - 9k}{5} = -2k + \dfrac{1 + k}{5}$$
    
    Đặt $\dfrac{1 + k}{5} = m$ ($m \in \mathbb{Z}$) $\Rightarrow k = 5m - 1$.
    Thay ngược lại để tính $y$ theo $m$:
    $$y = -2(5m - 1) + m = -10m + 2 + m = 2 - 9m$$
    
    Thay giá trị của $y$ vào biểu thức tính $x$:
    $$x = \dfrac{100 - 14(2 - 9m)}{9} = \dfrac{72 + 126m}{9} = 8 + 14m$$
    
    **Bước 3: Kiểm tra điều kiện nghiệm nguyên dương**
    
    Vì $x, y \in \mathbb{N}^*$ và $x > y$:
    *   $x > 0 \Rightarrow 8 + 14m > 0 \Rightarrow m \ge 0$
    *   $y > 0 \Rightarrow 2 - 9m > 0 \Rightarrow m < \dfrac{2}{9}$
    
    Vì $m$ là số nguyên nên ta chọn được duy nhất $m = 0$.
    
    Với $m = 0$, ta tính được:
    *   $x = 8 + 14(0) = 8$ (số bóng đèn loại $9\text{W}$)
    *   $y = 2 - 9(0) = 2$ (số bóng đèn loại $18\text{W}$)
    
    Kiểm tra điều kiện $x > y$, tức $8 > 2$ (thỏa mãn đề bài).
    
    **Bước 4: Tính tổng số bóng đèn**
    
    Tổng số bóng đèn Đoàn trường đã mua là:
    $$x + y = 8 + 2 = 10 \text{ (bóng đèn)}$$
    
    **Kết luận:** Đoàn trường đã mua tổng cộng **$10$** bóng đèn.
    """)

st.markdown("---")
