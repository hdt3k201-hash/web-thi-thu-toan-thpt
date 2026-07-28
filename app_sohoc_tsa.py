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



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 7. [TSA ]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Cho số tự nhiên $M = 20^{26}$. Gọi $S$ là tập hợp tất cả các ước số nguyên dương của $M$. Chọn ngẫu nhiên một số từ tập $S$, xác suất để số được chọn là một **số chính phương** có dạng phân số tối giản là $\dfrac{a}{b}$ (với $a, b \in \mathbb{N}^*$). 

Hãy tính giá trị của $a + b$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (giá trị a + b):", key="q7_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q7_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng thừa)
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 67 (a = 14, b = 53)
    if normalized_user_answer == "67":
        st.success("🎉 Chính xác! Bạn có tư duy số học và tổ hợp rất xuất sắc. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("⚠️ Bạn chưa nhập đáp án.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Để một ước số là số chính phương thì số mũ của các thừa số nguyên tố trong phân tích chuẩn tắc phải là số chẵn nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q7_solution_shown' not in st.session_state:
    st.session_state['q7_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q7_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q7_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q7_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q7_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết (Tư duy TSA):")
    
    st.markdown(r"""
    Bài toán yêu cầu kết hợp tư duy **Số học (Lý thuyết chia hết & Số chính phương)** và **Tổ hợp (Xác suất cổ điển)**.
    
    **Bước 1: Tìm không gian mẫu (Tổng số ước số nguyên dương của $M$)**
    
    Phân tích $M$ ra thừa số nguyên tố:
    $$M = 20^{26} = (2^2 \times 5)^{26} = 2^{52} \times 5^{26}$$
    
    Một ước số nguyên dương bất kỳ $d$ của $M$ đều có dạng $d = 2^x \times 5^y$, trong đó:
    *   Số mũ $x \in \{0, 1, 2, \dots, 52\}$ $\rightarrow$ có $52 - 0 + 1 = 53$ cách chọn.
    *   Số mũ $y \in \{0, 1, 2, \dots, 26\}$ $\rightarrow$ có $26 - 0 + 1 = 27$ cách chọn.
    
    Số phần tử của không gian mẫu (tổng số ước nguyên dương của $M$) là:
    $$n(\Omega) = 53 \times 27 = 1431$$
    
    **Bước 2: Tìm số kết quả thuận lợi (Ước số là số chính phương)**
    
    Để ước số $d = 2^x \times 5^y$ là một **số chính phương** thì các số mũ $x$ và $y$ đồng thời phải là **các số chẵn**.
    
    *   Số mũ $x \in \{0, 2, 4, \dots, 52\}$ $\rightarrow$ có $\frac{52 - 0}{2} + 1 = 27$ cách chọn.
    *   Số mũ $y \in \{0, 2, 4, \dots, 26\}$ $\rightarrow$ có $\frac{26 - 0}{2} + 1 = 14$ cách chọn.
    
    Áp dụng quy tắc nhân, số lượng ước số là số chính phương của $M$ là:
    $$n(A) = 27 \times 14 = 378$$
    
    **Bước 3: Tính xác suất và kết luận**
    
    Xác suất để chọn được ước số là số chính phương là:
    $$P(A) = \frac{n(A)}{n(\Omega)} = \frac{378}{1431}$$
    
    Rút gọn phân số (chia cả tử và mẫu cho $27$):
    $$P(A) = \frac{14}{53}$$
    
    Vì $\frac{14}{53}$ là phân số tối giản nên ta có $a = 14$ và $b = 53$.
    
    Giá trị cần tìm là:
    $$a + b = 14 + 53 = 67$$
    
    ---
    **👉 Đáp số:** `67`
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 8. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Có bao nhiêu số tự nhiên $n$ có $3$ chữ số ($100 \le n \le 999$) sao cho biểu thức:
$$A = n^3 - n$$
chia hết cho $24$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập số lượng số tự nhiên n thỏa mãn:", key="q8_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q8_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng thừa)
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 562
    if normalized_user_answer == "562":
        st.success("🎉 Chính xác! Bạn đã phân tích tính chất chia hết và đếm tập hợp rất xuất sắc. Lời giải đã được mở khóa.")
    elif user_answer == "":
        st.warning("⚠️ Bạn chưa nhập đáp án.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy phân tích $A = n(n-1)(n+1)$ và xét riêng 2 trường hợp $n$ là số lẻ và $n$ là số chẵn nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q8_solution_shown' not in st.session_state:
    st.session_state['q8_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q8_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q8_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q8_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q8_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết (Tư duy TSA):")
    
    st.markdown(r"""
    **Bước 1: Phân tích biểu thức và yêu cầu bài toán**
    
    Ta có: $A = n^3 - n = (n - 1)n(n + 1)$. Đây là tích của $3$ số nguyên liên tiếp.
    
    Trong $3$ số nguyên liên tiếp luôn có ít nhất một số chia hết cho $2$ và một số chia hết cho $3$. Do $\gcd(2, 3) = 1$ nên $A$ luôn chia hết cho $6$ với mọi $n \in \mathbb{N}$.
    
    Để $A \text{ } \vdots \text{ } 24$ (mà $24 = 3 \times 8$ và $\gcd(3, 8) = 1$), ta chỉ cần tìm điều kiện để $A \text{ } \vdots \text{ } 8$.
    
    **Bước 2: Xét tính chẵn lẻ của $n$**
    
    *   **Trường hợp 1: $n$ là số lẻ ($n = 2k + 1$)**
        Khi đó, $n - 1 = 2k$ và $n + 1 = 2k + 2$ là **hai số chẵn liên tiếp**.
        Tích của hai số chẵn liên tiếp luôn chia hết cho $8$. Do đó, $(n - 1)(n + 1) \text{ } \vdots \text{ } 8 \implies A \text{ } \vdots \text{ } 8$.
        $\rightarrow$ **Mọi số lẻ $n$ đều thỏa mãn bài toán.**
        
    *   **Trường hợp 2: $n$ là số chẵn ($n = 2k$)**
        Khi đó, $n - 1$ và $n + 1$ là hai số lẻ nên không chứa thừa số $2$ nào.
        Để $A = n(n-1)(n+1) \text{ } \vdots \text{ } 8$ thì bắt buộc bản thân số $n$ phải chia hết cho $8$.
        $\rightarrow$ **Các số chẵn $n$ thỏa mãn khi và chỉ khi $n$ là bội của $8$.**
        
    **Bước 3: Đếm số lượng số $n$ có $3$ chữ số ($100 \le n \le 999$)**
    
    Tổng số các số tự nhiên có $3$ chữ số là: $999 - 100 + 1 = 900$ số.
    
    1.  **Số lượng số lẻ:**
        Từ $101$ đến $999$ có: $\frac{999 - 101}{2} + 1 = 450$ số.
        
    2.  **Số lượng số chia hết cho $8$ (đều là số chẵn):**
        Số nhỏ nhất có $3$ chữ số chia hết cho $8$ là $104$ ($8 \times 13$).
        Số lớn nhất có $3$ chữ số chia hết cho $8$ là $992$ ($8 \times 124$).
        Số lượng số là: $124 - 13 + 1 = 112$ số.
        
    Vì tập hợp các số lẻ và tập hợp các số chia hết cho $8$ là rời nhau (không trùng lặp), tổng số giá trị $n$ thỏa mãn là:
    $$450 + 112 = 562 \text{ (số)}$$
    
    ---
    **👉 Đáp số:** `562`
    """)
    
st.markdown("---")





# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 9. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Cho biểu thức đại số:
$$P(n) = n^4 + 2n^3 + 2n^2 + 11n - 13$$
Gọi $S$ là tập hợp tất cả các số nguyên dương $n$ để $P(n)$ là một **số chính phương**. 

Hãy tính **tổng** các phần tử của tập hợp $S$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập tổng các giá trị n thỏa mãn:", key="q9_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q9_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng thừa)
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 9 (S = {2, 7} => 2 + 7 = 9)
    if normalized_user_answer == "9":
        st.success("🎉 Chính xác! Bạn đã sử dụng phương pháp 'Kẹp giữa hai số chính phương' cực kỳ bậc thầy. Lời giải đã được mở khóa.")
    elif user_answer == "":
        st.warning("⚠️ Bạn chưa nhập đáp án.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy chứng minh với $n \ge 2$, biểu thức $P(n)$ luôn bị kẹp giữa $(n^2+n)^2$ và $(n^2+n+2)^2$.")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q9_solution_shown' not in st.session_state:
    st.session_state['q9_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q9_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q9_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q9_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q9_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết (Tư duy TSA):")
    
    st.markdown(r"""
    Để giải bài toán số chính phương với đa thức bậc 4, phương pháp hiệu quả nhất là **Phương pháp kẹp (Sandwich Method)** giữa hai số chính phương liên tiếp.
    
    **Bước 1: So sánh $P(n)$ với các bình phương lân cận**
    
    Ta xét bình phương của biểu thức $(n^2 + n)$:
    $$(n^2 + n)^2 = n^4 + 2n^3 + n^2$$
    Xét hiệu: $P(n) - (n^2 + n)^2 = n^2 + 11n - 13$.
    Với mọi số nguyên dương $n \ge 2$, ta dễ dàng thấy $n^2 + 11n - 13 > 0$. 
    $\implies P(n) > (n^2 + n)^2 \text{ với mọi } n \ge 2 \quad (1)$
    
    Tiếp tục xét bình phương của biểu thức $(n^2 + n + 2)$:
    $$(n^2 + n + 2)^2 = n^4 + 2n^3 + 5n^2 + 4n + 4$$
    Xét hiệu: $(n^2 + n + 2)^2 - P(n) = 3n^2 - 7n + 17$.
    Do tam thức bậc hai $3n^2 - 7n + 17$ có $\Delta = (-7)^2 - 4 \times 3 \times 17 = -155 < 0$, nên $3n^2 - 7n + 17 > 0$ với mọi $n \in \mathbb{R}$.
    $\implies P(n) < (n^2 + n + 2)^2 \text{ với mọi } n \in \mathbb{N}^* \quad (2)$
    
    **Bước 2: Sử dụng nguyên lý kẹp**
    
    từ $(1)$ và $(2)$, với mọi $n \ge 2$, ta có bất đẳng thức:
    $$(n^2 + n)^2 < P(n) < (n^2 + n + 2)^2$$
    
    Vì $P(n)$ là một số chính phương và nằm nghiêm ngặt giữa hai số chính phương cách nhau $2$ đơn vị, nên **$P(n)$ buộc phải bằng số chính phương ở chính giữa**, tức là:
    $$P(n) = (n^2 + n + 1)^2$$
    
    **Bước 3: Giải phương trình tìm $n$**
    
    Ta có phương trình:
    $$n^4 + 2n^3 + 2n^2 + 11n - 13 = (n^2 + n + 1)^2$$
    $$\iff n^4 + 2n^3 + 2n^2 + 11n - 13 = n^4 + 2n^3 + 3n^2 + 2n + 1$$
    $$\iff n^2 - 9n + 14 = 0$$
    $$\iff (n - 2)(n - 7) = 0 \implies \left[ \begin{array}{l} n = 2 \\ n = 7 \end{array} \right.$$
    
    Cả hai giá trị $n=2$ và $n=7$ đều thỏa mãn điều kiện $n \ge 2$ và là số nguyên dương:
    *   Với $n = 2 \implies P(2) = 49 = 7^2$ (thỏa mãn).
    *   Với $n = 7 \implies P(7) = 3249 = 57^2$ (thỏa mãn).
    
    *(Lưu ý: Kiểm tra riêng với $n=1$ ta có $P(1) = 3$ không phải số chính phương).*
    
    **Bước 4: Kết luận**
    
    Tập hợp các giá trị thỏa mãn là $S = \{2; 7\}$.
    Tổng các phần tử của $S$ là: $2 + 7 = 9$.
    
    ---
    **👉 Đáp số:** `9`
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 10 - CHUYÊN ĐỀ: LÝ THUYẾT ĐỒNG DƯ & SỐ DƯ (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 10. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Gọi $r$ là số dư trong phép chia số $A = 2026^{2026}$ cho $100$. 

Hãy tính giá trị của $r$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 10) ---
user_ans_10 = st.text_input("Nhập giá trị của r (số dư):", key="q10_ans")

if st.button("Kiểm tra đáp án Câu 10", key="q10_check"):
    norm_ans_10 = user_ans_10.strip()
    
    # Đáp án chính xác là 76
    if norm_ans_10 == "76":
        st.success("🎉 Chính xác! Bạn đã vận dụng rất xuất sắc lý thuyết đồng dư và tính chất chu kỳ số dư. Lời giải Câu 10 đã được mở khóa.")
    elif user_ans_10 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 10.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy tách $100 = 4 \times 25$. Tìm số dư của $A$ khi chia cho $4$ và $25$ (sử dụng Định lý Euler/Fermat hoặc nhị phân Newton), sau đó dùng Định lý số dư Trung Hoa.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 10 ---
st.markdown("---")

if 'q10_solution_shown' not in st.session_state:
    st.session_state['q10_solution_shown'] = False

col1_10, col2_10 = st.columns([1, 4])
with col1_10:
    if st.button("Xem lời giải Câu 10", key="q10_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q10_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q10_solution_shown'] = False 

if st.session_state.get('q10_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 10 (Tư duy TSA):")
    st.markdown(r"""
    Để tìm số dư của $A = 2026^{2026}$ khi chia cho $100$, ta tìm số dư của $A$ khi chia cho $4$ và $25$ (vì $\gcd(4, 25) = 1$ và $4 \times 25 = 100$).
    
    **Bước 1: Tìm số dư của $A$ khi chia cho $4$**
    
    Ta có $2026$ là số chẵn nên $2026 \text{ } \vdots \text{ } 2 \implies 2026^2 \text{ } \vdots \text{ } 4$.
    Do số mũ $2026 \ge 2$ nên $A = 2026^{2026} \equiv 0 \pmod 4$. $\quad (1)$
    
    **Bước 2: Tìm số dư của $A$ khi chia cho $25$**
    
    Ta có: $2026 = 81 \times 25 + 1 \implies 2026 \equiv 1 \pmod{25}$.
    
    Áp dụng tính chất đồng dư:
    $$A = 2026^{2026} \equiv 1^{2026} \equiv 1 \pmod{25} \quad (2)$$
    
    *(Lưu ý: Nếu số dư cơ số không phải là 1, ta sẽ dùng Định lý Euler: $a^{\varphi(25)} = a^{20} \equiv 1 \pmod{25}$ với $\gcd(a, 5)=1$).*
    
    **Bước 3: Kết hợp bằng hệ phương trình đồng dư**
    
    từ $(1)$ và $(2)$, gọi $r$ là số dư cần tìm ($0 \le r < 100$), ta có hệ:
    $$\begin{cases} r \equiv 0 \pmod 4 \\ r \equiv 1 \pmod{25} \end{cases}$$
    
    từ phương trình thứ hai, $r$ có thể là các giá trị thuộc tập $\{1; 26; 51; 76\}$.
    Trong các giá trị trên, chỉ có duy nhất số $76$ chia hết cho $4$.
    
    Vậy $A \equiv 76 \pmod{100}$, tức là số dư khi chia cho $100$ là $76$.
    
    ---
    **👉 Đáp số Câu 10:** `76`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 11 - CHUYÊN ĐỀ: PHƯƠNG TRÌNH NGHIỆM NGUYÊN & ƯCLN (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 11. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu cặp số nguyên dương $(x; y)$ thỏa mãn đồng thời hai điều kiện sau:
1. Phương trình nghiệm nguyên: $x^2 - 2y^2 = 1$
2. Giá trị của $x$ nhỏ hơn $2000$ ($x < 2000$).
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 11) ---
user_ans_11 = st.text_input("Nhập số lượng cặp số (x; y) thỏa mãn:", key="q11_ans")

if st.button("Kiểm tra đáp án Câu 11", key="q11_check"):
    norm_ans_11 = user_ans_11.strip()
    
    # Đáp án chính xác là 3
    if norm_ans_11 == "3":
        st.success("🎉 Chính xác! Bạn đã nắm rất vững phương pháp giải phương trình Pell (phương trình nghiệm nguyên bậc hai). Lời giải Câu 11 đã được mở khóa.")
    elif user_ans_11 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 11.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Đây là dạng phương trình Pell $x^2 - Dy^2 = 1$. Hãy tìm nghiệm nhỏ nhất $(x_1, y_1) = (3, 2)$ và sử dụng công thức truy hồi hoặc mò trực tiếp các giá trị của $x < 2000$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 11 ---
st.markdown("---")

if 'q11_solution_shown' not in st.session_state:
    st.session_state['q11_solution_shown'] = False

col1_11, col2_11 = st.columns([1, 4])
with col1_11:
    if st.button("Xem lời giải Câu 11", key="q11_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q11_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q11_solution_shown'] = False 

if st.session_state.get('q11_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 11 (Tư duy TSA):")
    st.markdown(r"""
    Phương trình $x^2 - 2y^2 = 1$ là một **phương trình Pell** dạng cơ bản. Để giải phương trình nghiệm nguyên này trong giới hạn $x < 2000$, ta có thể sử dụng phương pháp nghiệm truy hồi hoặc đánh giá theo tính chất số học.
    
    **Bước 1: Tìm nghiệm nguyên dương nhỏ nhất (Nghiệm cơ sở)**
    
    Thử trực tiếp với các giá trị nhỏ của $y$:
    *   Với $y = 1 \implies x^2 = 3$ (loại).
    *   Với $y = 2 \implies x^2 = 2(2^2) + 1 = 9 \implies x = 3$ (thỏa mãn).
    
    Vậy nghiệm nguyên dương nhỏ nhất là $(x_1; y_1) = (3; 2)$.
    
    **Bước 2: Sử dụng công thức nghiệm của phương trình Pell**
    
    Các nghiệm nguyên dương $(x_n; y_n)$ của phương trình được xác định bởi công thức:
    $$x_n + y_n\sqrt{2} = (3 + 2\sqrt{2})^n \quad \text{với } n = 1, 2, 3, \dots$$
    
    Từ đây ta suy ra hệ thức truy hồi để tìm các nghiệm tiếp theo một cách cực kỳ nhanh chóng:
    $$\begin{cases} x_{n+1} = 3x_n + 4y_n \\ y_{n+1} = 2x_n + 3y_n \end{cases}$$
    
    **Bước 3: Liệt kê các nghiệm và đối chiếu điều kiện $x < 2000$**
    
    *   **Với $n = 1$:** Ta có nghiệm thứ nhất $(x_1; y_1) = \mathbf{(3; 2)}$.
        $(x_1 = 3 < 2000 \implies \text{Thỏa mãn})$.
        
    *   **Với $n = 2$:** Áp dụng công thức truy hồi:
        $x_2 = 3(3) + 4(2) = 17$
        $y_2 = 2(3) + 3(2) = 12$
        Ta có nghiệm thứ hai là $(x_2; y_2) = \mathbf{(17; 12)}$.
        $(x_2 = 17 < 2000 \implies \text{Thỏa mãn})$.
        *(Kiểm tra lại: $17^2 - 2 \times 12^2 = 289 - 288 = 1$).*
        
    *   **Với $n = 3$:** Áp dụng công thức truy hồi:
        $x_3 = 3(17) + 4(12) = 99$
        $y_3 = 2(17) + 3(12) = 70$
        Ta có nghiệm thứ ba là $(x_3; y_3) = \mathbf{(99; 70)}$.
        $(x_3 = 99 < 2000 \implies \text{Thỏa mãn})$.
        *(Kiểm tra lại: $99^2 - 2 \times 70^2 = 9801 - 9800 = 1$).*
        
    *   **Với $n = 4$:** Áp dụng công thức truy hồi:
        $x_4 = 3(99) + 4(70) = 297 + 280 = 577$
        $y_4 = 2(99) + 3(70) = 198 + 210 = 408$
        Ta có nghiệm thứ tư là $(x_4; y_4) = \mathbf{(577; 408)}$.
        $(x_4 = 577 < 2000 \implies \text{Thỏa mãn})$.

    *   **Với $n = 5$:** Áp dụng công thức truy hồi:
        $x_5 = 3(577) + 4(408) = 1731 + 1632 = 3363$.
        Vì $x_5 = 3363 > 2000$ nên nghiệm này và các nghiệm sau đó đều không thỏa mãn điều kiện bài toán.
        
    **Bước 4: Kết luận**
    
    Có tất cả **4** cặp số nguyên dương $(x; y)$ thỏa mãn bài toán là: $(3; 2), (17; 12), (99; 70)$ và $(577; 408)$.
    
    ---
    **👉 Đáp số Câu 11:** `4`
    """)

st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 12 - CHUYÊN ĐỀ: DÃY SỐ TRUY HỒI & ĐỒNG DƯ THỨC (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 12. [Trả lời ngắn - Mức độ Vận dụng cao]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho dãy số $(u_n)$ được xác định bởi $u_1 = 5$, $u_2 = 17$ và hệ thức truy hồi:
$$u_{n+2} = 5u_{n+1} - 4u_n \quad (\forall n \ge 1)$$

Tính số dư khi chia số hạng $u_{2026}$ cho $7$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 12) ---
user_ans_12 = st.text_input("Nhập số dư của u_{2026} khi chia cho 7:", key="q12_ans")

if st.button("Kiểm tra đáp án Câu 12", key="q12_check"):
    norm_ans_12 = user_ans_12.strip()
    
    # Đáp án chính xác là 5
    if norm_ans_12 == "5":
        st.success("🎉 Chính xác! Bạn đã tìm công thức tổng quát và vận dụng tính chất chu kỳ số dư rất xuất sắc. Lời giải Câu 12 đã được mở khóa.")
    elif user_ans_12 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 12.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy giải phương trình đặc trưng $r^2 - 5r + 4 = 0$ để tìm công thức tổng quát $u_n = 4^n + 1$, sau đó xét chu kỳ số dư của $4^n$ khi chia cho $7$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 12 ---
st.markdown("---")

if 'q12_solution_shown' not in st.session_state:
    st.session_state['q12_solution_shown'] = False

col1_12, col2_12 = st.columns([1, 4])
with col1_12:
    if st.button("Xem lời giải Câu 12", key="q12_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q12_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q12_solution_shown'] = False 

if st.session_state.get('q12_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 12 (Tư duy TSA):")
    st.markdown(r"""
    Bài toán kết hợp hai kỹ thuật quan trọng: **Tìm số hạng tổng quát của dãy truy hồi tuyến tính cấp 2** và **Tìm số dư bằng chu kỳ đồng dư**.
    
    **Bước 1: Tìm công thức số hạng tổng quát của dãy số $(u_n)$**
    
    Xét phương trình đặc trưng của hệ thức truy hồi $u_{n+2} - 5u_{n+1} + 4u_n = 0$:
    $$r^2 - 5r + 4 = 0 \iff \left[ \begin{array}{l} r = 1 \\ r = 4 \end{array} \right.$$
    
    Do đó, công thức tổng quát của dãy số có dạng:
    $$u_n = A \cdot 1^n + B \cdot 4^n = A + B \cdot 4^n$$
    
    Sử dụng các điều kiện ban đầu ($u_1 = 5, u_2 = 17$), ta lập hệ phương trình:
    $$\begin{cases} u_1 = A + 4B = 5 \\ u_2 = A + 16B = 17 \end{cases} \iff \begin{cases} 12B = 12 \\ A = 5 - 4B \end{cases} \iff \begin{cases} A = 1 \\ B = 1 \end{cases}$$
    
    Vậy công thức số hạng tổng quát là:
    $$u_n = 4^n + 1 \quad (\forall n \ge 1)$$
    
    **Bước 2: Tính số dư của $u_{2026}$ khi chia cho $7$**
    
    Ta cần tính số dư của $u_{2026} = 4^{2026} + 1$ khi chia cho $7$. Hãy xét chu kỳ lũy thừa của $4$ modulo $7$:
    *   $4^1 \equiv 4 \pmod 7$
    *   $4^2 = 16 \equiv 2 \pmod 7$
    *   $4^3 = 64 \equiv 1 \pmod 7$
    
    Ta thấy chu kỳ số dư lặp lại sau mỗi **3** bước.
    
    Xét số mũ $2026$ khi chia cho $3$:
    $$2026 = 3 \times 675 + 1 \implies 2026 \equiv 1 \pmod 3$$
    
    Do đó:
    $$4^{2026} = (4^3)^{675} \cdot 4^1 \equiv 1^{675} \cdot 4 \equiv 4 \pmod 7$$
    
    **Bước 3: Kết luận**
    
    Thay vào biểu thức của $u_{2026}$, ta có:
    $$u_{2026} = 4^{2026} + 1 \equiv 4 + 1 \equiv 5 \pmod 7$$
    
    Vậy số dư khi chia số hạng $u_{2026}$ cho $7$ là $5$.
    
    ---
    **👉 Đáp số Câu 12:** `5`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 13 - CHUYÊN ĐỀ: SỐ HỌC & TỔ HỢP (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 13. [Trả lời ngắn - Mức độ Vận dụng cao]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $N = 2^{10} \cdot 3^8 \cdot 5^6$. Tính số lượng các ước số dương của $N$ đồng thời là bội của số $M = 2^5 \cdot 3^3 \cdot 5^2$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 13) ---
user_ans_13 = st.text_input("Nhập số lượng ước số thỏa mãn:", key="q13_ans")

if st.button("Kiểm tra đáp án Câu 13", key="q13_check"):
    norm_ans_13 = user_ans_13.strip()
    
    # Đáp án chính xác là 180
    if norm_ans_13 == "180":
        st.success("🎉 Chính xác! Bạn đã hiểu rất rõ bản chất của quan hệ chia hết và quy tắc đếm tổ hợp. Lời giải Câu 13 đã được mở khóa.")
    elif user_ans_13 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 13.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Gọi ước số là $d = 2^x \cdot 3^y \cdot 5^z$. Để $d$ vừa là ước của $N$ vừa là bội của $M$ thì $5 \le x \le 10$, $3 \le y \le 8$ và $2 \le z \le 6$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 13 ---
st.markdown("---")

if 'q13_solution_shown' not in st.session_state:
    st.session_state['q13_solution_shown'] = False

col1_13, col2_13 = st.columns([1, 4])
with col1_13:
    if st.button("Xem lời giải Câu 13", key="q13_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q13_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q13_solution_shown'] = False 

if st.session_state.get('q13_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 13 (Tư duy TSA):")
    st.markdown(r"""
    Đây là bài toán tổ hợp số học tiêu biểu trong đề thi TSA. Để giải quyết, ta sử dụng điều kiện cần và đủ của phép chia hết trong dạng phân tích ra thừa số nguyên tố.
    
    **Bước 1: Thiết lập dạng của ước số thỏa mãn**
    
    Một số nguyên dương $d$ là ước của $N = 2^{10} \cdot 3^8 \cdot 5^6$ nên $d$ chỉ chứa các thừa số nguyên tố $2, 3, 5$. Do đó, $d$ có dạng:
    $$d = 2^x \cdot 3^y \cdot 5^z \quad (x, y, z \in \mathbb{N})$$
    
    Để $d$ **là ước của $N$** thì số mũ của các thừa số không được vượt quá số mũ tương ứng trong $N$:
    $$x \le 10; \quad y \le 8; \quad z \le 6$$
    
    Đồng thời, để $d$ **là bội của $M = 2^5 \cdot 3^3 \cdot 5^2$** (tức là $d$ chia hết cho $M$) thì số mũ của các thừa số trong $d$ phải lớn hơn hoặc bằng số mũ tương ứng trong $M$:
    $$x \ge 5; \quad y \ge 3; \quad z \ge 2$$
    
    **Bước 2: Đếm số cách chọn các số mũ $x, y, z$**
    
    Kết hợp hai điều kiện trên, ta có miền giá trị cho từng số mũ:
    *   Số mũ $x \in \{5, 6, 7, 8, 9, 10\}$ $\implies$ Có $10 - 5 + 1 = \mathbf{6}$ cách chọn.
    *   Số mũ $y \in \{3, 4, 5, 6, 7, 8\}$ $\implies$ Có $8 - 3 + 1 = \mathbf{6}$ cách chọn.
    *   Số mũ $z \in \{2, 3, 4, 5, 6\}$ $\implies$ Có $6 - 2 + 1 = \mathbf{5}$ cách chọn.
    
    **Bước 3: Tính kết quả bằng quy tắc nhân**
    
    Mỗi ước số thỏa mãn yêu cầu bài toán tương ứng duy nhất với một bộ ba số mũ $(x; y; z)$. 
    Áp dụng quy tắc nhân, tổng số lượng các ước số dương cần tìm là:
    $$6 \times 6 \times 5 = 180 \text{ (ước số)}$$
    
    ---
    **👉 Đáp số Câu 13:** `180`
    """)

st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 14 - CHUYÊN ĐỀ: CẤU TRÚC HÀM SỐ ƯỚC SỐ & TỐI ƯU (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 14. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số nguyên dương $n$ **nhỏ nhất** thỏa mãn đồng thời hai điều kiện sau:
1. Số $n$ chia hết cho $6$.
2. Số $n$ có đúng $20$ ước số nguyên dương.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 14) ---
user_ans_14 = st.text_input("Nhập giá trị nhỏ nhất của số n:", key="q14_ans")

if st.button("Kiểm tra đáp án Câu 14", key="q14_check"):
    norm_ans_14 = user_ans_14.strip()
    
    # Đáp án chính xác là 240
    if norm_ans_14 == "240":
        st.success("🎉 Chính xác! Bạn có tư duy tối ưu hóa và phân tích hàm ước số cực kỳ sắc bén. Lời giải Câu 14 đã được mở khóa.")
    elif user_ans_14 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 14.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Phân tích số lượng ước $20 = 10 \times 2 = 5 \times 4 = 5 \times 2 \times 2$. Để $n$ nhỏ nhất và chia hết cho $6 = 2 \times 3$, hãy gán số mũ lớn nhất cho thừa số nguyên tố nhỏ nhất (số $2$).")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 14 ---
st.markdown("---")

if 'q14_solution_shown' not in st.session_state:
    st.session_state['q14_solution_shown'] = False

col1_14, col2_14 = st.columns([1, 4])
with col1_14:
    if st.button("Xem lời giải Câu 14", key="q14_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q14_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q14_solution_shown'] = False 

if st.session_state.get('q14_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 14 (Tư duy TSA):")
    st.markdown(r"""
    Đây là bài toán kết hợp lý thuyết cấu trúc số và tối ưu hóa rời rạc.
    
    **Bước 1: Lý thuyết cấu trúc số lượng ước số**
    
    Một số nguyên dương $n$ khi phân tích ra thừa số nguyên tố có dạng:
    $$n = p_1^{a_1} \cdot p_2^{a_2} \cdots p_k^{a_k}$$
    Khi đó, tổng số ước số nguyên dương của $n$ (ký hiệu là $\tau(n)$) được tính bởi công thức:
    $$\tau(n) = (a_1 + 1)(a_2 + 1)\cdots(a_k + 1) = 20$$
    
    Do $n \text{ } \vdots \text{ } 6 \implies n \text{ } \vdots \text{ } (2 \times 3)$, số $n$ bắt buộc phải chứa ít nhất hai thừa số nguyên tố là $2$ và $3$.
    
    **Bước 2: Phân tích số $20$ thành tích các thừa số lớn hơn $1$**
    
    Ta có các cách phân tích số $20$ sau:
    *   $20 = 20$ (Loại, vì tương ứng với $n = p^{19}$, chỉ có $1$ thừa số nguyên tố).
    *   $20 = 10 \times 2 \implies n = p_1^9 \cdot p_2^1$.
    *   $20 = 5 \times 4 \implies n = p_1^4 \cdot p_2^3$.
    *   $20 = 5 \times 2 \times 2 \implies n = p_1^4 \cdot p_2^1 \cdot p_3^1$.
    
    **Bước 3: Tìm cực trị trong từng trường hợp (Ưu tiên số mũ lớn cho nguyên tố nhỏ)**
    
    *   **Trường hợp 1: $n = p_1^9 \cdot p_2^1$**
        Vì $n$ chứa thừa số $2$ và $3$, để $n$ nhỏ nhất ta chọn $p_1 = 2, p_2 = 3$:
        $$n = 2^9 \cdot 3^1 = 512 \times 3 = 1536$$
        
    *   **Trường hợp 2: $n = p_1^4 \cdot p_2^3$**
        Để $n$ nhỏ nhất, gán số mũ lớn ($4$) cho nguyên tố nhỏ ($2$), số mũ nhỏ ($3$) cho nguyên tố lớn hơn ($3$):
        $$n = 2^4 \cdot 3^3 = 16 \times 27 = 432$$
        
    *   **Trường hợp 3: $n = p_1^4 \cdot p_2^1 \cdot p_3^1$**
        Ở đây $n$ có $3$ thừa số nguyên tố. Do $n \text{ } \vdots \text{ } 6$, ta đã có $2$ và $3$. Để $n$ nhỏ nhất, thừa số nguyên tố thứ ba $p_3$ phải là số nguyên tố nhỏ nhất tiếp theo, tức là $p_3 = 5$.
        Gán số mũ cao nhất ($4$) cho số nguyên tố nhỏ nhất ($2$):
        $$n = 2^4 \cdot 3^1 \cdot 5^1 = 16 \times 3 \times 5 = 240$$
        
    **Bước 4: Kết luận**
    
    So sánh các giá trị tìm được ($1536 > 432 > 240$), số nguyên dương nhỏ nhất thỏa mãn yêu cầu bài toán là $240$.
    
    ---
    **👉 Đáp số Câu 14:** `240`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 15 - CHUYÊN ĐỀ: THUẬT TOÁN EUCLID & PHÂN SỐ TỐI GIẢN (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 15. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu số nguyên dương $n$ thuộc đoạn $[1; 2026]$ sao cho phân số sau **KHÔNG** phải là phân số tối giản (chưa tối giản):
$$P = \frac{n^2 + 4}{n + 5}$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 15) ---
user_ans_15 = st.text_input("Nhập số lượng giá trị n thỏa mãn:", key="q15_ans")

if st.button("Kiểm tra đáp án Câu 15", key="q15_check"):
    norm_ans_15 = user_ans_15.strip()
    
    # Đáp án chính xác là 70
    if norm_ans_15 == "70":
        st.success("🎉 Chính xác! Bạn đã vận dụng thuật toán Euclid cho đa thức và tính chất ước chung lớn nhất vô cùng bậc thầy. Lời giải Câu 15 đã được mở khóa.")
    elif user_ans_15 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 15.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy biến đổi tử số $n^2 + 4 = (n+5)(n-5) + 29$. Để phân số chưa tối giản thì tử số và mẫu số phải có ước chung lớn hơn $1$, dẫn đến $n + 5$ phải chia hết cho $29$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 15 ---
st.markdown("---")

if 'q15_solution_shown' not in st.session_state:
    st.session_state['q15_solution_shown'] = False

col1_15, col2_15 = st.columns([1, 4])
with col1_15:
    if st.button("Xem lời giải Câu 15", key="q15_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q15_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q15_solution_shown'] = False 

if st.session_state.get('q15_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 15 (Tư duy TSA):")
    st.markdown(r"""
    Để giải bài toán phân số tối giản chứa đa thức, công cụ mạnh mẽ nhất là **Thuật toán Euclid (Tìm ước chung lớn nhất của hai đa thức)**.
    
    **Bước 1: Tìm ước chung lớn nhất của tử số và mẫu số**
    
    Gọi $d = \gcd(n^2 + 4, n + 5)$ là ước chung lớn nhất của tử số và mẫu số ($d \in \mathbb{N}^*$).
    
    Thực hiện phép chia đa thức $n^2 + 4$ cho $n + 5$, ta có biến đổi sau:
    $$n^2 + 4 = n^2 - 25 + 29 = (n + 5)(n - 5) + 29$$
    
    Theo tính chất của ước chung lớn nhất:
    $$d = \gcd\left((n + 5)(n - 5) + 29, n + 5\right) = \gcd(29, n + 5)$$
    
    **Bước 2: Biện luận điều kiện để phân số KHÔNG tối giản**
    
    Vì $29$ là **số nguyên tố**, nên ước chung lớn nhất $d$ chỉ có thể nhận hai giá trị là $1$ hoặc $29$.
    *   Nếu $d = 1$, phân số $P$ là phân số tối giản.
    *   Để phân số $P$ **KHÔNG** tối giản (chưa tối giản) thì buộc ta phải có $d > 1$, tức là:
        $$d = 29 \iff (n + 5) \text{ } \vdots \text{ } 29$$
        
    **Bước 3: Tìm quy luật và đếm số lượng giá trị $n \in [1; 2026]$**
    
    Để $(n + 5) \text{ } \vdots \text{ } 29$, thì số $n$ phải có dạng:
    $$n + 5 = 29k \iff n = 29k - 5 \quad (k \in \mathbb{Z})$$
    *(Hoặc viết dưới dạng số dư: $n \equiv 24 \pmod{29}$, tức $n = 29m + 24$ với $m \ge 0$).*
    
    Áp dụng điều kiện giới hạn của đề bài ($1 \le n \le 2026$):
    $$1 \le 29k - 5 \le 2026$$
    $$\iff 6 \le 29k \le 2031$$
    $$\iff 0.2 \le k \le 70.03$$
    
    Vì $k$ là số nguyên ($k \in \mathbb{Z}$), nên $k$ có thể nhận các giá trị:
    $$k \in \{1; 2; 3; \dots; 70\}$$
    
    Số lượng giá trị $k$ thỏa mãn (cũng chính là số lượng số nguyên dương $n$ cần tìm) là:
    $$70 - 1 + 1 = 70 \text{ (giá trị)}$$
    
    *(Cụ thể, các giá trị của $n$ là: $24, 53, 82, \dots, 2025$).*
    
    ---
    **👉 Đáp số Câu 15:** `70`
    """)

st.markdown("---")
