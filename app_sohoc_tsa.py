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
$$P = \dfrac{n^2 + 4}{n + 5}$$
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



# =====================================================================
# CÂU HỎI SỐ 16 - CHUYÊN ĐỀ: SỐ NGUYÊN TỐ & ĐỒNG DƯ THỨC (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 16. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu số nguyên tố $p$ thuộc khoảng $(0; 2026)$ sao cho biểu thức sau cũng là một **số nguyên tố**:
$$A = p^2 + 2^p$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 16) ---
user_ans_16 = st.text_input("Nhập số lượng số nguyên tố p thỏa mãn:", key="q16_ans")

if st.button("Kiểm tra đáp án Câu 16", key="q16_check"):
    norm_ans_16 = user_ans_16.strip()
    
    # Đáp án chính xác là 1 (chỉ có p = 3)
    if norm_ans_16 == "1":
        st.success("🎉 Chính xác! Bạn đã dùng phương pháp xét số dư theo Mô-đun 3 cực kỳ chuẩn xác để chứng minh tính duy nhất. Lời giải Câu 16 đã được mở khóa.")
    elif user_ans_16 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 16.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy thử nghiệm với các số nguyên tố nhỏ ($p = 2, 3$), sau đó với $p > 3$, hãy xét số dư của $p^2$ và $2^p$ khi chia cho $3$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 16 ---
st.markdown("---")

if 'q16_solution_shown' not in st.session_state:
    st.session_state['q16_solution_shown'] = False

col1_16, col2_16 = st.columns([1, 4])
with col1_16:
    if st.button("Xem lời giải Câu 16", key="q16_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q16_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q16_solution_shown'] = False 

if st.session_state.get('q16_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 16 (Tư duy TSA):")
    st.markdown(r"""
    Để giải bài toán số nguyên tố với số mũ biến thiên, phương pháp hiệu quả nhất là **xét tính chia hết cho $3$ (Mô-đun $3$)**.
    
    **Bước 1: Thử trực tiếp với các số nguyên tố nhỏ ($p = 2$ và $p = 3$)**
    
    *   **With $p = 2$:** Ta có $A = 2^2 + 2^2 = 4 + 4 = 8$. Vì $8$ là số hợp số nên $p = 2$ (Loại).
    *   **Với $p = 3$:** Ta có $A = 3^2 + 2^3 = 9 + 8 = 17$. Vì $17$ là số nguyên tố nên **$p = 3$ thỏa mãn**.
    
    **Bước 2: Chứng minh không tồn tại nghiệm với mọi số nguyên tố $p > 3$**
    
    Với mọi số nguyên tố $p > 3$, số $p$ chắc chắn là **số lẻ** và **không chia hết cho $3$**.
    
    1.  **Xét số dư của $p^2$ khi chia cho $3$:**
        Mọi số nguyên không chia hết cho $3$ khi bình phương lên luôn chia $3$ dư $1$.
        $$\implies p^2 \equiv 1 \pmod 3 \quad (1)$$
        
    2.  **Xét số dư của $2^p$ khi chia cho $3$:**
        Vì $p > 3$ là số nguyên tố nên $p$ là số lẻ, ta đặt $p = 2k + 1$ ($k \in \mathbb{N}^*$).
        Ta có:
        $$2^p = 2^{2k+1} = 2 \cdot (2^2)^k = 2 \cdot 4^k$$
        Vì $4 \equiv 1 \pmod 3 \implies 4^k \equiv 1 \pmod 3$.
        $$\implies 2^p \equiv 2 \cdot 1 \equiv 2 \pmod 3 \quad (2)$$
        
    **Bước 3: Tổng hợp kết quả**
    
    từ $(1)$ và $(2)$, cộng vế theo vế ta được:
    $$A = p^2 + 2^p \equiv 1 + 2 \equiv 3 \equiv 0 \pmod 3$$
    
    Nghĩa là với mọi số nguyên tố $p > 3$, biểu thức $A = p^2 + 2^p$ luôn chia hết cho $3$. 
    Hơn nữa, vì $p > 3 \implies A > 17 > 3$. Một số lớn hơn $3$ và chia hết cho $3$ chắc chắn là **hợp số**.
    
    **Bước 4: Kết luận**
    
    Trong khoảng $(0; 2026)$, chỉ có **duy nhất $1$ số nguyên tố** thỏa mãn bài toán là $p = 3$.
    
    ---
    **👉 Đáp số Câu 16:** `1`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 17 - CHUYÊN ĐỀ: CÔNG THỨC LEGENDRE & GIAI THỪA (VDC)
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 17. [Trả lời ngắn - TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số nguyên tự nhiên $k$ **lớn nhất** sao cho số $2026!$ (giai thừa của $2026$) chia hết cho $12^k$:
$$2026! \text{ } \vdots \text{ } 12^k$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 17) ---
user_ans_17 = st.text_input("Nhập giá trị lớn nhất của k:", key="q17_ans")

if st.button("Kiểm tra đáp án Câu 17", key="q17_check"):
    norm_ans_17 = user_ans_17.strip()
    
    # Đáp án chính xác là 1009 (Bẫy kinh điển: v_2/2 nhỏ hơn v_3)
    if norm_ans_17 == "1009":
        st.success("🎉 Xuất sắc! Bạn đã vượt qua 'bẫy tư duy' kinh điển của TSA. Số mũ của thừa số 2 mới là yếu tố giới hạn chứ không phải thừa số 3! Lời giải Câu 17 đã được mở khóa.")
    elif norm_ans_17 == "1010":
        st.error("❌ Bạn đã rơi vào 'bẫy' rồi! 1010 là số mũ của thừa số 3 trong 2026!. Nhưng $12 = 2^2 \times 3$, hãy kiểm tra xem số mũ của $2^2$ trong 2026! có đủ 1010 không nhé!")
    elif user_ans_17 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 17.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Sử dụng công thức Legendre $v_p(n!) = \sum \lfloor \frac{n}{p^i} \rfloor$ để tính số mũ của nguyên tố $2$ và $3$ trong $2026!$. Chú ý $12 = 2^2 \times 3^1$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 17 ---
st.markdown("---")

if 'q17_solution_shown' not in st.session_state:
    st.session_state['q17_solution_shown'] = False

col1_17, col2_17 = st.columns([1, 4])
with col1_17:
    if st.button("Xem lời giải Câu 17", key="q17_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q17_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q17_solution_shown'] = False 

if st.session_state.get('q17_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 17 (Tư duy TSA):")
    st.markdown(r"""
    Đây là một bài toán Số học có **bẫy tư duy rất sâu** nhằm phân loại học sinh giỏi thực sự trong kỳ thi TSA.
    
    **Bước 1: Phân tích cơ số và yêu cầu bài toán**
    
    Ta phân tích số $12$ ra thừa số nguyên tố:
    $$12 = 2^2 \times 3^1 \implies 12^k = 2^{2k} \times 3^k$$
    
    Để $2026!$ chia hết cho $12^k$, thì số mũ của nguyên tố $2$ trong $2026!$ phải $\ge 2k$, và số mũ của nguyên tố $3$ phải $\ge k$.
    
    Gọi $v_p(n!)$ là số mũ của số nguyên tố $p$ trong phân tích ra thừa số nguyên tố của $n!$. Theo **công thức Legendre**:
    $$v_p(n!) = \lfloor \frac{n}{p} \rfloor + \lfloor \frac{n}{p^2} \rfloor + \lfloor \frac{n}{p^3} \rfloor + \cdots$$
    
    **Bước 2: Tính số mũ của nguyên tố $3$ trong $2026!$ ($v_3$)**
    
    $$v_3(2026!) = \lfloor \frac{2026}{3} \rfloor + \lfloor \frac{2026}{9} \rfloor + \lfloor \frac{2026}{27} \rfloor + \lfloor \frac{2026}{81} \rfloor + \lfloor \frac{2026}{243} \rfloor + \lfloor \frac{2026}{729} \rfloor$$
    $$v_3(2026!) = 675 + 225 + 75 + 25 + 8 + 2 = 1010$$
    
    $\implies$ Từ điều kiện thừa số $3$, ta có $k \le 1010$. *(90% học sinh chủ quan dừng ở đây và chọn đáp số 1010).*
    
    **Bước 3: Tính số mũ của nguyên tố $2$ trong $2026!$ ($v_2$) - BẢN CHẤT CỦA BẪY!**
    
    Thông thường thừa số lớn hơn (số $3$) sẽ là yếu tố giới hạn. Nhưng vì số $12$ cần tới **HAI** thừa số $2$ ($2^2$), ta buộc phải kiểm tra $v_2(2026!)$:
    
    $$v_2(2026!) = \lfloor \frac{2026}{2} \rfloor + \lfloor \frac{2026}{4} \rfloor + \lfloor \frac{2026}{8} \rfloor + \lfloor \frac{2026}{16} \rfloor + \lfloor \frac{2026}{32} \rfloor + \lfloor \frac{2026}{64} \rfloor + \lfloor \frac{2026}{128} \rfloor + \lfloor \frac{2026}{256} \rfloor + \lfloor \frac{2026}{512} \rfloor + \lfloor \frac{2026}{1024} \rfloor$$
    $$v_2(2026!) = 1013 + 506 + 253 + 126 + 63 + 31 + 15 + 7 + 3 + 1 = 2018$$
    
    Do đó, trong $2026!$ có chứa thừa số $2^{2018}$. 
    Số lượng cụm $2^2$ (tức là $4$) tối đa có thể tạo ra là:
    $$\lfloor \frac{v_2}{2} \rfloor = \lfloor \frac{2018}{2} \rfloor = 1009$$
    
    **Bước 4: Sử dụng tư duy "Nút thắt cổ chai" để kết luận**
    
    Trong số $2026!$, ta có:
    *   Tạo được tối đa **$1009$** thừa số $4$ ($2^2$).
    *   Tạo được tối đa **$1010$** thừa số $3$.
    
    Vì $12 = 4 \times 3$, số lượng thừa số $12$ tối đa ghép được sẽ bị giới hạn bởi số nhỏ hơn giữa $1009$ và $1010$.
    $$k_{max} = \min(1009; 1010) = 1009$$
    
    ---
    **👉 Đáp số Câu 17:** `1009`
    """)

st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 18 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 18. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho dãy số $(u_n)$ được xác định bởi $u_1 = 1$, $u_2 = 3$ và hệ thức truy hồi $u_{n+1} = 3u_n - 2u_{n-1}$ với mọi $n \ge 2$. Tìm số dư của số hạng $u_{2026}$ khi chia cho số nguyên tố $1009$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 18) ---
user_ans_18 = st.text_input("Nhập số dư của u_{2026} khi chia cho 1009:", key="q18_ans")

if st.button("Kiểm tra đáp án Câu 18", key="q18_check"):
    norm_ans_18 = user_ans_18.strip()
    
    # Đáp án chính xác là 14
    if norm_ans_18 == "14":
        st.success("🎉 Chính xác! Bạn đã tìm công thức tổng quát và vận dụng định lý Fermat nhỏ cực kỳ xuất sắc. Lời giải Câu 18 đã được mở khóa.")
    elif user_ans_18 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 18.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Tìm công thức tổng quát của dãy số dạng $u_n = 2^n - 1$, sau đó dùng định lý Fermat nhỏ để tính $2^{2026} \pmod{1009}$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 18 ---
st.markdown("---")

if 'q18_solution_shown' not in st.session_state:
    st.session_state['q18_solution_shown'] = False

col1_18, col2_18 = st.columns([1, 4])
with col1_18:
    if st.button("Xem lời giải Câu 18", key="q18_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q18_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q18_solution_shown'] = False 

if st.session_state.get('q18_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 18 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Tìm công thức tổng quát của dãy số $(u_n)$**
    
    Phương trình đặc trưng của hệ thức truy hồi $u_{n+1} - 3u_n + 2u_{n-1} = 0$ là:
    $$r^2 - 3r + 2 = 0 \iff \begin{cases} r = 1 \\ r = 2 \end{cases}$$
    
    Do đó, số hạng tổng quát của dãy số có dạng:
    $$u_n = A \cdot 1^n + B \cdot 2^n = A + B \cdot 2^n$$
    
    Sử dụng điều kiện ban đầu ($u_1 = 1$, $u_2 = 3$), ta có hệ phương trình:
    $$\begin{cases} u_1 = A + 2B = 1 \\ u_2 = A + 4B = 3 \end{cases} \iff \begin{cases} 2B = 2 \\ A + 2(1) = 1 \end{cases} \iff \begin{cases} A = -1 \\ B = 1 \end{cases}$$
    
    Vậy công thức tổng quát của dãy số là:
    $$u_n = 2^n - 1 \quad (\forall n \ge 1)$$
    
    **Bước 2: Tính số hạng $u_{2026}$ modulo $1009$**
    
    Ta cần tính số dư của $u_{2026} = 2^{2026} - 1$ khi chia cho số nguyên tố $1009$.
    
    Theo **Định lý Fermat nhỏ**, vì $1009$ là số nguyên tố và $\gcd(2, 1009) = 1$, ta có:
    $$2^{1008} \equiv 1 \pmod{1009}$$
    
    Chia số mũ $2026$ cho $1008$:
    $$2026 = 2 \times 1008 + 10$$
    
    Do đó:
    $$2^{2026} = (2^{1008})^2 \cdot 2^{10} \equiv 1^2 \cdot 1024 \pmod{1009}$$
    
    Vì $1024 = 1 \times 1009 + 15$, suy ra:
    $$2^{2026} \equiv 15 \pmod{1009}$$
    
    **Bước 3: Kết luận**
    
    Số dư của $u_{2026}$ khi chia cho $1009$ là:
    $$u_{2026} = 2^{2026} - 1 \equiv 15 - 1 = 14 \pmod{1009}$$
    
    ---
    **👉 Đáp số Câu 18:** `14`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 19 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 19. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho tập hợp $S = \{1, 2, 3, \dots, 100\}$. Gọi $K$ là số các tập con gồm đúng 3 phần tử được chọn từ tập $S$ sao cho tổng các phần tử của tập con đó chia hết cho $3$. Tính giá trị của $K$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 19) ---
user_ans_19 = st.text_input("Nhập giá trị của K:", key="q19_ans")

if st.button("Kiểm tra đáp án Câu 19", key="q19_check"):
    norm_ans_19 = user_ans_19.strip()
    
    # Đáp án chính xác là 53922
    if norm_ans_19 == "53922":
        st.success("🎉 Chính xác! Bạn đã phân chia số dư mô-đun 3 và áp dụng tổ hợp vô cùng chính xác. Lời giải Câu 19 đã được mở khóa.")
    elif user_ans_19 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 19.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Chia tập $S$ thành 3 tập con dựa theo số dư khi chia cho $3$, sau đó xét các trường hợp chọn 3 phần tử sao cho tổng chia hết cho $3$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 19 ---
st.markdown("---")

if 'q19_solution_shown' not in st.session_state:
    st.session_state['q19_solution_shown'] = False

col1_19, col2_19 = st.columns([1, 4])
with col1_19:
    if st.button("Xem lời giải Câu 19", key="q19_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q19_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q19_solution_shown'] = False 

if st.session_state.get('q19_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 19 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân chia tập hợp $S$ theo số dư khi chia cho $3$**
    
    Chia tập hợp $S = \{1, 2, 3, \dots, 100\}$ thành ba tập hợp con rời nhau dựa trên số dư khi chia cho $3$:
    *   $R_0$: Các số chia hết cho $3$ ($n \equiv 0 \pmod 3$), gồm: $\{3, 6, 9, \dots, 99\}$. 
        Số lượng phần tử là: $|R_0| = \dfrac{99}{3} = 33$ phần tử.
    *   $R_1$: Các số chia $3$ dư $1$ ($n \equiv 1 \pmod 3$), gồm: $\{1, 4, 7, \dots, 100\}$. 
        Số lượng phần tử là: $|R_1| = \dfrac{100 - 1}{3} + 1 = 34$ phần tử.
    *   $R_2$: Các số chia $3$ dư $2$ ($n \equiv 2 \pmod 3$), gồm: $\{2, 5, 8, \dots, 98\}$. 
        Số lượng phần tử là: $|R_2| = \dfrac{98 - 2}{3} + 1 = 33$ phần tử.
    
    **Bước 2: Xét các trường hợp chọn 3 phần tử có tổng chia hết cho $3$**
    
    Gọi bộ 3 phần tử được chọn là $\{a, b, c\}$. Tổng $a + b + c$ chia hết cho $3$ khi và chỉ khi tổng số dư của ba phần tử đó khi chia cho $3$ phải chia hết cho $3$. Ta có các trường hợp sau:
    
    1. **Trường hợp 1: Cả 3 phần tử đều thuộc $R_0$** (số dư dạng $0 + 0 + 0 \equiv 0 \pmod 3$).
       Số cách chọn là: 
       $$\mathbf{C_1} = \dbinom{33}{3} = \dfrac{33 \times 32 \times 31}{6} = 5456$$
       
    2. **Trường hợp 2: Cả 3 phần tử đều thuộc $R_1$** (số dư dạng $1 + 1 + 1 = 3 \equiv 0 \pmod 3$).
       Số cách chọn là: 
       $$\mathbf{C_2} = \dbinom{34}{3} = \dfrac{34 \times 33 \times 32}{6} = 5984$$
       
    3. **Trường hợp 3: Cả 3 phần tử đều thuộc $R_2$** (số dư dạng $2 + 2 + 2 = 6 \equiv 0 \pmod 3$).
       Số cách chọn là: 
       $$\mathbf{C_3} = \dbinom{33}{3} = \dfrac{33 \times 32 \times 31}{6} = 5456$$
       
    4. **Trường hợp 4: Mỗi tập hợp $R_0, R_1, R_2$ được chọn đúng 1 phần tử** (số dư dạng $0 + 1 + 2 = 3 \equiv 0 \pmod 3$).
       Số cách chọn là: 
       $$\mathbf{C_4} = |R_0| \times |R_1| \times |R_2| = 33 \times 34 \times 33 = 37026$$
       
    **Bước 3: Tính tổng số cách chọn $K$**
    
    Áp dụng quy tắc cộng, tổng số tập con $K$ thỏa mãn yêu cầu bài toán là:
    $$K = C_1 + C_2 + C_3 + C_4 = 5456 + 5984 + 5456 + 37026 = 53922$$
    
    ---
    **👉 Đáp số Câu 19:** `53922`
    """)

st.markdown("---")



# ==========================================
# CÂU 20
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 20 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Có bao nhiêu số tự nhiên $n$ có 3 chữ số sao cho biểu thức $n^2 + 3n + 5$ chia hết cho $11$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_20 = st.text_input("Nhập số lượng giá trị của n:", key="q20_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q20_check"):
    normalized_user_answer = user_answer_20.strip()
    
    # Đáp án chính xác là 82
    if normalized_user_answer == "82":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_20 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thử thêm bớt để tạo thành hằng đẳng thức theo module 11 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q20_solution_shown' not in st.session_state:
    st.session_state['q20_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q20_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q20_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q20_solution_shown'] = False 

if st.session_state.get('q20_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biến đổi biểu thức về dạng bình phương**
    
    Ta cần tìm $n$ sao cho $n^2 + 3n + 5 \equiv 0 \pmod{11}$.
    
    Nhân cả 2 vế với 4 (vì 4 và 11 nguyên tố cùng nhau), ta được:
    $$4n^2 + 12n + 20 \equiv 0 \pmod{11}$$
    $$(2n + 3)^2 + 11 \equiv 0 \pmod{11}$$
    $$(2n + 3)^2 \equiv 0 \pmod{11}$$
    
    *Cách 2 (Thêm bớt trực tiếp):*
    Ta có: $n^2 + 3n + 5 = n^2 - 8n + 16 - 11 = (n - 4)^2 - 11$.
    Để biểu thức chia hết cho $11$ thì $(n - 4)^2 \vdots 11$.
    
    **Bước 2: Tìm điều kiện của $n$**
    
    Vì $11$ là số nguyên tố nên $(n - 4)^2 \vdots 11 \Leftrightarrow n - 4 \vdots 11$.
    
    Do đó, $n \equiv 4 \pmod{11}$, hay $n = 11k + 4$ (với $k \in \mathbb{Z}$).
    
    **Bước 3: Kết hợp điều kiện n có 3 chữ số**
    
    Vì $n$ là số tự nhiên có 3 chữ số nên:
    $$100 \le n \le 999$$
    $$100 \le 11k + 4 \le 999$$
    $$96 \le 11k \le 995$$
    $$\dfrac{96}{11} \le k \le \dfrac{995}{11}$$
    $$8,72 \le k \le 90,45$$
    
    Vì $k \in \mathbb{Z}$ nên $k \in \{9; 10; 11; ... ; 90\}$.
    
    **Bước 4: Tính số lượng giá trị thỏa mãn**
    
    Số lượng các giá trị của $k$ (cũng chính là số lượng các giá trị của $n$ thỏa mãn) là:
    $$90 - 9 + 1 = 82 \text{ (số)}$$
    
    **Kết luận:** Có **$82$** số tự nhiên thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 21
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 21 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi
st.markdown(r"""
Cho dãy số $(u_n)$ thỏa mãn $u_1 = 1$, $u_2 = 3$ và $u_{n+2} = 3u_{n+1} - 2u_n$ với mọi $n \ge 1$. 

Tính tổng $10$ số hạng đầu tiên của dãy số: $S = u_1 + u_2 + ... + u_{10}$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_21 = st.text_input("Nhập tổng S:", key="q21_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q21_check"):
    normalized_user_answer = user_answer_21.strip()
    
    # Đáp án chính xác là 2036
    if normalized_user_answer == "2036":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_21 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy thiết lập công thức tổng quát của dãy số trước khi tính tổng nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q21_solution_shown' not in st.session_state:
    st.session_state['q21_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q21_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q21_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q21_solution_shown'] = False 

if st.session_state.get('q21_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm công thức tổng quát của dãy số $(u_n)$**
    
    Từ hệ thức truy hồi $u_{n+2} = 3u_{n+1} - 2u_n$, ta có phương trình đặc trưng:
    $$\lambda^2 - 3\lambda + 2 = 0 \Leftrightarrow \lambda_1 = 1, \lambda_2 = 2$$
    
    Do đó, công thức tổng quát của dãy số có dạng:
    $$u_n = A \cdot 1^n + B \cdot 2^n = A + B \cdot 2^n$$
    
    Dựa vào điều kiện ban đầu, ta có hệ phương trình:
    $$
    \begin{cases}
    u_1 = A + 2B = 1 \\
    u_2 = A + 4B = 3
    \end{cases}
    \Rightarrow 
    \begin{cases}
    2B = 2 \\
    A + 2B = 1
    \end{cases}
    \Rightarrow 
    \begin{cases}
    B = 1 \\
    A = -1
    \end{cases}
    $$
    
    Vậy số hạng tổng quát của dãy số là:
    $$u_n = 2^n - 1 \quad (\forall n \ge 1)$$
    
    **Bước 2: Tính tổng $S = u_1 + u_2 + ... + u_{10}$**
    
    Ta thay công thức tổng quát vào tổng $S$:
    $$S = (2^1 - 1) + (2^2 - 1) + ... + (2^{10} - 1)$$
    $$S = (2^1 + 2^2 + ... + 2^{10}) - (\underbrace{1 + 1 + ... + 1}_{10 \text{ số}})$$
    
    Tổng các số hạng của cấp số nhân $2^1 + 2^2 + ... + 2^{10}$ là:
    $$S_{CSN} = \dfrac{2(1 - 2^{10})}{1 - 2} = 2^{11} - 2 = 2048 - 2 = 2046$$
    
    **Bước 3: Kết luận kết quả**
    
    $$S = 2046 - 10 = 2036$$
    
    **Kết luận:** Tổng $10$ số hạng đầu tiên của dãy số là **$2036$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 22
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 22 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi
st.markdown(r"""
Tìm số nguyên dương $m$ nhỏ nhất sao cho biểu thức $3^{2026} + m$ chia hết cho $17$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_22 = st.text_input("Nhập giá trị m nhỏ nhất:", key="q22_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q22_check"):
    normalized_user_answer = user_answer_22.strip()
    
    # Đáp án chính xác là 9
    if normalized_user_answer == "9":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_22 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy sử dụng định lý Fermat nhỏ để xét số dư của lũy thừa nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q22_solution_shown' not in st.session_state:
    st.session_state['q22_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q22_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q22_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q22_solution_shown'] = False 

if st.session_state.get('q22_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm số dư của $3^{2026}$ khi chia cho $17$**
    
    Vì $17$ là số nguyên tố và $(3, 17) = 1$, theo định lý Fermat nhỏ, ta có:
    $$3^{16} \equiv 1 \pmod{17}$$
    
    Ta thực hiện phép chia phần mũ $2026$ cho $16$:
    $$2026 = 16 \times 126 + 10$$
    
    Do đó:
    $$3^{2026} = 3^{16 \times 126 + 10} = (3^{16})^{126} \cdot 3^{10} \equiv 1^{126} \cdot 3^{10} \equiv 3^{10} \pmod{17}$$
    
    **Bước 2: Tính số dư của $3^{10}$ modulo $17$**
    
    Ta tính lần lượt để hạ bậc:
    *   $3^2 = 9$
    *   $3^4 = 81 = 17 \times 4 + 13 \equiv 13 \equiv -4 \pmod{17}$
    *   $3^8 = (3^4)^2 \equiv (-4)^2 = 16 \equiv -1 \pmod{17}$
    
    Suy ra:
    $$3^{10} = 3^8 \cdot 3^2 \equiv (-1) \cdot 9 = -9 \equiv 8 \pmod{17}$$
    
    Vậy $3^{2026} \equiv 8 \pmod{17}$.
    
    **Bước 3: Tìm $m$ nhỏ nhất**
    
    Để $(3^{2026} + m) \vdots 17$, ta phải có:
    $$8 + m \equiv 0 \pmod{17}$$
    $$m \equiv -8 \equiv 9 \pmod{17}$$
    
    Hay $m = 17k + 9$ (với $k \in \mathbb{N}$).
    
    Vì bài toán yêu cầu tìm số nguyên dương $m$ nhỏ nhất, ta chọn $k = 0$. Khi đó:
    $$m = 9$$
    
    **Kết luận:** Giá trị nguyên dương $m$ nhỏ nhất cần tìm là **$9$**.
    """)
    
st.markdown("---")



# ==========================================
import streamlit as st

# ==========================================
# CÂU 23: TOÁN THỰC TẾ SỐ HỌC (BÀI TOÁN ĐIỀU PHỐI / ĐỊNH LÝ PHẦN DƯ TRUNG HOA)
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 23 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh / text
st.markdown(r"""
Một công ty logistics tại Hà Nội cần điều phối một số lượng lớn các container hàng hóa xuất khẩu. Người quản lý kho nhận thấy quy luật sau:
*   Nếu xếp các container lên các xe tải loại chở được $11$ chiếc/xe thì còn dư $5$ chiếc.
*   Nếu xếp các container lên các xe tải loại chở được $13$ chiếc/xe thì còn dư $8$ chiếc.
*   Nếu xếp các container lên các siêu trọng tải loại chở được $17$ chiếc/xe thì còn dư $12$ chiếc.

Biết rằng tổng số container của công ty nằm trong khoảng từ $2000$ đến $3000$ chiếc. Hãy tính chính xác số lượng container mà công ty đang có.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_23 = st.text_input("Nhập số lượng container:", key="q23_ans")



# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q23_check"):
    normalized_user_answer_23 = user_answer_23.strip()
    
    # Đáp án chính xác là 2205
    if normalized_user_answer_23 == "2205":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_23 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập hệ phương trình đồng dư và giải bằng phương pháp thế dần nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q23_solution_shown' not in st.session_state:
    st.session_state['q23_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q23_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q23_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q23_solution_shown'] = False 

if st.session_state.get('q23_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ phương trình đồng dư**
    
    Gọi $N$ là tổng số lượng container cần tìm ($2000 \le N \le 3000, N \in \mathbb{N}^*$).
    Theo bài ra, ta có hệ điều kiện đồng dư:
    $$
    \begin{cases}
    N \equiv 5 \pmod{11} \quad (1) \\
    N \equiv 8 \pmod{13} \quad (2) \\
    N \equiv 12 \pmod{17} \quad (3)
    \end{cases}
    $$
    
    **Bước 2: Giải hệ đồng dư bằng phương pháp thế**
    
    Từ phương trình $(1)$, ta có $N = 11k + 5$ ($k \in \mathbb{Z}$).
    Thế vào phương trình $(2)$:
    $$11k + 5 \equiv 8 \pmod{13}$$
    $$11k \equiv 3 \pmod{13}$$
    Nhân cả 2 vế với $6$ (vì $11 \times 6 = 66 \equiv 1 \pmod{13}$):
    $$k \equiv 3 \times 6 \equiv 18 \equiv 5 \pmod{13}$$
    Suy ra $k = 13m + 5$ ($m \in \mathbb{Z}$).
    
    Thay $k$ trở lại vào biểu thức của $N$:
    $$N = 11(13m + 5) + 5 = 143m + 60$$
    
    Tiếp tục thế vào phương trình $(3)$:
    $$143m + 60 \equiv 12 \pmod{17}$$
    Ta có $143 = 17 \times 8 + 7$, nên $143m \equiv 7m \pmod{17}$.
    $$7m + 60 \equiv 12 \pmod{17}$$
    $$7m \equiv -48 \equiv -48 + 17 \times 3 \equiv 3 \pmod{17}$$
    Nhân cả 2 vế với $5$ (vì $7 \times 5 = 35 \equiv 1 \pmod{17}$):
    $$m \equiv 3 \times 5 \equiv 15 \pmod{17}$$
    Suy ra $m = 17t + 15$ ($t \in \mathbb{Z}$).
    
    **Bước 3: Tìm công thức tổng quát và kết luận**
    
    Thay $m$ vào biểu thức của $N$:
    $$N = 143(17t + 15) + 60 = 2431t + 2145 + 60 = 2431t + 2205$$
    
    Vì số container nằm trong khoảng $2000 \le N \le 3000$:
    $$2000 \le 2431t + 2205 \le 3000$$
    $$-205 \le 2431t \le 795$$
    $$\dfrac{-205}{2431} \le t \le \dfrac{795}{2431}$$
    
    Do $t$ là số nguyên nên $t = 0$.
    Với $t = 0$, ta có:
    $$N = 2205$$
    
    **Kết luận:** Số lượng container của công ty là **$2205$** chiếc.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 24: TOÁN THỰC TẾ SỐ HỌC (BẢO MẬT/MÃ HÓA DIFFIE-HELLMAN)
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 24 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh / text
st.markdown(r"""
Trong thuật toán trao đổi khóa bảo mật thông tin trên nền tảng thi trực tuyến, khóa chung $K$ giữa máy chủ và người dùng được tính dựa trên lý thuyết số bằng công thức: 
$$K = (g^a \bmod p)^b \bmod p$$
Trong đó $p$ là một số nguyên tố, $g$ là cơ số công khai, còn $a$ và $b$ lần lượt là các khóa bí mật của người dùng và máy chủ. 
Theo tính chất của phép đồng dư, ta có $K \equiv g^{a \cdot b} \pmod p$ và $0 \le K < p$.

Giả sử hệ thống chọn số nguyên tố $p = 19$, cơ số $g = 5$. Trình duyệt của học sinh sinh ra khóa bí mật $a = 125$, và máy chủ của trường sinh ra khóa bí mật $b = 455$. 

Hãy tính giá trị khóa chung $K$ (là một số tự nhiên) mà hai bên sẽ sử dụng để mã hóa dữ liệu.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_24 = st.text_input("Nhập giá trị khóa chung K:", key="q24_ans")




# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q24_check"):
    normalized_user_answer_24 = user_answer_24.strip()
    
    # Đáp án chính xác là 17
    if normalized_user_answer_24 == "17":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_24 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy sử dụng Định lý Fermat nhỏ $g^{p-1} \equiv 1 \pmod p$ để hạ bậc lũy thừa nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q24_solution_shown' not in st.session_state:
    st.session_state['q24_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q24_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q24_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q24_solution_shown'] = False 

if st.session_state.get('q24_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích bài toán bằng lý thuyết đồng dư**
    
    Khóa chung $K$ được tính bằng:
    $$K \equiv 5^{125 \times 455} \pmod{19} \quad (\text{với } 0 \le K < 19)$$
    
    Vì $19$ là số nguyên tố và $(5, 19) = 1$, theo **Định lý Fermat nhỏ**, ta có:
    $$5^{18} \equiv 1 \pmod{19}$$
    
    Do đó, để tìm số dư của lũy thừa $5^{125 \times 455}$ cho $19$, ta cần tìm số dư của số mũ $E = 125 \times 455$ khi chia cho $18$.
    
    **Bước 2: Rút gọn số mũ**
    
    Ta xét số dư của từng thừa số trong số mũ khi chia cho $18$:
    *   $125 = 18 \times 6 + 17 \equiv 17 \equiv -1 \pmod{18}$
    *   $455 = 18 \times 25 + 5 \equiv 5 \pmod{18}$
    
    Suy ra số mũ $E$ thỏa mãn:
    $$E = 125 \times 455 \equiv (-1) \times 5 = -5 \equiv 13 \pmod{18}$$
    
    Như vậy, $E = 18k + 13$. Khi đó:
    $$5^{125 \times 455} = 5^{18k + 13} = (5^{18})^k \cdot 5^{13} \equiv 1^k \cdot 5^{13} \equiv 5^{13} \pmod{19}$$
    
    **Bước 3: Tính $5^{13} \pmod{19}$ bằng phương pháp hạ bậc**
    
    Ta tính lần lượt các lũy thừa của $5$ theo modulo $19$:
    *   $5^2 = 25 \equiv 6 \pmod{19}$
    *   $5^4 = (5^2)^2 \equiv 6^2 = 36 \equiv -2 \pmod{19}$
    *   $5^8 = (5^4)^2 \equiv (-2)^2 = 4 \pmod{19}$
    
    Phân tích số mũ $13 = 8 + 4 + 1$, ta có:
    $$5^{13} = 5^8 \cdot 5^4 \cdot 5^1 \equiv 4 \cdot (-2) \cdot 5 \pmod{19}$$
    $$5^{13} \equiv -40 \pmod{19}$$
    
    Ta thực hiện phép chia để đưa về số dư dương:
    $$-40 = 19 \times (-3) + 17 \Rightarrow -40 \equiv 17 \pmod{19}$$
    
    Vậy $5^{125 \times 455} \equiv 17 \pmod{19}$.
    
    **Kết luận:** Giá trị khóa chung cần tìm là **$K = 17$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 25
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 25 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi
st.markdown(r"""
Gọi $S$ là tập hợp các số tự nhiên có 4 chữ số đôi một khác nhau được lập từ các chữ số $0, 1, 2, 3, 4, 5, 6, 7$. Chọn ngẫu nhiên một số từ tập $S$. Biết xác suất để số được chọn chia hết cho $15$ là $\dfrac{a}{b}$ (với $a, b$ là các số nguyên dương và phân số là tối giản). 

Tính giá trị biểu thức $T = a + b$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_25 = st.text_input("Nhập giá trị của T:", key="q25_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q25_check"):
    normalized_user_answer = user_answer_25.strip()
    
    # Đáp án chính xác là 268
    if normalized_user_answer == "268":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_25 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Số chia hết cho 15 cần chia hết cho 5 và 3. Hãy chia làm 2 trường hợp: tận cùng là 0 hoặc tận cùng là 5 và phân chia các tập số dư nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q25_solution_shown' not in st.session_state:
    st.session_state['q25_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q25_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q25_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q25_solution_shown'] = False 

if st.session_state.get('q25_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính số phần tử của không gian mẫu**
    
    Số các số tự nhiên có 4 chữ số phân biệt từ $8$ chữ số đã cho là:
    $n(\Omega) = 7 \times A_7^3 = 7 \times 7 \times 6 \times 5 = 1470$ (số).
    
    **Bước 2: Phân tích điều kiện chia hết cho 15**
    
    Số được chọn $\overline{xyzt} \vdots 15 \Leftrightarrow \overline{xyzt} \vdots 5$ và $\overline{xyzt} \vdots 3$.
    Do đó tận cùng $t \in \{0, 5\}$. Chia làm hai trường hợp:
    
    *   **Trường hợp 1: $t = 0$**
        Ta cần chọn $3$ chữ số $\{x, y, z\}$ từ $\{1, 2, 3, 4, 5, 6, 7\}$ sao cho tổng của chúng chia hết cho $3$.
        Chia tập này theo module 3: 
        $G_0 = \{3, 6\}$ (có $2$ số); $G_1 = \{1, 4, 7\}$ (có $3$ số); $G_2 = \{2, 5\}$ (có $2$ số).
        Để tổng 3 chữ số chia hết cho 3, ta có các cách lấy:
        + 3 số cùng nhóm: Chỉ có thể lấy $3$ số từ $G_1$ (có $C_3^3 = 1$ bộ).
        + 3 số từ 3 nhóm khác nhau: Chọn 1 số từ mỗi nhóm, có $C_2^1 \cdot C_3^1 \cdot C_2^1 = 12$ bộ.
        Vậy có tổng cộng $1 + 12 = 13$ bộ.
        Hoán vị 3 chữ số ở các vị trí $x, y, z$, ta được: $13 \times 3! = \mathbf{78}$ số.
        
    *   **Trường hợp 2: $t = 5$**
        Ta cần chọn $3$ chữ số $\{x, y, z\}$ từ $\{0, 1, 2, 3, 4, 6, 7\}$ sao cho tổng của chúng cộng $5$ chia hết cho $3$, tức là $(x+y+z) \equiv 1 \pmod 3$.
        Chia tập này theo module 3: 
        $G_0 = \{0, 3, 6\}$ (có $3$ số); $G_1 = \{1, 4, 7\}$ (có $3$ số); $G_2 = \{2\}$ (có $1$ số).
        Để $(x+y+z) \equiv 1 \pmod 3$, ta có các cách lấy 3 phần tử:
        + 2 số từ $G_0$, 1 số từ $G_1$: Có $C_3^2 \cdot C_3^1 = 9$ bộ.
        + 2 số từ $G_1$, 1 số từ $G_2$: Có $C_3^2 \cdot C_1^1 = 3$ bộ.
        Tổng cộng có $12$ bộ. 
        Tuy nhiên cần trừ đi trường hợp chữ số $0$ đứng đầu:
        Trong 9 bộ ở nhóm đầu, các bộ chứa chữ số $0$ được tạo bởi: lấy $0$, lấy $1$ số từ $\{3, 6\}$ và $1$ số từ $\{1, 4, 7\}$ $\Rightarrow$ có $1 \times C_2^1 \times C_3^1 = 6$ bộ. 
        Đối với $6$ bộ chứa $0$ này, khi sắp xếp thành số có 3 chữ số ($x \neq 0$), có $2 \times 2! = 4$ cách lập $\Rightarrow$ được $6 \times 4 = 24$ số.
        Các bộ không chứa $0$ còn lại có $12 - 6 = 6$ bộ. Với mỗi bộ ta hoán vị tùy ý $3!$ cách $\Rightarrow$ được $6 \times 6 = 36$ số.
        Vậy ở trường hợp 2 có tất cả: $24 + 36 = \mathbf{60}$ số.
        
    **Bước 3: Tính xác suất**
    
    Tổng số các số chia hết cho 15 là: $n(A) = 78 + 60 = 138$ số.
    Xác suất là: $P(A) = \dfrac{138}{1470} = \dfrac{23}{245}$.
    
    Vì phân số $\dfrac{23}{245}$ là tối giản, nên $a = 23, b = 245$.
    Vậy $T = a + b = 23 + 245 = 268$.
    
    **Kết luận:** Giá trị cần tìm là **$268$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 26 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 26. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tính số dư khi chia tổng $S = 1^5 + 2^5 + 3^5 + \dots + 2026^5$ cho $7$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 26) ---
user_ans_26 = st.text_input("Nhập số dư của tổng S khi chia cho 7:", key="q26_ans")

if st.button("Kiểm tra đáp án Câu 26", key="q26_check"):
    norm_ans_26 = user_ans_26.strip()
    
    # Đáp án chính xác là 3
    if norm_ans_26 == "3":
        st.success("🎉 Chính xác! Bạn đã vận dụng tính chất chu kỳ số dư lũy thừa bậc cao rất xuất sắc. Lời giải Câu 26 đã được mở khóa.")
    elif user_ans_26 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 26.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy xét giá trị của $a^5 \pmod 7$ với các số dư từ $0$ đến $6$ để tìm chu kỳ lặp lại của tổng sau mỗi $7$ số hạng.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 26 ---
st.markdown("---")

if 'q26_solution_shown' not in st.session_state:
    st.session_state['q26_solution_shown'] = False

col1_26, col2_26 = st.columns([1, 4])
with col1_26:
    if st.button("Xem lời giải Câu 26", key="q26_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q26_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q26_solution_shown'] = False 

if st.session_state.get('q26_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 26 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Khảo sát tính chất chu kỳ modulo $7$ của hàm số $f(a) = a^5 \pmod 7$**
    
    Ta xét giá trị của $a^5$ khi chia cho $7$ với mọi số dư $a \in \{0, 1, 2, 3, 4, 5, 6\}$:
    *   $0^5 \equiv 0 \pmod 7$
    *   $1^5 \equiv 1 \pmod 7$
    *   $2^5 = 32 \equiv 4 \pmod 7$
    *   $3^5 = 243 \equiv 5 \pmod 7$
    *   $4^5 = 1024 \equiv 2 \pmod 7$
    *   $5^5 = 3125 \equiv 3 \pmod 7$
    *   $6^5 = 7776 \equiv 6 \pmod 7$
    
    Tổng các số dư trong một chu kỳ gồm $7$ số liên tiếp là:
    $$0 + 1 + 4 + 5 + 2 + 3 + 6 = 21 \equiv 0 \pmod 7$$
    Điều này có nghĩa là tổng của bất kỳ $7$ số hạng liên tiếp nào trong tổng $S$ đều chia hết cho $7$.
    
    **Bước 2: Phân tích số lượng số hạng của tổng $S$**
    
    Tổng $S$ có tổng cộng $2026$ số hạng (từ $1^5$ đến $2026^5$).
    Thực hiện phép chia $2026$ cho $7$:
    $$2026 = 7 \times 289 + 3$$
    
    Như vậy, tổng $S$ được chia thành $289$ nhóm, mỗi nhóm gồm $7$ số hạng liên tiếp (tổng các nhóm này chia hết cho $7$) và dư ra $3$ số hạng ở đầu nhóm tiếp theo.
    
    **Bước 3: Tính toán phần dư**
    
    Do $289$ nhóm đầu tiên đều đồng dư với $0 \pmod 7$, ta chỉ cần tính tổng của $3$ số hạng dư ra:
    $$S \equiv 1^5 + 2^5 + 3^5 \pmod 7$$
    $$S \equiv 1 + 32 + 243 = 276 \pmod 7$$
    
    Thực hiện phép chia $276$ cho $7$:
    $$276 = 7 \times 39 + 3 \implies 276 \equiv 3 \pmod 7$$
    
    **Bước 4: Kết luận**
    
    Số dư của tổng $S$ khi chia cho $7$ là $3$.
    
    ---
    **👉 Đáp số Câu 26:** `3`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 27 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 27. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số tự nhiên $N = 2026!$ (giai thừa của $2026$). Hỏi số $N$ có tận cùng bằng bao nhiêu chữ số $0$ liên tiếp tính từ phải sang trái?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 27) ---
user_ans_27 = st.text_input("Nhập số lượng chữ số 0 tận cùng:", key="q27_ans")

if st.button("Kiểm tra đáp án Câu 27", key="q27_check"):
    norm_ans_27 = user_ans_27.strip()
    
    # Đáp án chính xác là 505
    if norm_ans_27 == "505":
        st.success("🎉 Chính xác! Bạn đã nắm vững công thức Legendre để đếm số mũ thừa số nguyên tố rất tuyệt vời. Lời giải Câu 27 đã được mở khóa.")
    elif user_ans_27 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 27.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Số chữ số 0 tận cùng của $N!$ bằng số mũ của thừa số nguyên tố $5$ trong phân tích chuẩn tắc. Hãy sử dụng công thức Legendre: $v_5(N!) = \sum \left\lfloor \dfrac{N}{5^i} \right\rfloor$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 27 ---
st.markdown("---")

if 'q27_solution_shown' not in st.session_state:
    st.session_state['q27_solution_shown'] = False

col1_27, col2_27 = st.columns([1, 4])
with col1_27:
    if st.button("Xem lời giải Câu 27", key="q27_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q27_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q27_solution_shown'] = False 

if st.session_state.get('q27_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 27 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Bản chất của số chữ số $0$ tận cùng**
    
    Số chữ số $0$ tận cùng liên tiếp của một số nguyên dương chính là số lượng thừa số $10$ ($10 = 2 \times 5$) có trong phân tích ra thừa số nguyên tố của số đó. 
    Vì trong dãy từ $1$ đến $2026$, số lượng bội của $2$ luôn nhiều hơn rất nhiều so với số lượng bội của $5$, nên số chữ số $0$ tận cùng của $2026!$ sẽ được quyết định hoàn toàn bởi số mũ của thừa số nguyên tố $5$.
    
    **Bước 2: Áp dụng công thức Legendre**
    
    Số mũ của thừa số nguyên tố $p$ trong $N!$ được tính bởi công thức Legendre:
    $$v_p(N!) = \sum_{k=1}^{\infty} \left\lfloor \dfrac{N}{p^k} \right\rfloor = \left\lfloor \dfrac{N}{p} \right\rfloor + \left\lfloor \dfrac{N}{p^2} \right\rfloor + \left\lfloor \dfrac{N}{p^3} \right\rfloor + \dots$$
    
    Với $N = 2026$ và $p = 5$, ta tính các thành phần:
    *   $\left\lfloor \dfrac{2026}{5} \right\rfloor = \left\lfloor 405.2 \right\rfloor = 405$
    *   $\left\lfloor \dfrac{2026}{25} \right\rfloor = \left\lfloor 81.04 \right\rfloor = 81$
    *   $\left\lfloor \dfrac{2026}{125} \right\rfloor = \left\lfloor 16.208 \right\rfloor = 16$
    *   $\left\lfloor \dfrac{2026}{625} \right\rfloor = \left\lfloor 3.2416 \right\rfloor = 3$
    *   Các lũy thừa tiếp theo ($5^5 = 3125 > 2026$) sẽ cho phần nguyên bằng $0$.
    
    **Bước 3: Tính tổng số mũ và kết luận**
    
    Tổng số mũ của thừa số $5$ trong $2026!$ là:
    $$v_5(2026!) = 405 + 81 + 16 + 3 = 505$$
    
    Vậy số $2026!$ có tận cùng bằng $505$ chữ số $0$ liên tiếp.
    
    ---
    **👉 Đáp số Câu 27:** `505`
    """)

st.markdown("---")
