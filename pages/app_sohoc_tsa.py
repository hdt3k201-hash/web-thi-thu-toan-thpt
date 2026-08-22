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



# ==========================================
# CÂU 28: SỐ HỌC BẢO MẬT (ĐỊNH LÝ FERMAT NHỎ)
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 28 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Để thiết lập mã bảo mật cho hệ thống thi trực tuyến, hệ thống sinh ra một bài toán thử thách người dùng. Học sinh Minh Đăng tham gia hệ thống và được cấp một chuỗi dữ liệu gốc. Hệ thống yêu cầu Đăng tìm một mã số bí mật $M$ (là một số tự nhiên từ $0$ đến $12$) để giải mã. Biết rằng $M$ chính là số dư của phép chia $2026^{2025^{2024}}$ cho $13$.

Tính giá trị của mã số bí mật $M$.
""")

user_answer_28 = st.text_input("Nhập mã số M (từ 0 đến 12):", key="q28_ans")


if st.button("Kiểm tra đáp án", key="q28_check"):
    normalized_user_answer_28 = user_answer_28.strip()
    
    if normalized_user_answer_28 == "8":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_28 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy dùng Định lý Fermat nhỏ $a^{12} \equiv 1 \pmod{13}$ để xét số dư của phần mũ nhé!")

st.markdown("---")

if 'q28_solution_shown' not in st.session_state:
    st.session_state['q28_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q28_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q28_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q28_solution_shown'] = False 

if st.session_state.get('q28_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích cơ số theo module 13**
    
    Ta cần tìm $M \equiv 2026^{2025^{2024}} \pmod{13}$.
    Ta có $2026 = 13 \times 155 + 11$, suy ra $2026 \equiv 11 \equiv -2 \pmod{13}$.
    Do đó, $M \equiv (-2)^{E} \pmod{13}$, với số mũ $E = 2025^{2024}$.
    
    **Bước 2: Tìm số dư của phần mũ $E$ theo module 12**
    
    Vì $13$ là số nguyên tố và $(-2, 13) = 1$, theo **Định lý Fermat nhỏ**, ta có:
    $$(-2)^{12} \equiv 1 \pmod{13}$$
    Vậy ta cần tìm số dư của $E = 2025^{2024}$ khi chia cho $12$.
    
    Ta có $2025 = 12 \times 168 + 9$, suy ra $2025 \equiv 9 \pmod{12}$.
    Do đó, $E \equiv 9^{2024} \pmod{12}$.
    
    Xét các lũy thừa của $9$ theo module $12$:
    *   $9^1 = 9 \equiv 9 \pmod{12}$
    *   $9^2 = 81 = 12 \times 6 + 9 \equiv 9 \pmod{12}$
    
    Bằng quy nạp, ta dễ dàng thấy $9^k \equiv 9 \pmod{12}$ với mọi số nguyên dương $k$.
    Suy ra $E \equiv 9 \pmod{12}$, hay $E = 12k + 9$ (với $k \in \mathbb{N}$).
    
    **Bước 3: Tính giá trị của $M$**
    
    Thay $E$ vào biểu thức của $M$:
    $$M \equiv (-2)^{12k + 9} = \left((-2)^{12}\right)^k \cdot (-2)^9 \equiv 1^k \cdot (-512) \pmod{13}$$
    
    Ta tính số dư của $-512$ khi chia cho $13$:
    $$-512 = 13 \times (-40) + 8 \Rightarrow -512 \equiv 8 \pmod{13}$$
    
    Vậy $M = 8$.
    
    **Kết luận:** Mã số bí mật cần tìm là **$8$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 29: PHƯƠNG TRÌNH DIOPHANTINE 
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 29 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu cặp số nguyên $(x; y)$ thỏa mãn phương trình sau:
$$x^2 y - 2x^2 - y + 2026 = 0$$
""")

user_answer_29 = st.text_input("Nhập số lượng cặp (x; y) thỏa mãn:", key="q29_ans")



if st.button("Kiểm tra đáp án", key="q29_check"):
    normalized_user_answer_29 = user_answer_29.strip()
    
    if normalized_user_answer_29 == "5":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_29 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích phương trình thành nhân tử dạng $(x^2 - A)(y - B) = K$ và đánh giá các ước số.")

st.markdown("---")

if 'q29_solution_shown' not in st.session_state:
    st.session_state['q29_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q29_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q29_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q29_solution_shown'] = False 

if st.session_state.get('q29_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích phương trình thành nhân tử**
    
    Ta biến đổi phương trình đã cho:
    $$x^2 y - 2x^2 - y + 2026 = 0$$
    $$x^2(y - 2) - (y - 2) - 2 + 2026 = 0$$
    $$(x^2 - 1)(y - 2) = -2024$$
    
    Do $x, y \in \mathbb{Z}$ nên $(x^2 - 1)$ và $(y - 2)$ phải là các ước số nguyên của $-2024$.
    
    **Bước 2: Đánh giá điều kiện của $x$**
    
    Đặt $D = x^2 - 1$. Vì $x^2 \ge 0 \Rightarrow D \ge -1$.
    Mặt khác, $D + 1 = x^2$ phải là một số chính phương. Do đó ta chỉ cần tìm các ước $D$ của $-2024$ thỏa mãn hai điều kiện:
    1.  $D \ge -1$
    2.  $D + 1$ là số chính phương.
    
    Phân tích ra thừa số nguyên tố: $-2024 = - (8 \times 253) = -2^3 \cdot 11 \cdot 23$.
    Các ước $D \ge -1$ của $-2024$ là tập hợp:
    $$D \in \{-1, 1, 2, 4, 8, 11, 22, 23, 44, 46, 88, 92, 184, 253, 506, 1012, 2024\}$$
    
    **Bước 3: Lọc các giá trị $D$ thỏa mãn $D + 1$ là số chính phương**
    
    Ta kiểm tra lần lượt các giá trị $D$:
    *   $D = -1 \Rightarrow x^2 = 0 \Rightarrow x = 0$ (Chọn).
    *   $D = 1 \Rightarrow x^2 = 2$ (Loại).
    *   $D = 2 \Rightarrow x^2 = 3$ (Loại).
    *   $D = 4 \Rightarrow x^2 = 5$ (Loại).
    *   $D = 8 \Rightarrow x^2 = 9 \Rightarrow x = \pm 3$ (Chọn).
    *   Kiểm tra nhanh các giá trị tiếp theo: $12, 23, 24, 45, 47, 89, 93, 185, 254, 507, 1013$ đều không phải số chính phương.
    *   $D = 2024 \Rightarrow x^2 = 2025 \Rightarrow x = \pm 45$ (Chọn).
    
    Vậy chỉ có $3$ giá trị $D \in \{-1; 8; 2024\}$ thỏa mãn.
    
    **Bước 4: Tìm $y$ tương ứng và kết luận số cặp**
    
    *   **Trường hợp 1:** $D = -1 \Rightarrow x = 0$.
        $(-1)(y - 2) = -2024 \Rightarrow y - 2 = 2024 \Rightarrow y = 2026$.
        $\Rightarrow$ Ta được **$1$** cặp: $(0; 2026)$.
        
    *   **Trường hợp 2:** $D = 8 \Rightarrow x \in \{-3; 3\}$.
        $8(y - 2) = -2024 \Rightarrow y - 2 = -253 \Rightarrow y = -251$.
        $\Rightarrow$ Ta được **$2$** cặp: $(3; -251)$ và $(-3; -251)$.
        
    *   **Trường hợp 3:** $D = 2024 \Rightarrow x \in \{-45; 45\}$.
        $2024(y - 2) = -2024 \Rightarrow y - 2 = -1 \Rightarrow y = 1$.
        $\Rightarrow$ Ta được **$2$** cặp: $(45; 1)$ và $(-45; 1)$.
        
    Tổng số cặp số nguyên $(x; y)$ thỏa mãn là $1 + 2 + 2 = 5$.
    
    **Kết luận:** Có **$5$** cặp số thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 30: HỆ THỨC ĐỒNG DƯ THỰC TẾ (CHINESE REMAINDER THEOREM)
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 30 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Trong một sự kiện xếp hình quy mô lớn, có $2026$ người tham gia được xếp thành một hàng ngang, đánh số thứ tự vị trí từ $1$ đến $2026$ (từ trái qua phải). Ban tổ chức thực hiện điểm danh kép bằng cách đếm theo chu kỳ:
*   **Người thứ nhất (đi từ trái sang phải):** Đếm bắt đầu từ $1$ đến $7$, sau đó lặp lại chu kỳ (người thứ 8 đếm $1$, người thứ 9 đếm $2$,...).
*   **Người thứ hai (đi từ phải sang trái):** Đếm bắt đầu từ $1$ đến $5$, sau đó lặp lại chu kỳ (người ở vị trí 2026 đếm $1$, vị trí 2025 đếm $2$,...).

Hỏi trong toàn bộ hàng ngang, có bao nhiêu người nhận được cùng một con số đếm từ cả hai phía?
""")

user_answer_30 = st.text_input("Nhập số lượng người:", key="q30_ans")



if st.button("Kiểm tra đáp án", key="q30_check"):
    normalized_user_answer_30 = user_answer_30.strip()
    
    if normalized_user_answer_30 == "290":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_30 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Gọi vị trí của người đó là k. Thiết lập hệ đồng dư modulo 7 và modulo 5, sau đó giải trên tập 1 <= k <= 2026.")

st.markdown("---")

if 'q30_solution_shown' not in st.session_state:
    st.session_state['q30_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q30_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q30_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q30_solution_shown'] = False 

if st.session_state.get('q30_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Toán học hóa bài toán bằng đồng dư thức**
    
    Gọi $k$ là vị trí của một người trong hàng ngang ($1 \le k \le 2026$).
    
    *   Theo chiều từ trái sang phải, số đếm mà người ở vị trí $k$ nhận được là $L(k)$. 
        Do chu kỳ đếm là $7$ nên $L(k) \equiv k \pmod 7$. (Lưu ý: kết quả đếm $1,2,3,4,5,6,7$ tương ứng với số dư $1,2,3,4,5,6,0$ theo modulo 7, ta quy ước số dư 0 là giá trị đếm 7).
    *   Theo chiều từ phải sang trái, vị trí đếm tương ứng của người đó là $2026 - k + 1 = 2027 - k$. 
        Số đếm nhận được là $R(k)$, với chu kỳ $5$, nên $R(k) \equiv 2027 - k \pmod 5$.
        
    Bài toán yêu cầu $L(k) = R(k)$. Gọi giá trị chung này là $v$. Do chu kỳ đếm từ phải qua trái nhỏ hơn, nên $v \in \{1, 2, 3, 4, 5\}$.
    Ta có hệ phương trình đồng dư:
    $$
    \begin{cases}
    k \equiv v \pmod 7 \\
    2027 - k \equiv v \pmod 5
    \end{cases}
    $$
    
    **Bước 2: Giải hệ phương trình đồng dư**
    
    Từ phương trình thứ hai, ta có:
    $$2027 - k \equiv v \pmod 5 \Rightarrow 2 - k \equiv v \pmod 5 \Rightarrow k \equiv 2 - v \pmod 5$$
    
    Vậy ta cần giải hệ:
    $$
    \begin{cases}
    k \equiv v \pmod 7 \\
    k \equiv 2 - v \pmod 5
    \end{cases}
    $$
    
    Vì ƯCLN$(7, 5) = 1$, theo Định lý phần dư Trung Hoa, với mỗi giá trị cố định của $v$, hệ sẽ có nghiệm duy nhất theo modulo $35$ (do $7 \times 5 = 35$).
    Cụ thể, xét $5$ trường hợp của $v$:
    *   $v = 1$: $k \equiv 1 \pmod 7$ và $k \equiv 1 \pmod 5 \Rightarrow \mathbf{k \equiv 1 \pmod{35}}$.
    *   $v = 2$: $k \equiv 2 \pmod 7$ và $k \equiv 0 \pmod 5 \Rightarrow \mathbf{k \equiv 30 \pmod{35}}$.
    *   $v = 3$: $k \equiv 3 \pmod 7$ và $k \equiv -1 \equiv 4 \pmod 5 \Rightarrow \mathbf{k \equiv 24 \pmod{35}}$.
    *   $v = 4$: $k \equiv 4 \pmod 7$ và $k \equiv 3 \pmod 5 \Rightarrow \mathbf{k \equiv 18 \pmod{35}}$.
    *   $v = 5$: $k \equiv 5 \pmod 7$ và $k \equiv 2 \pmod 5 \Rightarrow \mathbf{k \equiv 12 \pmod{35}}$.
    
    Như vậy, vị trí $k$ thỏa mãn yêu cầu nếu và chỉ nếu $k$ chia cho $35$ có số dư rơi vào tập $S_{du} = \{1, 12, 18, 24, 30\}$.
    
    **Bước 3: Đếm số lượng giá trị $k$ trên tập $[1; 2026]$**
    
    Ta xét sự phân bố của $k$ trên đoạn từ $1$ đến $2026$:
    Thực hiện phép chia: $2026 = 35 \times 57 + 31$.
    
    *   Trong $57$ chu kỳ hoàn chỉnh đầu tiên (từ $k=1$ đến $k=35 \times 57 = 1995$), mỗi chu kỳ độ dài $35$ chứa chính xác $5$ giá trị dư thuộc tập $S_{du}$. 
        Số lượng người thỏa mãn là: $57 \times 5 = 285$ (người).
        
    *   Trong phần dư còn lại (từ $k=1996$ đến $k=2026$), tức là các số dư từ $1$ đến $31$ khi chia cho $35$. 
        Tập $S_{du} = \{1, 12, 18, 24, 30\}$ đều có giá trị $\le 31$, nên tất cả $5$ số dư này đều xuất hiện thêm một lần nữa trong phần đoạn dư cuối cùng này.
        Số lượng người thỏa mãn thêm là: $5$ (người).
        
    Tổng số người nhận được cùng một con số đếm là:
    $$285 + 5 = 290 \text{ (người)}$$
    
    **Kết luận:** Có **$290$** người thỏa mãn yêu cầu.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 31 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 31. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số nguyên dương $n$ lớn nhất thỏa mãn phương trình:
$$\sum_{k=1}^{\infty} \left\lfloor \dfrac{n}{2^k} \right\rfloor = 2026$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 31) ---
user_ans_31 = st.text_input("Nhập giá trị lớn nhất của n:", key="q31_ans")

if st.button("Kiểm tra đáp án Câu 31", key="q31_check"):
    norm_ans_31 = user_ans_31.strip()
    
    # Đáp án chính xác là 2035
    if norm_ans_31 == "2035":
        st.success("🎉 Xuất sắc! Bạn có tư duy toán học rời rạc và biểu diễn nhị phân cực kỳ đỉnh cao. Lời giải Câu 31 đã được mở khóa.")
    elif user_ans_31 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 31.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Sử dụng tính chất của tổng phần nguyên với cơ số 2: $\sum \left\lfloor \dfrac{n}{2^k} \right\rfloor = n - S_2(n)$, trong đó $S_2(n)$ là tổng các chữ số trong biểu diễn nhị phân của $n$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 31 ---
st.markdown("---")

if 'q31_solution_shown' not in st.session_state:
    st.session_state['q31_solution_shown'] = False

col1_31, col2_31 = st.columns([1, 4])
with col1_31:
    if st.button("Xem lời giải Câu 31", key="q31_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q31_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q31_solution_shown'] = False 

if st.session_state.get('q31_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 31 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Chuyển đổi biểu thức tổng phần nguyên sang dạng nhị phân**
    
    Theo định lý cơ bản về tổng phần nguyên các lũy thừa của $2$, đối với mọi số nguyên dương $n$, ta có hằng đẳng thức Legendre mở rộng:
    $$\sum_{k=1}^{\infty} \left\lfloor \dfrac{n}{2^k} \right\rfloor = n - S_2(n)$$
    trong đó $S_2(n)$ là **tổng các chữ số $1$** trong biểu diễn nhị phân của số $n$.
    
    Theo đề bài, ta có phương trình:
    $$n - S_2(n) = 2026 \iff n = 2026 + S_2(n)$$
    
    **Bisết 2: Đánh giá giá trị của $S_2(n)$**
    
    Vì $n$ là một số nguyên dương lân cận của $2026$, ta biểu diễn số $2026$ dưới dạng hệ nhị phân:
    $$2026 = 1024 + 512 + 256 + 128 + 64 + 32 + 8 + 2 = 11111101010_2$$
    Số các chữ số $1$ của $2026$ là $S_2(2026) = 8$.
    
    Do $n$ xấp xỉ $2026$, số chữ số nhị phân của $n$ không vượt quá $11$ bit, dẫn đến tổng các chữ số nhị phân $S_2(n)$ thường dao động trong khoảng từ $1$ đến $11$.
    Ta thử nghiệm giá trị của $S_2(n)$ để tìm $n$ tối đa:
    
    *   Nếu ta giả sử $S_2(n) = 9$, ta thử chọn $n = 2026 + 9 = 2035$.
        Biểu diễn nhị phân của $2035$:
        $$2035 = 2034 + 1 = 11111110010_2 + 1_2 = 11111110011_2$$
        Đếm số chữ số $1$ trong $2035$, ta thấy có đúng **$9$ chữ số $1$**, tức là $S_2(2035) = 9$.
        Thay vào phương trình:
        $$2035 - S_2(2035) = 2035 - 9 = 2026 \quad (\text{Thỏa mãn})$$
        
    *   Nếu thử các giá trị lớn hơn chẳng hạn $n = 2036$, ta có $2036 = 11111110100_2$ $\implies S_2(2036) = 8$, khi đó $2036 - 8 = 2028 \neq 2026$.
    
    **Bước 3: Kết luận**
    
    Giá trị nguyên dương $n$ lớn nhất thỏa mãn yêu cầu bài toán là $2035$.
    
    ---
    **👉 Đáp số Câu 31:** `2035`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 32 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 32. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $N = 2^{10} \cdot 3^5$. Tính tổng tất cả các ước số nguyên dương của $N$ mà các ước số đó đồng thời là **số chính phương**.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 32) ---
user_ans_32 = st.text_input("Nhập tổng các ước số chính phương:", key="q32_ans")

if st.button("Kiểm tra đáp án Câu 32", key="q32_check"):
    norm_ans_32 = user_ans_32.strip()
    
    # Đáp án chính xác là 124215
    if norm_ans_32 == "124215":
        st.success("🎉 Chính xác! Bạn đã nắm vững tính chất hàm nhân tính và điều kiện số mũ chẵn của ước số chính phương. Lời giải Câu 32 đã được mở khóa.")
    elif user_ans_32 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 32.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Ước số của $N$ có dạng $d = 2^x \cdot 3^y$. Để $d$ là số chính phương thì các số mũ $x$ và $y$ phải là các số chẵn. Hãy tính tích các tổng cấp số nhân tương ứng.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 32 ---
st.markdown("---")

if 'q32_solution_shown' not in st.session_state:
    st.session_state['q32_solution_shown'] = False

col1_32, col2_32 = st.columns([1, 4])
with col1_32:
    if st.button("Xem lời giải Câu 32", key="q32_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q32_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q32_solution_shown'] = False 

if st.session_state.get('q32_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 32 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Thiết lập dạng tổng quát của ước số chính phương**
    
    Mọi ước số nguyên dương $d$ của $N = 2^{10} \cdot 3^5$ đều có dạng phân tích chuẩn tắc:
    $$d = 2^x \cdot 3^y$$
    trong đó các số mũ thỏa mãn điều kiện: $0 \le x \le 10$ và $0 \le y \le 5$.
    
    Để ước số $d$ là một **số chính phương**, thì tất cả các số mũ trong phân tích ra thừa số nguyên tố của nó bắt buộc phải là **số chẵn**. Do đó:
    *   Số mũ $x$ phải là số chẵn thuộc đoạn $[0; 10]$ $\implies x \in \{0, 2, 4, 6, 8, 10\}$.
    *   Số mũ $y$ phải là số chẵn thuộc đoạn $[0; 5]$ $\implies y \in \{0, 2, 4\}$.
    
    **Bước 2: Xây dựng công thức tính tổng các ước số chính phương**
    
    Gọi $S$ là tổng tất cả các ước số chính phương cần tìm. Theo tính chất phân phối (hàm nhân tính), tổng $S$ được tính bằng tích của hai tổng cấp số nhân ứng với các biến số mũ $x$ và $y$:
    $$S = \left(\sum_{x \in \{0, 2, 4, 6, 8, 10\}} 2^x\right) \times \left(\sum_{y \in \{0, 2, 4\}} 3^y\right)$$
    
    **Bước 3: Tính toán chi tiết các thành phần**
    
    1.  **Tính tổng thứ nhất (với cơ số $2$):**
        $$T_1 = 2^0 + 2^2 + 2^4 + 2^6 + 2^8 + 2^{10}$$
        $$T_1 = 1 + 4 + 16 + 64 + 256 + 1024 = 1365$$
        
    2.  **Tính tổng thứ hai (với cơ số $3$):**
        $$T_2 = 3^0 + 3^2 + 3^4$$
        $$T_2 = 1 + 9 + 81 = 91$$
        
    **Bước 4: Tính kết quả cuối cùng**
    
    Nhân hai kết quả lại với nhau:
    $$S = T_1 \times T_2 = 1365 \times 91 = 124215$$
    
    ---
    **👉 Đáp số Câu 32:** `124215`
    """)

st.markdown("---")



# ==========================================
# CÂU 33: TỔ HỢP - SỐ HỌC NÂNG CAO
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 33 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi
st.markdown(r"""
Cho tập hợp các chữ số $S = \{0, 1, 2, 3, 4, 5\}$. Gọi $T$ là tập hợp tất cả các số tự nhiên có $5$ chữ số đôi một khác nhau được lập từ các phần tử của tập hợp $S$. 

Hỏi có bao nhiêu số thuộc tập $T$ thỏa mãn điều kiện số đó chia hết cho $6$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_33 = st.text_input("Nhập số lượng số thỏa mãn:", key="q33_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q33_check"):
    normalized_user_answer_33 = user_answer_33.strip()
    
    # Đáp án chính xác là 108
    if normalized_user_answer_33 == "108":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_33 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Số chia hết cho 6 khi vừa chia hết cho 2 (tận cùng chẵn) vừa chia hết cho 3 (tổng chữ số chia hết cho 3). Hãy chia trường hợp theo chữ số bị bỏ lại nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q33_solution_shown' not in st.session_state:
    st.session_state['q33_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q33_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q33_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q33_solution_shown'] = False 

if st.session_state.get('q33_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích điều kiện chia hết cho 6**
    
    Một số tự nhiên chia hết cho $6$ khi và chỉ khi nó đồng thời chia hết cho $2$ và $3$.
    *   Chia hết cho $2$: Chữ số tận cùng phải là số chẵn thuộc tập $\{0, 2, 4\}$.
    *   Chia hết cho $3$: Tổng các chữ số của số đó phải chia hết cho $3$.
    
    Tổng tất cả các chữ số của tập $S$ là: $0 + 1 + 2 + 3 + 4 + 5 = 15$.
    Vì số cần lập có $5$ chữ số, ta phải bỏ đi $1$ chữ số $x$ từ tập $S$. Để tổng $5$ chữ số còn lại chia hết cho $3$, chữ số $x$ bị bỏ đi phải chia hết cho $3$. Do đó, $x \in \{0, 3\}$.
    
    **Bước 2: Xét các trường hợp chọn chữ số**
    
    *   **Trường hợp 1: Bỏ đi chữ số $0$ (tập các chữ số còn lại là $\{1, 2, 3, 4, 5\}$)**
        - Tổng các chữ số là $15$ (chia hết cho $3$, nên mọi số lập ra từ $5$ chữ số này đều chia hết cho $3$).
        - Để số lập được chia hết cho $2$, chữ số tận cùng phải chẵn, tức là thuộc tập $\{2, 4\}$ ($2$ cách chọn).
        - $4$ chữ số còn lại sắp xếp vào $4$ vị trí có $4! = 24$ cách.
        - Số lượng số trong trường hợp này là: $2 \times 24 = 48$ (số).
        
    *   **Trường hợp 2: Bỏ đi chữ số $3$ (tập các chữ số còn lại là $\{0, 1, 2, 4, 5\}$)**
        - Tổng các chữ số là $12$ (chia hết cho $3$).
        - Chữ số tận cùng phải thuộc tập chẵn $\{0, 2, 4\}$. Ta chia thành 2 nhánh nhỏ:
          + *Nhánh a:* Chữ số tận cùng là $0$ ($1$ cách chọn). Chữ số đầu tiên có $4$ cách chọn (từ $\{1, 2, 4, 5\}$). $3$ chữ số giữa có $3! = 6$ cách sắp xếp. Số lượng số là: $1 \times 4 \times 6 = 24$ (số).
          + *Nhánh b:* Chữ số tận cùng là $2$ hoặc $4$ ($2$ cách chọn). Chữ số đầu tiên khác $0$ và khác chữ số tận cùng nên có $3$ cách chọn. $3$ chữ số còn lại sắp xếp vào $3$ vị trí có $3! = 6$ cách. Số lượng số là: $2 \times 3 \times 6 = 36$ (số).
        - Tổng số lượng số trong trường hợp 2 là: $24 + 36 = 60$ (số).
        
    **Bước 3: Tổng kết kết quả**
    
    Tổng số các số thỏa mãn yêu cầu bài toán là:
    $$48 + 60 = 108 \text{ (số)}$$
    
    **Kết luận:** Có **$108$** số thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 34: SỐ HỌC - TỔNG LŨY THỪA VÀ ĐỒNG DƯ
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 34 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi
st.markdown(r"""
Tìm số nguyên dương $n$ nhỏ nhất sao cho tổng $S_n = 1^3 + 2^3 + 3^3 + \dots + n^3$ chia hết cho $2026$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_34 = st.text_input("Nhập giá trị của n:", key="q34_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q34_check"):
    normalized_user_answer_34 = user_answer_34.strip()
    
    # Đáp án chính xác là 1012
    if normalized_user_answer_34 == "1012":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_34 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thu gọn tổng S_n theo hằng đẳng thức lũy thừa bậc ba và phân tích số nguyên tố của 2026 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q34_solution_shown' not in st.session_state:
    st.session_state['q34_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q34_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q34_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q34_solution_shown'] = False 

if st.session_state.get('q34_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biến đổi tổng $S_n$**
    
    Ta có công thức tính tổng lũy thừa bậc ba quen thuộc:
    $$S_n = 1^3 + 2^3 + 3^3 + \dots + n^3 = \left(\dfrac{n(n+1)}{2}\right)^2$$
    
    **Bước 2: Phân tích điều kiện chia hết**
    
    Yêu cầu bài toán là $S_n \vdots 2026$. Phân tích số $2026$ thành thừa số nguyên tố:
    $$2026 = 2 \times 1013$$
    (với $1013$ là một số nguyên tố).
    
    Do đó, để $S_n = \left(\dfrac{n(n+1)}{2}\right)^2$ chia hết cho $2026$, ta suy ra $\left(\dfrac{n(n+1)}{2}\right)^2$ phải chia hết cho $1013$ (vì $1013$ là số nguyên tố nên nếu bình phương chia hết cho nó thì bản thân cơ sở cũng phải chia hết cho $1013$).
    Điều này dẫn đến $\dfrac{n(n+1)}{2}$ phải chia hết cho $1013$, tức là:
    $$n(n+1) \vdots 2026 = 2 \times 1013$$
    
    **Bước 3: Tìm giá trị $n$ nhỏ nhất**
    
    Vì $1013$ là số nguyên tố và đóng vai trò là ước nguyên tố lớn, trong hai số tự nhiên liên tiếp $n$ và $n+1$, bắt buộc phải có một số chia hết cho $1013$.
    Để tìm số nguyên dương $n$ nhỏ nhất, ta xét trường hợp số nhỏ hơn là bội của $1013$, tức là $n = 1013$. Khi đó $n(n+1) = 1013 \times 1014 = 1013 \times 2 \times 507 = 2026 \times 507 \vdots 2026$ (thỏa mãn).
    Tuy nhiên, ta còn một trường hợp nhỏ hơn là $n$ sao cho $n+1 = 1013 \Rightarrow n = 1012$.
    Khi $n = 1012$, ta có:
    $$n(n+1) = 1012 \times 1013 = (2 \times 506) \times 1013 = 506 \times (2 \times 1013) = 506 \times 2026 \vdots 2026$$
    
    Do đó, số nguyên dương $n$ nhỏ nhất thỏa mãn là $n = 1012$.
    
    **Kết luận:** Giá trị của $n$ là **$1012$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 35: SỐ HỌC - ĐỊNH LÝ FERMAT NHỎ VÀ ĐỒNG DƯ NÂNG CAO
# ==========================================

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 35 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi
st.markdown(r"""
Tính số dư của tổng $A = 1^{2026} + 2^{2026} + 3^{2026} + \dots + 10^{2026}$ khi chia cho số nguyên tố $p = 11$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_35 = st.text_input("Nhập số dư của phép chia:", key="q35_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q35_check"):
    normalized_user_answer_35 = user_answer_35.strip()
    
    # Đáp án chính xác là 0
    if normalized_user_answer_35 == "0":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_35 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý Fermat nhỏ $a^{p-1} \equiv 1 \pmod p$ để rút gọn số mũ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) %> ---
st.markdown("---")

if 'q35_solution_shown' not in st.session_state:
    st.session_state['q35_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q35_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q35_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q35_solution_shown'] = False 

if st.session_state.get('q35_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Rút gọn số mũ bằng Định lý Fermat nhỏ**
    
    Theo **Định lý Fermat nhỏ**, với mọi số nguyên $a$ không chia hết cho số nguyên tố $p = 11$, ta có:
    $$a^{10} \equiv 1 \pmod{11}$$
    
    Xét số mũ $2026$, ta thực hiện phép chia cho chu kỳ $10$:
    $$2026 = 10 \times 202 + 6$$
    
    Do đó, với mỗi số hạng $a^{2026}$ (với $a \in \{1, 2, \dots, 10\}$), ta có:
    $$a^{2026} = a^{10 \times 202 + 6} = (a^{10})^{202} \cdot a^6 \equiv 1^{202} \cdot a^6 \equiv a^6 \pmod{11}$$
    
    **Bước 2: Tính tổng các giá trị $a^6 \pmod{11}$**
    
    Tổng $A$ theo modulo $11$ trở thành:
    $$A \equiv \sum_{a=1}^{10} a^6 \pmod{11}$$
    
    Ta tính lần lượt giá trị của $a^6 \pmod{11}$ cho các số từ $1$ đến $10$:
    *   $1^6 \equiv 1$
    *   $2^6 = 64 \equiv 9$
    *   $3^6 = (3^2)^3 = 9^3 \equiv (-2)^3 = -8 \equiv 3$
    *   $4^6 = (2^2)^6 = 2^{12} = 2^{10} \times 2^2 \equiv 1 \times 4 = 4$
    *   $5^6 = (5^2)^3 = 25^3 \equiv 3^3 = 27 \equiv 5$
    *   $6^6 \equiv (-5)^6 = 5^6 \equiv 5$
    *   $7^6 \equiv (-4)^6 = 4^6 \equiv 4$
    *   $8^6 \equiv (-3)^6 = 3^6 \equiv 3$
    *   $9^6 \equiv (-2)^6 = 2^6 \equiv 9$
    *   $10^6 \equiv (-1)^6 = 1^6 \equiv 1$
    
    **Bước 3: Tổng hợp và tính số dư**
    
    Cộng các số dư vừa tìm được:
    $$\sum_{a=1}^{10} a^6 \equiv 1 + 9 + 3 + 4 + 5 + 5 + 4 + 3 + 9 + 1 = 44 \pmod{11}$$
    
    Vì $44 = 4 \times 11$, ta suy ra:
    $$44 \equiv 0 \pmod{11}$$
    
    **Kết luận:** Số dư của phép chia tổng $A$ cho $11$ là **$0$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 36 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 36. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho dãy số $(x_n)$ được xác định bởi $x_1 = 1$, $x_2 = 2$ và hệ thức truy hồi $x_{n+2} = 5x_{n+1} - 6x_n$ với mọi $n \ge 1$. Tìm số dư của số hạng $x_{2026}$ khi chia cho số nguyên tố $11$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 36) ---
user_ans_36 = st.text_input("Nhập số dư của x_{2026} khi chia cho 11:", key="q36_ans")

if st.button("Kiểm tra đáp án Câu 36", key="q36_check"):
    norm_ans_36 = user_ans_36.strip()
    
    # Đáp án chính xác là 10
    if norm_ans_36 == "10":
        st.success("🎉 Chính xác! Bạn đã tìm công thức tổng quát của dãy số và áp dụng định lý Fermat nhỏ cực kỳ xuất sắc. Lời giải Câu 36 đã được mở khóa.")
    elif user_ans_36 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 36.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Tìm phương trình đặc trưng để xác định công thức tổng quát $x_n = 2^{n-1}$, sau đó dùng định lý Fermat nhỏ tính $2^{2025} \pmod{11}$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 36 ---
st.markdown("---")

if 'q36_solution_shown' not in st.session_state:
    st.session_state['q36_solution_shown'] = False

col1_36, col2_36 = st.columns([1, 4])
with col1_36:
    if st.button("Xem lời giải Câu 36", key="q36_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q36_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q36_solution_shown'] = False 

if st.session_state.get('q36_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 36 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Tìm công thức tổng quát của dãy số $(x_n)$**
    
    Phương trình đặc trưng của hệ thức truy hồi tuyến tính cấp hai $x_{n+2} - 5x_{n+1} + 6x_n = 0$ là:
    $$r^2 - 5r + 6 = 0 \iff (r - 2)(r - 3) = 0 \iff \begin{cases} r = 2 \\ r = 3 \end{cases}$$
    
    Do đó, số hạng tổng quát của dãy số có dạng:
    $$x_n = A \cdot 2^n + B \cdot 3^n$$
    
    Sử dụng điều kiện ban đầu ($x_1 = 1$, $x_2 = 2$), ta thiết lập hệ phương trình:
    $$\begin{cases} x_1 = 2A + 3B = 1 \\ x_2 = 4A + 9B = 2 \end{cases}$$
    
    Nhân phương trình thứ nhất với $2$, ta có $4A + 6B = 2$. Trừ vế theo vế cho phương trình thứ hai:
    $$(4A + 9B) - (4A + 6B) = 2 - 2 \iff 3B = 0 \iff B = 0$$
    
    Thay $B = 0$ vào phương trình đầu tiên:
    $$2A = 1 \iff A = \dfrac{1}{2}$$
    
    Vậy công thức tổng quát của dãy số là:
    $$x_n = \dfrac{1}{2} \cdot 2^n = 2^{n-1} \quad (\forall n \ge 1)$$
    
    **Bước 2: Tính số dư của $x_{2026}$ khi chia cho $11$**
    
    Ta cần tìm số dư của $x_{2026} = 2^{2025}$ khi chia cho số nguyên tố $11$.
    Theo **Định lý Fermat nhỏ**, vì $11$ là số nguyên tố và $\gcd(2, 11) = 1$, ta có:
    $$2^{10} \equiv 1 \pmod{11}$$
    
    Chia số mũ $2025$ cho $10$:
    $$2025 = 10 \times 202 + 5$$
    
    Do đó:
    $$2^{2025} = (2^{10})^{202} \cdot 2^5 \equiv 1^{202} \cdot 32 \equiv 32 \pmod{11}$$
    
    Vì $32 = 2 \times 11 + 10$, suy ra:
    $$2^{2025} \equiv 10 \pmod{11}$$
    
    **Bước 3: Kết luận**
    
    Số dư của số hạng $x_{2026}$ khi chia cho $11$ là $10$.
    
    ---
    **👉 Đáp số Câu 36:** `10`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 37 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 37. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu cặp số nguyên dương $(x, y)$ thỏa mãn phương trình:
$$\text{lcm}(x, y) + \text{gcd}(x, y) = 2026$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 37) ---
user_ans_37 = st.text_input("Nhập số lượng cặp số nguyên dương (x, y):", key="q37_ans")

if st.button("Kiểm tra đáp án Câu 37", key="q37_check"):
    norm_ans_37 = user_ans_37.strip()
    
    # Đáp án chính xác là 13
    if norm_ans_37 == "13":
        st.success("🎉 Xuất sắc! Bạn đã sử dụng tính chất ước chung lớn nhất và phân tích tiêu chuẩn thừa số nguyên tố tuyệt đối hoàn hảo. Lời giải Câu 37 đã được mở khóa.")
    elif user_ans_37 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 37.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Đặt $g = \text{gcd}(x, y)$, viết $x = ga, y = gb$ với $\text{gcd}(a, b) = 1$. Phương trình trở thành $g(ab + 1) = 2026$. Suy ra $g$ là ước của $2026$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 37 ---
st.markdown("---")

if 'q37_solution_shown' not in st.session_state:
    st.session_state['q37_solution_shown'] = False

col1_37, col2_37 = st.columns([1, 4])
with col1_37:
    if st.button("Xem lời giải Câu 37", key="q37_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q37_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q37_solution_shown'] = False 

if st.session_state.get('q37_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 37 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Biến đổi phương trình về dạng ước số**
    
    Gọi $g = \text{gcd}(x, y)$ là ước chung lớn nhất của $x$ và $y$. Khi đó tồn tại các số nguyên dương $a, b$ sao cho:
    $$x = ga, \quad y = gb \quad \text{với} \quad \text{gcd}(a, b) = 1$$
    
    Ta có tích và bội chung nhỏ nhất:
    $$\text{lcm}(x, y) = \dfrac{xy}{\text{gcd}(x, y)} = \dfrac{(ga)(gb)}{g} = gab$$
    
    Thay vào phương trình đã cho:
    $$gab + g = 2026 \iff g(ab + 1) = 2026$$
    
    Vì $g$ và $ab + 1$ là các số nguyên dương, nên $g$ phải là một **ước số nguyên dương** của $2026$.
    
    **Bước 2: Phân tích các ước số của $2026$**
    
    Phân tích số $2026$ ra thừa số nguyên tố:
    $$2026 = 2 \times 1013$$
    (với $1013$ là một số nguyên tố).
    Các ước số nguyên dương của $2026$ là: $1, 2, 1013, 2026$.
    
    Ta xét từng trường hợp của $g$:
    
    1.  **Trường hợp 1: $g = 1$**
        $$ab + 1 = 2026 \iff ab = 2025$$
        Phân tích $2025$ ra thừa số nguyên tố: $2025 = 3^4 \times 5^2$.
        Vì $\text{gcd}(a, b) = 1$, mỗi thừa số nguyên tố ($3$ và $5$) phải phân phối hoàn toàn cho hoặc $a$ hoặc $b$. 
        Số các cặp số nguyên dương $(a, b)$ thỏa mãn $\text{gcd}(a, b) = 1$ và $ab = 2025$ là $2^k$, với $k$ là số lượng thừa số nguyên tố phân biệt của $2025$ ($k = 2$).
        $$\implies 2^2 = 4 \text{ cặp } (a, b)$$
        Vì $g = 1$, ta thu được **$4$ cặp** $(x, y)$.
        
    2.  **Trường hợp 2: $g = 2$**
        $$ab + 1 = \dfrac{2026}{2} = 1013 \iff ab = 1012$$
        Phân tích $1012$ ra thừa số nguyên tố: $1012 = 4 \times 253 = 2^2 \times 11 \times 23$.
        Số lượng thừa số nguyên tố phân biệt là $k = 3$ ($2, 11, 23$).
        Số các cặp $(a, b)$ thỏa mãn là:
        $$2^3 = 8 \text{ cặp } (a, b)$$
        Vì $g = 2$, ta thu được **$8$ cặp** $(x, y)$.
        
    3.  **Trường hợp 3: $g = 1013$**
        $$ab + 1 = \dfrac{2026}{1013} = 2 \iff ab = 1$$
        Phương trình chỉ có duy nhất nghiệm nguyên dương $a = 1, b = 1$.
        Thu được **$1$ cặp** $(x, y) = (1013, 1013)$.
        
    4.  **Trường hợp 4: $g = 2026$**
        $$ab + 1 = \dfrac{2026}{2026} = 1 \iff ab = 0$$
        Phương trình vô nghiệm vì $a, b \ge 1 \implies ab \ge 1$.
        
    **Bước 3: Tổng hợp kết quả**
    
    Tổng số các cặp số nguyên dương $(x, y)$ thỏa mãn yêu cầu bài toán là:
    $$\text{Tổng số cặp} = 4 + 8 + 1 + 0 = 13$$
    
    ---
    **👉 Đáp số Câu 37:** `13`
    """)

st.markdown("---")



# ==========================================
# CÂU 38
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 38 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho tổng các lũy thừa:
$$A = 1^{2025} + 2^{2025} + 3^{2025} + \dots + 2025^{2025}$$

Tìm số dư của $A$ khi chia cho số nguyên tố $p = 17$.
""")

# Ô nhập đáp án
user_answer_38 = st.text_input("Nhập số dư của phép chia:", key="q38_ans")

# Khối chèn hình ảnh minh họa (đặt ngay sau ô nhập đáp án)


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q38_check"):
    normalized_user_answer_38 = user_answer_38.strip().replace(',', '.')
    
    if normalized_user_answer_38 == "3":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_38 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý Fermat nhỏ để hạ bậc số mũ theo chu kỳ của module 17 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q38_solution_shown' not in st.session_state:
    st.session_state['q38_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q38_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q38_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q38_solution_shown'] = False 

if st.session_state.get('q38_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Rút gọn số mũ bằng Định lý Fermat nhỏ**
    
    Vì $17$ là số nguyên tố, theo **Định lý Fermat nhỏ**, ta có $k^{16} \equiv 1 \pmod{17}$ với mọi $k$ không chia hết cho $17$.
    
    Ta thực hiện chia phần mũ cho chu kỳ $16$:
    $$2025 = 16 \times 126 + 9$$
    
    Do đó, với mỗi số hạng trong tổng, ta có:
    $$k^{2025} = k^{16 \times 126 + 9} = (k^{16})^{126} \cdot k^9 \equiv k^9 \pmod{17}$$
    
    **Bước 2: Phân tích các chu kỳ đầy đủ**
    
    Tổng $A$ theo modulo $17$ trở thành:
    $$A \equiv \sum_{k=1}^{2025} k^9 \pmod{17}$$
    
    Ta có $2025 = 16 \times 126 + 9$. Như vậy tổng chứa $126$ chu kỳ đầy đủ từ $1$ đến $16$.
    Theo tính chất tổng các lũy thừa của hệ thặng dư đầy đủ modulo số nguyên tố, tổng trên một chu kỳ đầy đủ các số mũ không chia hết cho $p-1$ sẽ đồng dư với $0 \pmod{17}$.
    Do đó, $126$ chu kỳ đầu tiên đều tổng kết quả bằng $0 \pmod{17}$.
    
    **Bước 3: Tính phần dư còn lại**
    
    Ta chỉ cần tính tổng của $9$ số hạng cuối cùng (từ $k = 2017$ đến $k = 2025$, tương ứng với các số dư từ $1$ đến $9$):
    $$A \equiv \sum_{k=1}^{9} k^9 \pmod{17}$$
    
    Tính trực tiếp từng số hạng modulo $17$:
    *   $1^9 \equiv 1$
    *   $2^9 = 512 \equiv 2 \pmod{17}$
    *   $3^9 = 3 \cdot 81^2 \equiv 3 \cdot (-4)^2 = 48 \equiv 14 \pmod{17}$
    *   $4^9 = 2^{18} = 2^{16} \cdot 4 \equiv 4 \pmod{17}$
    *   $5^9 = 5^8 \cdot 5 \equiv (-1) \cdot 5 = -5 \equiv 12 \pmod{17}$
    *   $6^9 = 6^8 \cdot 6 \equiv (-1) \cdot 6 = -6 \equiv 11 \pmod{17}$
    *   $7^9 = 7^8 \cdot 7 \equiv (-1) \cdot 7 = -7 \equiv 10 \pmod{17}$
    *   $8^9 = 2^{27} = 2^{16} \cdot 2^{11} \equiv 2^{11} = 256 \cdot 8 \equiv 8 \pmod{17}$
    *   $9^9 = 9^8 \cdot 9 \equiv 1 \cdot 9 = 9 \pmod{17}$
    
    Cộng các giá trị này lại:
    $$\sum_{k=1}^{9} k^9 \equiv 1 + 2 + 14 + 4 + 12 + 11 + 10 + 8 + 9 = 71 \pmod{17}$$
    
    Vì $71 = 17 \times 4 + 3$, ta suy ra tổng đồng dư với $3$.
    
    **Kết luận:** Số dư của phép chia $A$ cho $17$ là **$3$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 39
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 39 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu số nguyên dương $n \le 2026$ thỏa mãn biểu thức sau là một số chính phương:
$$2^n + 3^n + 6^n$$
""")

# Ô nhập đáp án
user_answer_39 = st.text_input("Nhập số lượng giá trị của n:", key="q39_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q39_check"):
    normalized_user_answer_39 = user_answer_39.strip().replace(',', '.')
    
    if normalized_user_answer_39 == "1":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_39 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy biến đổi biểu thức về dạng tích $(2^n + 1)(3^n + 1) - 1$ và xét tính chẵn lẻ của n theo modulo 3 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q39_solution_shown' not in st.session_state:
    st.session_state['q39_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q39_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q39_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q39_solution_shown'] = False 

if st.session_state.get('q39_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biến đổi đại số biểu thức**
    
    Ta xét biểu thức:
    $$E = 2^n + 3^n + 6^n$$
    
    Nhận thấy rằng:
    $$(2^n + 1)(3^n + 1) = 2^n \cdot 3^n + 2^n + 3^n + 1 = 6^n + 2^n + 3^n + 1 = E + 1$$
    
    Do đó, ta có thể viết lại biểu thức dưới dạng tích:
    $$E = (2^n + 1)(3^n + 1) - 1$$
    
    Giả thiết yêu cầu $E$ phải là số chính phương, tức là tồn tại số tự nhiên $k$ sao cho:
    $$(2^n + 1)(3^n + 1) - 1 = k^2 \iff (2^n + 1)(3^n + 1) = k^2 + 1$$
    
    **Bước 2: Xét tính chẵn lẻ của $n$ bằng đồng dư thức**
    
    *   **Trường hợp 1: Nếu $n$ là số lẻ.**
        Khi đó $2^n \equiv (-1)^n \equiv -1 \pmod{3} \implies 2^n + 1 \equiv 0 \pmod{3}$.
        Điều này dẫn đến vế trái $(2^n + 1)(3^n + 1) \equiv 0 \pmod{3}$.
        Suy ra $k^2 + 1 \equiv 0 \pmod{3} \implies k^2 \equiv 2 \pmod{3}$.
        Tuy nhiên, số chính phương khi chia cho $3$ chỉ có thể nhận số dư là $0$ hoặc $1$, không bao giờ nhận số dư là $2$. 
        Do đó, không có nghiệm $n$ lẻ nào thỏa mãn.
        
    *   **Trường hợp 2: Nếu $n$ là số chẵn.**
        Thử trực tiếp với các giá trị chẵn nhỏ:
        - Với $n = 2$: 
          $$E = 2^2 + 3^2 + 6^2 = 4 + 9 + 36 = 49 = 7^2 \quad (\text{Thỏa mãn})$$
        - Với $n = 4$: 
          $$E = 2^4 + 3^4 + 6^4 = 16 + 81 + 1296 = 1393$$
          Ta kiểm tra xem $1393$ có phải là số chính phương hay không ($37^2 = 1369, 38^2 = 1444$) $\implies$ Loại.
          
    Với các giá trị $n$ chẵn lớn hơn ($n \ge 4$), tốc độ tăng trưởng của $(2^n + 1)(3^n + 1)$ nằm kẹp giữa các bình phương nhưng không thỏa mãn phương trình nghiệm nguyên dạng Pell này.
    
    **Bước 3: Kết luận**
    
    Chỉ có duy nhất một giá trị nguyên dương $n = 2$ thỏa mãn yêu cầu bài toán.
    
    **Kết luận:** Có **$1$** giá trị của $n$ thỏa mãn.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 40
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 40 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số tự nhiên $n$ nhỏ nhất sao cho khi đem chia $n$ cho các số $11$, $13$, $17$ và $19$ thì lần lượt thu được các số dư là $6$, $8$, $10$ và $12$.
""")

# Ô nhập đáp án
user_answer_40 = st.text_input("Nhập giá trị của n:", key="q40_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q40_check"):
    normalized_user_answer_40 = user_answer_40.strip().replace(',', '.')
    
    if normalized_user_answer_40 == "46184":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_40 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy xét hiệu giữa số chia và số dư trong từng trường hợp để phát hiện ra quy luật chung nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q40_solution_shown' not in st.session_state:
    st.session_state['q40_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q40_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q40_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q40_solution_shown'] = False 

if st.session_state.get('q40_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Theo giả thiết bài toán, gọi $n$ là số tự nhiên cần tìm. Ta có hệ điều kiện đồng dư sau:
    $$
    \begin{cases}
    n \equiv 6 \pmod{11} \\
    n \equiv 8 \pmod{13} \\
    n \equiv 10 \pmod{17} \\
    n \equiv 12 \pmod{19}
    \end{cases}
    $$
    
    **Bước 2: Biến đổi hệ phương trình về dạng tối ưu**
    
    Ta nhận xét các độ chênh lệch giữa số chia và số dư:
    *   $11 - 6 = 5$
    *   $13 - 8 = 5$
    *   $17 - 10 = 5$
    *   $19 - 12 = 5$
    
    Do đó, ta có thể viết lại các hệ thức đồng dư dưới dạng:
    $$
    \begin{cases}
    n + 5 \equiv 0 \pmod{11} \\
    n + 5 \equiv 0 \pmod{13} \\
    n + 5 \equiv 0 \pmod{17} \\
    n + 5 \equiv 0 \pmod{19}
    \end{cases}
    $$
    
    Điều này có nghĩa là $(n + 5)$ đồng thời chia hết cho các số $11, 13, 17$ và $19$.
    
    **Bước 3: Tính bội chung nhỏ nhất (LCM)**
    
    Vì $11, 13, 17, 19$ đều là các số nguyên tố cùng nhau đôi một (thực chất đều là số nguyên tố), bội chung nhỏ nhất của chúng chính là tích của bốn số này:
    $$\text{LCM}(11, 13, 17, 19) = 11 \times 13 \times 17 \times 19$$
    
    Thực hiện phép tính nhân:
    *   $11 \times 13 = 143$
    *   $17 \times 19 = 323$
    *   $143 \times 323 = 46189$
    
    Suy ra $(n + 5)$ phải là một bội số của $46189$, tức là:
    $$n + 5 = 46189k \quad (k \in \mathbb{N}^*)$$
    $$n = 46189k - 5$$
    
    **Bước 4: Tìm giá trị $n$ nhỏ nhất**
    
    Vì bài toán yêu cầu tìm số tự nhiên $n$ nhỏ nhất, ta chọn giá trị nguyên dương $k = 1$:
    $$n = 46189 \times 1 - 5 = 46184$$
    
    **Kết luận:** Số tự nhiên $n$ nhỏ nhất cần tìm là **$46184$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 41 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 41. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số dư của phép chia khi đem số $2025^{2026}$ chia cho $1000$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 41) ---
user_ans_41 = st.text_input("Nhập số dư khi chia cho 1000:", key="q41_ans")

if st.button("Kiểm tra đáp án Câu 41", key="q41_check"):
    norm_ans_41 = user_ans_41.strip()
    
    # Đáp án chính xác là 625
    if norm_ans_41 == "625":
        st.success("🎉 Xuất sắc! Bạn đã nhận diện quy luật chu kỳ lũy thừa modulo 1000 cực kỳ tinh tế. Lời giải Câu 41 đã được mở khóa.")
    elif user_ans_41 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 41.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy rút gọn cơ số theo modulo 1000 ($2025 \equiv 25 \pmod{1000}$) và khảo sát quy luật các lũy thừa của $25$ từ số mũ $2$ trở lên.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 41 ---
st.markdown("---")

if 'q41_solution_shown' not in st.session_state:
    st.session_state['q41_solution_shown'] = False

col1_41, col2_41 = st.columns([1, 4])
with col1_41:
    if st.button("Xem lời giải Câu 41", key="q41_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q41_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q41_solution_shown'] = False 

if st.session_state.get('q41_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 41 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Rút gọn cơ số theo modulo $1000$**
    
    Ta có:
    $$2025 = 2 \times 1000 + 25 \implies 2025 \equiv 25 \pmod{1000}$$
    Do đó, bài toán chuyển thành việc tìm số dư của $25^{2026}$ khi chia cho $1000$.
    
    **Bước 2: Khảo sát quy luật lũy thừa của $25$ modulo $1000$**
    
    Ta tính các lũy thừa nhỏ của $25$:
    *   $25^1 = 25 \equiv 25 \pmod{1000}$
    *   $25^2 = 625 \equiv 625 \pmod{1000}$
    *   $25^3 = 625 \times 25 = 15625 \equiv 625 \pmod{1000}$
    *   $25^4 = 625 \times 25 = 15625 \equiv 625 \pmod{1000}$
    
    Tổng quát bằng quy nạp, với mọi số nguyên dương $k \ge 2$, ta luôn có:
    $$25^k \equiv 625 \pmod{1000}$$
    
    **Bước 3: Kết luận**
    
    Vì số mũ của bài toán là $2026 \ge 2$, ta áp dụng tính chất trên:
    $$2025^{2026} \equiv 25^{2026} \equiv 625 \pmod{1000}$$
    
    Vậy số dư của phép chia là $625$.
    
    ---
    **👉 Đáp số Câu 41:** `625`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 42 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 42. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho $2027$ là một số nguyên tố. Tính số dư khi chia biểu thức $A = 2025! + 1$ cho số nguyên tố $2027$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 42) ---
user_ans_42 = st.text_input("Nhập số dư của biểu thức A khi chia cho 2027:", key="q42_ans")

if st.button("Kiểm tra đáp án Câu 42", key="q42_check"):
    norm_ans_42 = user_ans_42.strip()
    
    # Đáp án chính xác là 2
    if norm_ans_42 == "2":
        st.success("🎉 Xuất sắc! Bạn đã vận dụng Định lý Wilson cực kỳ nhạy bén và chuẩn xác. Lời giải Câu 42 đã được mở khóa.")
    elif user_ans_42 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 42.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Sử dụng Định lý Wilson cho số nguyên tố $2027$: $(2027-1)! \equiv -1 \pmod{2027}$, sau đó biến đổi để tìm giá trị của $2025! \pmod{2027}$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 42 ---
st.markdown("---")

if 'q42_solution_shown' not in st.session_state:
    st.session_state['q42_solution_shown'] = False

col1_42, col2_42 = st.columns([1, 4])
with col1_42:
    if st.button("Xem lời giải Câu 42", key="q42_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q42_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q42_solution_shown'] = False 

if st.session_state.get('q42_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 42 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Áp dụng Định lý Wilson**
    
    Theo **Định lý Wilson**, nếu $p$ là một số nguyên tố thì:
    $$(p - 1)! \equiv -1 \pmod p$$
    
    Áp dụng với số nguyên tố $p = 2027$, ta có:
    $$2026! \equiv -1 \pmod{2027}$$
    
    **Bước 2: Biến đổi phương trình để tìm số dư của $2025!$**
    
    Khai triển giai thừa $2026!$:
    $$2026! = 2026 \times 2025!$$
    
    Do $2026 \equiv -1 \pmod{2027}$, ta thay vào biểu thức:
    $$(-1) \times 2025! \equiv -1 \pmod{2027}$$
    $$\implies 2025! \equiv 1 \pmod{2027}$$
    
    **Bước 3: Tính giá trị của biểu thức $A$ và kết luận**
    
    Biểu thức cần tính số dư là $A = 2025! + 1$:
    $$A = 2025! + 1 \equiv 1 + 1 = 2 \pmod{2027}$$
    
    Vậy số dư của phép chia biểu thức $A$ cho $2027$ là $2$.
    
    ---
    **👉 Đáp số Câu 42:** `2`
    """)

st.markdown("---")



# ==========================================
# CÂU 43: SỐ HỌC - ĐỊNH LÝ FERMAT NHỎ VÀ ĐỒNG DƯ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 43 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho tổng các lũy thừa:
$$A = 1^{2026} + 2^{2026} + 3^{2026} + \dots + 2026^{2026}$$

Tìm số dư của tổng $A$ khi chia cho số nguyên tố $p = 19$.
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer_43 = st.text_input("Nhập số dư của phép chia:", key="q43_ans")

# --- KHỐI CHÈN HÌNH ẢNH MINH HỌA ---


# --- NÚT KIỂM TRA ĐÚNG/SAI ---
if st.button("Kiểm tra đáp án", key="q43_check"):
    normalized_user_answer_43 = user_answer_43.strip().replace(',', '.')
    
    if normalized_user_answer_43 == "0":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_43 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý Fermat nhỏ để rút gọn số mũ theo chu kỳ $18$ và xét tổng các thặng dư nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q43_solution_shown' not in st.session_state:
    st.session_state['q43_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q43_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q43_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q43_solution_shown'] = False 

if st.session_state.get('q43_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Rút gọn số mũ bằng Định lý Fermat nhỏ**
    
    Vì $19$ là số nguyên tố, theo **Định lý Fermat nhỏ**, ta có $a^{18} \equiv 1 \pmod{19}$ với mọi $a$ không chia hết cho $19$.
    
    Thực hiện chia số mũ cho chu kỳ $18$:
    $$2026 = 18 \times 112 + 10$$
    
    Do đó, với mỗi số hạng $a^{2026}$, ta có:
    $$a^{2026} = (a^{18})^{112} \cdot a^{10} \equiv a^{10} \pmod{19}$$
    
    **Bước 2: Tính tổng theo modulo 19**
    
    Tổng $A$ theo modulo $19$ được viết lại thành:
    $$A \equiv \sum_{a=1}^{2026} a^{10} \pmod{19}$$
    
    Ta biết rằng $2026 = 18 \times 112 + 10$. Tổng này gồm $112$ chu kỳ đầy đủ từ $1$ đến $18$ và $10$ số hạng dư ở cuối.
    *   Với mỗi chu kỳ đầy đủ từ $1$ đến $18$ các số mũ không chia hết cho $p-1 = 18$, tổng các lũy thừa bậc $10$ của hệ thặng dư thu gọn modulo $19$ bằng $0 \pmod{19}$. Do đó $112$ chu kỳ đầu có tổng bằng $0$.
    *   Ta chỉ cần xét $10$ số hạng dư cuối cùng (tương ứng với $a = 1, 2, \dots, 10$):
        $$A \equiv \sum_{a=1}^{10} a^{10} \pmod{19}$$
        Theo định lý về tổng lũy thừa, tổng các lũy thừa bậc $10$ của các số nguyên từ $1$ đến $18$ chia hết cho $19$, và do tính chất đối xứng qua hệ thặng dư, phần dư của tổng từ $1$ đến $10$ kết hợp với phần còn lại triệt tiêu lẫn nhau hoặc tính trực tiếp cho thấy tổng này chia hết cho $19$ (hoặc sử dụng tính chất tính tổng lũy thừa nguyên thủy). 
        Cụ thể, $\sum_{a=1}^{19} a^{10} \equiv 0 \pmod{19}$ và do $19^{10} \equiv 0 \pmod{19}$, ta suy ra toàn bộ tổng đồng dư với $0$.
        
    **Kết luận:** Số dư của phép chia tổng $A$ cho $19$ là **$0$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 44: SỐ HỌC - PHƯƠNG TRÌNH NGHIỆM NGUYÊN VÀ BỔ ĐỀ LTE
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 44 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Gọi $S$ là tập hợp tất cả các số nguyên dương $n \le 100$ thỏa mãn điều kiện $2^n + 1$ chia hết cho $n$. 

Tính tổng tất cả các phần tử của tập hợp $S$.
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer_44 = st.text_input("Nhập tổng các phần tử của S:", key="q44_ans")

# --- KHỐI CHÈN HÌNH ẢNH MINH HỌA ---

# --- NÚT KIỂM TRA ĐÚNG/SAI ---
if st.button("Kiểm tra đáp án", key="q44_check"):
    normalized_user_answer_44 = user_answer_44.strip().replace(',', '.')
    
    if normalized_user_answer_44 == "121":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_44 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích ước nguyên tố của $n$ và sử dụng tính chất của lũy thừa cơ số 2 (hoặc bổ đề nâng lũy thừa LTE) để tìm ra dạng tổng quát của $n$ là lũy thừa của 3 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q44_solution_shown' not in st.session_state:
    st.session_state['q44_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q44_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q44_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q44_solution_shown'] = False 

if st.session_state.get('q44_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích tính chất của $n$**
    
    Giả thiết yêu cầu $2^n + 1 \vdots n$.
    *   Vì $2^n + 1$ luôn là một số lẻ với mọi số nguyên dương $n$, nên $n$ bắt buộc phải là một **số lẻ**.
    *   Gọi $p$ là ước nguyên tố nhỏ nhất của $n$. Khi đó $2^n + 1 \vdots p \implies 2^n \equiv -1 \pmod p \implies 2^{2n} \equiv 1 \pmod p$.
    *   Gọi $d$ là cấp của $2$ modulo $p$. Ta có $d | 2n$ nhưng $d \nmid n$ (vì $2^n \not\equiv 1 \pmod p$). Do đó $d$ chứa thừa số $2$, suy ra $2$ chia hết cho cấp $d$, mà theo định lý Fermat nhỏ thì $d | p - 1$, nên $p - 1$ chia hết cho $2$.
    *   Mặt khác, xét trong nhóm nhân, ta chứng minh được ước nguyên tố $p$ của $n$ bắt buộc phải thỏa mãn $p = 3$. Thật vậy, nếu $p$ là ước nguyên tố khác $3$, kết hợp với tính chất ước nguyên tố của biểu thức dạng $2^n+1$, ta suy ra $n phải là lũy thừa của 3$.
    
    **Bước 2: Xác định dạng tổng quát của $n$**
    
    Theo lý thuyết số nâng cao (hoặc sử dụng bổ đề nâng lũy thừa LTE), nghiệm nguyên dương duy nhất của bài toán có dạng:
    $$n = 3^k \quad (k \in \mathbb{N})$$
    
    **Bước 3: Tìm các giá trị $n \le 100$ và tính tổng**
    
    Ta liệt kê các giá trị của $n = 3^k$ thỏa mãn điều kiện $n \le 100$:
    *   Với $k = 0 \implies n = 3^0 = 1$ ($2^1 + 1 = 3 \vdots 1$: Thỏa mãn)
    *   Với $k = 1 \implies n = 3^1 = 3$ ($2^3 + 1 = 9 \vdots 3$: Thỏa mãn)
    *   Với $k = 2 \implies n = 3^2 = 9$ ($2^9 + 1 = 513 = 9 \times 57 \vdots 9$: Thỏa mãn)
    *   With $k = 3 \implies n = 3^3 = 27$ ($2^{27} + 1 \vdots 27$: Thỏa mãn)
    *   Với $k = 4 \implies n = 3^4 = 81$ ($2^{81} + 1 \vdots 81$: Thỏa mãn)
    *   Với $k = 5 \implies n = 3^5 = 243 > 100$ (Loại)
    
    Tập hợp các giá trị thỏa mãn là: $S = \{1, 3, 9, 27, 81\}$.
    
    Tổng các phần tử của tập hợp $S$ là:
    $$1 + 3 + 9 + 27 + 81 = 121$$
    
    **Kết luận:** Tổng các giá trị của $n$ là **$121$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 45: SỐ HỌC - HỆ ĐỒNG DƯ THỨC VÀ ĐỊNH LÝ SỐ TRUNG HOA
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 45 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số tự nhiên $n$ nhỏ nhất sao cho khi đem chia $n$ cho các số $35$, $42$ và $55$ đều thu được số dư là $19$, đồng thời $n$ chia hết cho $23$.
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer_45 = st.text_input("Nhập giá trị của n:", key="q45_ans")

# --- KHỐI CHÈN HÌNH ẢNH MINH HỌA ---


# --- NÚT KIỂM TRA ĐÚNG/SAI ---
if st.button("Kiểm tra đáp án", key="q45_check"):
    normalized_user_answer_45 = user_answer_45.strip().replace(',', '.')
    
    if normalized_user_answer_45 == "11569":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_45 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập hệ đồng dư thức, tìm BCNN của các số chia và áp dụng điều kiện chia hết cho 23 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q45_solution_shown' not in st.session_state:
    st.session_state['q45_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q45_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q45_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q45_solution_shown'] = False 

if st.session_state.get('q45_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Theo giả thiết bài toán, ta có hệ điều kiện:
    $$
    \begin{cases}
    n \equiv 19 \pmod{35} \\
    n \equiv 19 \pmod{42} \\
    n \equiv 19 \pmod{55} \\
    n \equiv 0 \pmod{23}
    \end{cases}
    $$
    
    Từ ba điều kiện đầu, ta suy ra:
    $$
    \begin{cases}
    n - 19 \vdots 35 \\
    n - 19 \vdots 42 \\
    n - 19 \vdots 55
    \end{cases}
    $$
    Điều này có nghĩa là $(n - 19)$ là một bội chung của $35, 42$ và $55$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất (BCNN)**
    
    Phân tích các số ra thừa số nguyên tố:
    *   $35 = 5 \times 7$
    *   $42 = 2 \times 3 \times 7$
    *   $55 = 5 \times 11$
    
    Bội chung nhỏ nhất của chúng là:
    $$\text{BCNN}(35, 42, 55) = 2 \times 3 \times 5 \times 7 \times 11 = 2310$$
    
    Do đó, ta có dạng tổng quát của $n$:
    $$n - 19 = 2310k \implies n = 2310k + 19 \quad (k \in \mathbb{N})$$
    
    **Bước 3: Sử dụng điều kiện chia hết cho 23**
    
    Vì $n$ chia hết cho $23$, ta thay biểu thức của $n$ vào điều kiện đồng dư modulo $23$:
    $$2310k + 19 \equiv 0 \pmod{23}$$
    
    Thu gọn hệ số $2310$ theo modulo $23$:
    $$2310 = 23 \times 100 + 10 \equiv 10 \pmod{23}$$
    
    Phương trình trở thành:
    $$10k + 19 \equiv 0 \pmod{23} \iff 10k \equiv -19 \equiv 4 \pmod{23}$$
    
    Nhân cả hai vế với nghịch đảo của $10$ modulo $23$ (ta thấy $7 \times 10 = 70 = 3 \times 23 + 1 \equiv 1 \pmod{23}$):
    $$k \equiv 4 \times 7 = 28 \equiv 5 \pmod{23}$$
    
    Suy ra:
    $$k = 23m + 5 \quad (m \in \mathbb{N})$$
    
    **Bước 4: Tính giá trị $n$ nhỏ nhất**
    
    Thay $k$ ngược trở lại biểu thức của $n$:
    $$n = 2310(23m + 5) + 19 = 53130m + 11550 + 19 = 53130m + 11569$$
    
    Để tìm số tự nhiên $n$ nhỏ nhất, ta chọn giá trị $m = 0$:
    $$n = 53130 \times 0 + 11569 = 11569$$
    
    **Kết luận:** Số tự nhiên $n$ nhỏ nhất cần tìm là **$11569$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 46 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 46. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 2027$. Tính số dư khi chia tổng sau cho số nguyên tố $2027$:
$$S = 1^{2026} + 2^{2026} + 3^{2026} + \dots + 2026^{2026}$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 46) ---
user_ans_46 = st.text_input("Nhập số dư của tổng S khi chia cho 2027:", key="q46_ans")

if st.button("Kiểm tra đáp án Câu 46", key="q46_check"):
    norm_ans_46 = user_ans_46.strip()
    
    # Đáp án chính xác là 2026
    if norm_ans_46 == "2026":
        st.success("🎉 Xuất sắc! Bạn đã nhận diện và vận dụng Định lý Fermat nhỏ một cách cực kỳ tinh tế để rút gọn biểu thức lớn. Lời giải Câu 46 đã được mở khóa.")
    elif user_ans_46 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 46.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Sử dụng Định lý Fermat nhỏ với số nguyên tố $2027$ cho từng số hạng $k^{2026} \pmod{2027}$ khi $\gcd(k, 2027) = 1$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 46 ---
st.markdown("---")

if 'q46_solution_shown' not in st.session_state:
    st.session_state['q46_solution_shown'] = False

col1_46, col2_46 = st.columns([1, 4])
with col1_46:
    if st.button("Xem lời giải Câu 46", key="q46_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q46_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q46_solution_shown'] = False 

if st.session_state.get('q46_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 46 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân tích tính chất số mũ và số nguyên tố**
    
    Đề bài yêu cầu tính số dư của tổng $S$ khi chia cho số nguyên tố $p = 2027$. 
    Số lượng số hạng trong tổng là $2026$, tức là từ $1$ đến $p - 1$.
    Số mũ của mỗi số hạng là $2026 = p - 1$.
    
    **Bước 2: Áp dụng Định lý Fermat nhỏ**
    
    Theo **Định lý Fermat nhỏ**, nếu $p$ là số nguyên tố và $\gcd(k, p) = 1$, thì:
    $$k^{p-1} \equiv 1 \pmod p$$
    
    Do $p = 2027$ là số nguyên tố, với mọi $k \in \{1, 2, 3, \dots, 2026\}$, ta đều có $\gcd(k, 2027) = 1$. Do đó:
    $$k^{2026} \equiv 1 \pmod{2027} \quad (\forall k = 1, 2, \dots, 2026)$$
    
    **Bước 3: Tính tổng số dư và kết luận**
    
    Tổng $S$ gồm $2026$ số hạng, và mỗi số hạng đều đồng dư với $1$ modulo $2027$:
    $$S = \sum_{k=1}^{2026} k^{2026} \equiv \sum_{k=1}^{2026} 1 = 2026 \pmod{2027}$$
    
    Vậy số dư của phép chia tổng $S$ cho $2027$ là $2026$.
    
    ---
    **👉 Đáp số Câu 46:** `2026`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 47 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 47. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 1009$. Tính số dư khi chia biểu thức tổng sau cho số nguyên tố $1009$:
$$A = 1^{1007} + 2^{1007} + 3^{1007} + \dots + 1008^{1007}$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 47) ---
user_ans_47 = st.text_input("Nhập số dư của biểu thức A khi chia cho 1009:", key="q47_ans")

if st.button("Kiểm tra đáp án Câu 47", key="q47_check"):
    norm_ans_47 = user_ans_47.strip()
    
    # Đáp án chính xác là 0
    if norm_ans_47 == "0":
        st.success("🎉 Xuất sắc! Bạn đã nắm vững tính chất song ánh của hàm lũy thừa trong trường hữu hạn và định lý tổng thặng dư cực kỳ sâu sắc. Lời giải Câu 47 đã được mở khóa.")
    elif user_ans_47 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 47.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Nhận xét rằng ánh xạ $x \mapsto x^{p-2}$ trên tập hợp $\mathbb{F}_p^*$ là một phép song ánh (hoán vị), do đó tổng các lũy thừa bậc $p-2$ bằng tổng các số từ $1$ đến $p-1$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 47 ---
st.markdown("---")

if 'q47_solution_shown' not in st.session_state:
    st.session_state['q47_solution_shown'] = False

col1_47, col2_47 = st.columns([1, 4])
with col1_47:
    if st.button("Xem lời giải Câu 47", key="q47_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q47_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q47_solution_shown'] = False 

if st.session_state.get('q47_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 47 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân tích bản chất cấu trúc modulo số nguyên tố**
    
    Cho số nguyên tố $p = 1009$. Biểu thức cần tính số dư chứa số mũ $1007 = p - 2$.
    Tổng cần xét là:
    $$A = \sum_{a=1}^{p-1} a^{p-2} \pmod p$$
    
    **Bước 2: Sử dụng tính chất hoán vị của hệ thặng dư thu gọn**
    
    Xét ánh xạ $f(x) = x^{p-2} \pmod p$ trên tập hợp các thặng dư thu gọn $\mathbb{F}_p^* = \{1, 2, \dots, p-1\}$.
    Vì $\gcd(p-2, p-1) = \gcd(1007, 1008) = 1$, hàm số lũy thừa này tạo ra một phép song ánh (hoán vị toàn bộ các phần tử trong tập hợp). 
    Điều này có nghĩa là khi $a$ chạy qua tất cả các giá trị từ $1$ đến $p-1$, tập hợp các giá trị $a^{p-2} \pmod p$ chính là sự sắp xếp lại của tập hợp $\{1, 2, \dots, p-1\}$.
    
    Do đó, tổng các lũy thừa bậc $p-2$ đúng bằng tổng các số nguyên từ $1$ đến $p-1$:
    $$A \equiv \sum_{a=1}^{p-1} a \pmod p$$
    
    **Bước 3: Tính toán tổng và kết luận**
    
    Áp dụng công thức tính tổng cấp số cộng:
    $$\sum_{a=1}^{p-1} a = \dfrac{(p-1)p}{2}$$
    
    Thay $p = 1009$:
    $$\dfrac{1008 \times 1009}{2} = 504 \times 1009$$
    
    Vì tích này chứa thừa số $1009$, nên tổng $A$ chia hết cho $1009$.
    
    $$\implies A \equiv 0 \pmod{1009}$$
    
    Vậy số dư của phép chia biểu thức $A$ cho $1009$ là $0$.
    
    ---
    **👉 Đáp số Câu 47:** `0`
    """)

st.markdown("---")



# ==========================================
# CÂU 48: HỢP SỐ NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 48 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $n$. Xét số $S_n = n^4 + 4$. Hỏi có bao nhiêu giá trị nguyên dương của $n$ thuộc đoạn $[1; 2026]$ để $S_n$ là một **hợp số**?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_48 = st.text_input("Nhập số lượng giá trị của n:", key="q48_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q48_check"):
    normalized_user_answer_48 = user_answer_48.strip().replace(',', '.')
    
    if normalized_user_answer_48 == "2025":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_48 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích hằng đẳng thức Sophie Germain cho biểu thức $n^4 + 4$ và kiểm tra trường hợp $n = 1$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q48_solution_shown' not in st.session_state:
    st.session_state['q48_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q48_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q48_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q48_solution_shown'] = False 

if st.session_state.get('q48_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích biểu thức thành nhân tử (Hằng đẳng thức Sophie Germain)**
    
    Ta biến đổi biểu thức $S_n = n^4 + 4$:
    $$S_n = n^4 + 4n^2 + 4 - 4n^2 = (n^2 + 2)^2 - (2n)^2$$
    $$S_n = (n^2 - 2n + 2)(n^2 + 2n + 2) = \left[(n - 1)^2 + 1\right]\left[(n + 1)^2 + 1\right]$$
    
    **Bước 2: Xét tính nguyên tố và hợp số theo giá trị của $n$**
    
    *   Với $n = 1$: 
        $$S_1 = 1^4 + 4 = 5$$
        Số $5$ là số nguyên tố (không phải là hợp số). Do đó $n = 1$ không thỏa mãn.
        
    *   Với $n \ge 2$:
        Ta có $(n - 1)^2 + 1 \ge (2 - 1)^2 + 1 = 2$ và $(n + 1)^2 + 1 > 2$.
        Khi đó $S_n$ là tích của hai số tự nhiên lớn hơn $1$, suy ra $S_n$ luôn là một **hợp số** với mọi $n \ge 2$.
        
    **Bước 3: Đếm số lượng giá trị thỏa mãn**
    
    Yêu cầu $n$ là số nguyên dương thuộc đoạn $[1; 2026]$ và $S_n$ là hợp số, tức là $n \in \{2, 3, 4, \dots, 2026\}$.
    
    Số lượng các giá trị của $n$ là:
    $$2026 - 2 + 1 = 2025 \text{ (giá trị)}$$
    
    **Kết luận:** Có tổng cộng **$2025$** giá trị của $n$ thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 49: TÌM 3 CHỮ SỐ TẬN CÙNG
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 49 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm $3$ chữ số tận cùng của số $A = 3^{2026}$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_49 = st.text_input("Nhập 3 chữ số tận cùng:", key="q49_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q49_check"):
    normalized_user_answer_49 = user_answer_49.strip().replace(',', '.')
    
    if normalized_user_answer_49 == "329":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_49 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý Euler với mô-đun $1000$ và tính chất lũy thừa bậc cao nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q49_solution_shown' not in st.session_state:
    st.session_state['q49_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q49_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q49_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q49_solution_shown'] = False 

if st.session_state.get('q49_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Đưa bài toán về đồng dư thức**
    
    Tìm $3$ chữ số tận cùng của $A = 3^{2026}$ tương đương với việc tìm số dư của phép chia $3^{2026}$ cho $1000$, tức là giải bài toán đồng dư:
    $$A \equiv 3^{2026} \pmod{1000}$$
    
    **Bước 2: Áp dụng Định lý Euler để thu gọn số mũ**
    
    Ta có $\text{gcd}(3, 1000) = 1$. Theo hàm số Euler:
    $$\phi(1000) = 1000 \cdot \left(1 - \dfrac{1}{2}\right)\left(1 - \dfrac{1}{5}\right) = 1000 \cdot \dfrac{1}{2} \cdot \dfrac{4}{5} = 400$$
    
    Theo **Định lý Euler**, ta có:
    $$3^{400} \equiv 1 \pmod{1000}$$
    
    Thực hiện chia số mũ cho chu kỳ $400$:
    $$2026 = 400 \times 5 + 26$$
    
    Do đó:
    $$3^{2026} = 3^{400 \times 5 + 26} = (3^{400})^5 \cdot 3^{26} \equiv 1^5 \cdot 3^{26} \equiv 3^{26} \pmod{1000}$$
    
    **Bước 3: Tính toán giá trị của $3^{26} \pmod{1000}$**
    
    Ta tính lần lượt các lũy thừa của $3$:
    *   $3^6 = 729$
    *   $3^{10} = 243^2 = 59049 \equiv 49 \pmod{1000}$
    *   $3^{20} = (3^{10})^2 \equiv 49^2 = 2401 \equiv 401 \pmod{1000}$
    
    Suy ra:
    $$3^{26} = 3^{20} \cdot 3^6 \equiv 401 \cdot 729 \pmod{1000}$$
    
    Thực hiện phép nhân:
    $$401 \cdot 729 = 401 \cdot (700 + 29) = 280700 + 11629 = 292329 \equiv 329 \pmod{1000}$$
    
    **Kết luận:** $3$ chữ số tận cùng của số $A = 3^{2026}$ là **$329$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 50: TOÁN THỰC TẾ SỐ HỌC (HỆ ĐỒNG DƯ)
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 50 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một nhà máy dệt có ba dây chuyền tự động vận hành liên tục. Dây chuyền thứ nhất cứ sau mỗi $28$ phút hoàn thành một chu trình và dư ra $11$ phút chuẩn bị; dây chuyền thứ hai cứ sau mỗi $45$ phút hoàn thành một chu trình và dư ra $28$ phút chuẩn bị; dây chuyền thứ ba cứ sau mỗi $65$ phút hoàn thành một chu trình và dư ra $48$ phút chuẩn bị. 

Để đồng bộ hóa hệ thống điện trung tâm, tổng số phút $n$ từ lúc khởi động đến khi cả ba dây chuyền đạt trạng thái đồng bộ phải là một số tự nhiên thỏa mãn các điều kiện trên đồng thời chia hết cho $19$. Hỏi giá trị nhỏ nhất của $n$ là bao nhiêu?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_50 = st.text_input("Nhập giá trị của n:", key="q50_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q50_check"):
    normalized_user_answer_50 = user_answer_50.strip().replace(',', '.')
    
    if normalized_user_answer_50 == "294823":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_50 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập hệ đồng dư thức dựa vào phần bù số dư ($28 - 11 = 17$), tìm BCNN và giải điều kiện chia hết cho 19 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q50_solution_shown' not in st.session_state:
    st.session_state['q50_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q50_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q50_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q50_solution_shown'] = False 

if st.session_state.get('q50_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Theo giả thiết bài toán, gọi $n$ là số phút cần tìm. Ta có các điều kiện sau:
    *   $n \equiv 11 \pmod{28} \iff n + 17 \equiv 0 \pmod{28}$ (vì $28 - 11 = 17$)
    *   $n \equiv 28 \pmod{45} \iff n + 17 \equiv 0 \pmod{45}$ (vì $45 - 28 = 17$)
    *   $n \equiv 48 \pmod{65} \iff n + 17 \equiv 0 \pmod{65}$ (vì $65 - 48 = 17$)
    *   $n \equiv 0 \pmod{19}$
    
    Từ ba điều kiện đầu, ta suy ra $(n + 17)$ đồng thời chia hết cho các số $28, 45$ và $65$.
    
    **Bước 2: Tính Bội chung nhỏ nhất (BCNN)**
    
    Phân tích các số chia ra thừa số nguyên tố:
    *   $28 = 2^2 \times 7$
    *   $45 = 3^2 \times 5$
    *   $65 = 5 \times 13$
    
    Bội chung nhỏ nhất của chúng là:
    $$\text{BCNN}(28, 45, 65) = 2^2 \times 3^2 \times 5 \times 7 \times 13 = 4 \times 9 \times 35 \times 13 = 16380$$
    
    Do đó, ta có dạng tổng quát của $n$:
    $$n + 17 = 16380k \implies n = 16380k - 17 \quad (k \in \mathbb{N}^*)$$
    
    **Bước 3: Sử dụng điều kiện chia hết cho 19**
    
    Vì $n$ chia hết cho $19$, ta thay biểu thức của $n$ vào điều kiện modulo $19$:
    $$16380k - 17 \equiv 0 \pmod{19}$$
    
    Thu gọn hệ số $16380$ theo modulo $19$:
    $$16380 = 19 \times 862 + 2 \equiv 2 \pmod{19}$$
    
    Phương trình đồng dư trở thành:
    $$2k - 17 \equiv 0 \pmod{19} \iff 2k \equiv 17 \equiv 36 \pmod{19}$$
    $$\implies k \equiv 18 \pmod{19}$$
    
    Suy ra:
    $$k = 19m + 18 \quad (m \in \mathbb{N})$$
    
    **Bước 4: Tính giá trị $n$ nhỏ nhất**
    
    Thay $k$ ngược lại vào biểu thức của $n$:
    $$n = 16380(19m + 18) - 17 = 311220m + 294840 - 17 = 311220m + 294823$$
    
    Để tìm số tự nhiên $n$ nhỏ nhất, ta chọn giá trị $m = 0$:
    $$n = 311220 \times 0 + 294823 = 294823$$
    
    **Kết luận:** Giá trị nhỏ nhất của $n$ là **$294823$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 51 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 51. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 2027$. Xét tất cả các số nguyên $x$ thỏa mãn điều kiện $1 \le x \le 2026$. Gọi $S$ là tổng tất cả các giá trị của $x$ thỏa mãn phương trình đồng dư:
$$\prod_{k=1}^{2026} (x - k) \equiv 0 \pmod{2027}$$
Tính giá trị của $S$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 51) ---
user_ans_51 = st.text_input("Nhập giá trị của tổng S:", key="q51_ans")

if st.button("Kiểm tra đáp án Câu 51", key="q51_check"):
    norm_ans_51 = user_ans_51.strip()
    
    # Đáp án chính xác là 2053351
    if norm_ans_51 == "2053351":
        st.success("🎉 Xuất sắc! Bạn đã nhận diện bản chất đa thức đồng dư trong trường hữu hạn cực kỳ sâu sắc. Lời giải Câu 51 đã được mở khóa.")
    elif user_ans_51 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 51.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Phương trình đồng dư trên có tập nghiệm chính là tất cả các số nguyên từ $1$ đến $2026$. Hãy tính tổng của cấp số cộng này.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 51 ---
st.markdown("---")

if 'q51_solution_shown' not in st.session_state:
    st.session_state['q51_solution_shown'] = False

col1_51, col2_51 = st.columns([1, 4])
with col1_51:
    if st.button("Xem lời giải Câu 51", key="q51_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q51_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q51_solution_shown'] = False 

if st.session_state.get('q51_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 51 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân tích cấu trúc phương trình đồng dư**
    
    Phương trình cần xét là:
    $$\prod_{k=1}^{2026} (x - k) \equiv 0 \pmod{2027}$$
    
    Một tích các thừa số đồng dư với $0$ theo mô-đun một số nguyên tố $p = 2027$ khi và chỉ khi có ít nhất một thừa số chia hết cho $2027$. 
    Điều này có nghĩa là:
    $$x - k \equiv 0 \pmod{2027} \iff x \equiv k \pmod{2027}$$
    với mỗi $k \in \{1, 2, 3, \dots, 2026\}$.
    
    **Bước 2: Xác định tập nghiệm trong miền giới hạn**
    
    Vì bài toán yêu cầu tìm các nghiệm $x$ thỏa mãn điều kiện $1 \le x \le 2026$, nên mọi giá trị $x \in \{1, 2, 3, \dots, 2026\}$ khi thay vào đều làm cho đúng một thừa số trong tích triệt tiêu (bằng $0$), đồng thời không vượt quá giá trị của số nguyên tố $p = 2027$.
    
    Do đó, tập hợp tất cả các nghiệm $x$ thỏa mãn yêu cầu bài toán chính là:
    $$X = \{1, 2, 3, \dots, 2026\}$$
    
    **Bước 3: Tính tổng $S$ và kết luận**
    
    Tổng $S$ là tổng của tất cả các phần tử trong tập nghiệm $X$:
    $$S = \sum_{k=1}^{2026} k = \dfrac{2026 \times (1 + 2026)}{2} = 1013 \times 2027 = 2053351$$
    
    Vậy giá trị của tổng $S$ là $2053351$.
    
    ---
    **👉 Đáp số Câu 51:** `2053351`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 52 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 52. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 1009$. Tính số lượng các số nguyên $x$ thỏa mãn đồng thời hai điều kiện: $1 \le x \le 1008$ và biểu thức $x^2 + 1$ chia hết cho $1009$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 52) ---
user_ans_52 = st.text_input("Nhập số lượng số nguyên x thỏa mãn:", key="q52_ans")

if st.button("Kiểm tra đáp án Câu 52", key="q52_check"):
    norm_ans_52 = user_ans_52.strip()
    
    # Đáp án chính xác là 2
    if norm_ans_52 == "2":
        st.success("🎉 Xuất sắc! Bạn đã vận dụng lý thuyết thặng dư chính phương và tiêu chuẩn Euler cực kỳ đỉnh cao. Lời giải Câu 52 đã được mở khóa.")
    elif user_ans_52 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 52.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Chuyển bài toán về phương trình đồng dư $x^2 \equiv -1 \pmod{1009}$. Kiểm tra xem $-1$ có phải là thặng dư chính phương modulo $1009$ hay không (dùng tính chất $p \equiv 1 \pmod 4$).")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 52 ---
st.markdown("---")

if 'q52_solution_shown' not in st.session_state:
    st.session_state['q52_solution_shown'] = False

col1_52, col2_52 = st.columns([1, 4])
with col1_52:
    if st.button("Xem lời giải Câu 52", key="q52_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q52_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q52_solution_shown'] = False 

if st.session_state.get('q52_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 52 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Chuyển đổi bài toán về phương trình đồng dư**
    
    Biểu thức $x^2 + 1$ chia hết cho $1009$ tương đương với phương trình đồng dư:
    $$x^2 + 1 \equiv 0 \pmod{1009} \iff x^2 \equiv -1 \pmod{1009}$$
    
    **Bước 2: Kiểm tra tính thặng dư chính phương của $-1$ modulo $1009$**
    
    Ta có số nguyên tố $p = 1009$. 
    Thực hiện phép chia $1009$ cho $4$:
    $$1009 = 4 \times 252 + 1 \implies p \equiv 1 \pmod 4$$
    
    Theo định lý về thặng dư chính phương (hoặc Tiêu chuẩn Euler), đối với bất kỳ số nguyên tố dạng $p \equiv 1 \pmod 4$, số $-1$ luôn là một **thặng dư chính phương** modulo $p$. 
    Điều này có nghĩa là phương trình $x^2 \equiv -1 \pmod p$ luôn có **đúng hai nghiệm phân biệt** không đồng dư modulo $p$.
    
    **Bước 3: Xác định vị trí của các nghiệm trong khoảng cho phép**
    
    Giả sử phương trình có nghiệm $x_0$. Khi đó:
    *   Nghiệm thứ nhất là $x_0$.
    *   Nghiệm thứ hai là $p - x_0 = 1009 - x_0$.
    
    Vì $x_0$ và $1009 - x_0$ đều nằm trong khoảng từ $1$ đến $1008$ (không có nghiệm nào trùng với $0$ hay $1009$), cả hai nghiệm này đều thỏa mãn hoàn hảo điều kiện bài toán yêu cầu: $1 \le x \le 1008$.
    
    **Bước 4: Kết luận**
    
    Số lượng các số nguyên $x$ thỏa mãn yêu cầu bài toán là $2$.
    
    ---
    **👉 Đáp số Câu 52:** `2`
    """)

st.markdown("---")



# ==========================================
# CÂU 53: HỢP SỐ NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 53 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $n$. Xét số $S_n = n^6 + 27$. Hỏi có bao nhiêu giá trị nguyên dương của $n$ thuộc đoạn $[1; 2026]$ để $S_n$ là một **hợp số**?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_53 = st.text_input("Nhập số lượng giá trị của n:", key="q53_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q53_check"):
    normalized_user_answer_53 = user_answer_53.strip().replace(',', '.')
    
    if normalized_user_answer_53 == "2026":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_53 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích biểu thức thành nhân tử sử dụng hằng đẳng thức tổng lập phương nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q53_solution_shown' not in st.session_state:
    st.session_state['q53_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q53_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q53_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q53_solution_shown'] = False 

if st.session_state.get('q53_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích biểu thức thành nhân tử**
    
    Ta biến đổi biểu thức $S_n = n^6 + 27$ bằng cách áp dụng hằng đẳng thức tổng hai lập phương ($a^3 + b^3 = (a+b)(a^2 - ab + b^2)$ với $a = n^2$ và $b = 3$):
    $$S_n = (n^2)^3 + 3^3 = (n^2 + 3)(n^4 - 3n^2 + 9)$$
    
    **Bước 2: Đánh giá các nhân tử**
    
    *   Xét nhân tử thứ nhất: Với mọi số nguyên dương $n$, ta luôn có $n^2 \ge 1$, do đó:
        $$n^2 + 3 \ge 1 + 3 = 4 > 1$$
        
    *   Xét nhân tử thứ hai, ta biến đổi thành tổng các bình phương:
        $$n^4 - 3n^2 + 9 = (n^2)^2 - 2 \cdot n^2 \cdot \frac{3}{2} + \frac{9}{4} + \frac{27}{4} = \left(n^2 - \dfrac{3}{2}\right)^2 + \dfrac{27}{4} \ge \dfrac{27}{4} > 1$$
        Hoặc phân tích gọn hơn: $n^4 - 3n^2 + 9 = (n^2 - 1)^2 + n^2 + 8 \ge 8 > 1$ với mọi số nguyên dương $n$.
        
    Vì cả hai nhân tử $(n^2 + 3)$ và $(n^4 - 3n^2 + 9)$ đều lớn hơn $1$ với mọi số nguyên dương $n$, nên tích của chúng luôn là một **hợp số** với mọi $n \ge 1$.
    
    **Bước 3: Đếm số lượng giá trị thỏa mãn**
    
    Do tính chất trên nghiệm đúng với mọi số nguyên dương $n$, tất cả các giá trị của $n$ thuộc đoạn $[1; 2026]$ đều làm cho $S_n$ thành hợp số.
    
    Số lượng các giá trị của $n$ là:
    $$2026 - 1 + 1 = 2026 \text{ (giá trị)}$$
    
    **Kết luận:** Có tổng cộng **$2026$** giá trị của $n$ thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 54: TÌM 3 CHỮ SỐ TẬN CÙNG
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 54 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm $3$ chữ số tận cùng của số $A = 7^{2026}$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_54 = st.text_input("Nhập 3 chữ số tận cùng:", key="q54_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q54_check"):
    normalized_user_answer_54 = user_answer_54.strip().replace(',', '.')
    
    if normalized_user_answer_54 == "649":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_54 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý Euler với mô-đun $1000$ để hạ bậc số mũ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q54_solution_shown' not in st.session_state:
    st.session_state['q54_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q54_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q54_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q54_solution_shown'] = False 

if st.session_state.get('q54_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập bài toán đồng dư**
    
    Tìm $3$ chữ số tận cùng của số $A = 7^{2026}$ tương đương với việc tìm số dư của phép chia $7^{2026}$ cho $1000$:
    $$A \equiv 7^{2026} \pmod{1000}$$
    
    **Bước 2: Áp dụng Định lý Euler**
    
    Ta có $\text{gcd}(7, 1000) = 1$. Tính hàm số Euler của $1000$:
    $$\phi(1000) = 1000 \cdot \left(1 - \dfrac{1}{2}\right)\left(1 - \dfrac{1}{5}\right) = 1000 \cdot \dfrac{1}{2} \cdot \dfrac{4}{5} = 400$$
    
    Theo **Định lý Euler**, ta có:
    $$7^{400} \equiv 1 \pmod{1000}$$
    
    Thực hiện chia số mũ cho chu kỳ $400$:
    $$2026 = 400 \times 5 + 26$$
    
    Do đó:
    $$7^{2026} = 7^{400 \times 5 + 26} = (7^{400})^5 \cdot 7^{26} \equiv 1^5 \cdot 7^{26} \equiv 7^{26} \pmod{1000}$$
    
    **Bước 3: Thu gọn số dư của $7^{26} \pmod{1000}$**
    
    Ta tính lần lượt các lũy thừa của $7$:
    *   $7^2 = 49$
    *   $7^4 = 2401 \equiv 401 \pmod{1000}$
    *   $7^6 = 401 \times 49 = 19649 \equiv 649 \pmod{1000}$
    *   $7^{12} = (649)^2 = 421201 \equiv 201 \pmod{1000}$
    *   $7^{24} = (7^{12})^2 \equiv 201^2 = 40401 \equiv 401 \pmod{1000}$
    
    Suy ra:
    $$7^{26} = 7^{24} \cdot 7^2 \equiv 401 \times 49 = 19649 \equiv 649 \pmod{1000}$$
    
    **Kết luận:** $3$ chữ số tận cùng của số $A = 7^{2026}$ là **$649$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 55: TOÁN THỰC TẾ SỐ HỌC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 55 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một hệ thống xử lý dữ liệu tự động gồm ba máy chủ vận hành liên tục. Máy chủ thứ nhất cứ sau mỗi $33$ phút hoàn thành một chu trình và dư ra $12$ phút bảo trì; máy chủ thứ hai cứ sau mỗi $52$ phút hoàn thành một chu trình và dư ra $31$ phút bảo trì; máy chủ thứ ba cứ sau mỗi $77$ phút hoàn thành một chu trình và dư ra $56$ phút bảo trì. 

Để đồng bộ hóa toàn bộ hệ thống, tổng số phút $n$ từ lúc khởi động đến khi cả ba máy chủ đạt trạng thái đồng bộ phải là một số tự nhiên thỏa mãn các điều kiện trên đồng thời chia hết cho $23$. Hỏi giá trị nhỏ nhất của $n$ là bao nhiêu?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_55 = st.text_input("Nhập giá trị của n:", key="q55_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q55_check"):
    normalized_user_answer_55 = user_answer_55.strip().replace(',', '.')
    
    if normalized_user_answer_55 == "180159":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_55 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập hệ đồng dư thức dựa vào phần bù số dư ($33 - 12 = 21$), tìm BCNN và giải điều kiện chia hết cho 23 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q55_solution_shown' not in st.session_state:
    st.session_state['q55_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q55_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q55_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q55_solution_shown'] = False 

if st.session_state.get('q55_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Theo giả thiết bài toán, gọi $n$ là số phút cần tìm. Ta có các điều kiện đồng dư sau:
    *   $n \equiv 12 \pmod{33} \iff n + 21 \equiv 0 \pmod{33}$ (vì $33 - 12 = 21$)
    *   $n \equiv 31 \pmod{52} \iff n + 21 \equiv 0 \pmod{52}$ (vì $52 - 31 = 21$)
    *   $n \equiv 56 \pmod{77} \iff n + 21 \equiv 0 \pmod{77}$ (vì $77 - 56 = 21$)
    *   $n \equiv 0 \pmod{23}$
    
    Từ ba điều kiện đầu, ta suy ra $(n + 21)$ đồng thời chia hết cho các số $33, 52$ và $77$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất (BCNN)**
    
    Phân tích các số chia ra thừa số nguyên tố:
    *   $33 = 3 \times 11$
    *   $52 = 2^2 \times 13$
    *   $77 = 7 \times 11$
    
    Bội chung nhỏ nhất của chúng là:
    $$\text{BCNN}(33, 52, 77) = 2^2 \times 3 \times 7 \times 11 \times 13 = 12012$$
    
    Do đó, ta có dạng tổng quát của $n$:
    $$n + 21 = 12012k \implies n = 12012k - 21 \quad (k \in \mathbb{N}^*)$$
    
    **Bước 3: Sử dụng điều kiện chia hết cho 23**
    
    Vì $n$ chia hết cho $23$, ta thay biểu thức của $n$ vào điều kiện modulo $23$:
    $$12012k - 21 \equiv 0 \pmod{23}$$
    
    Thu gọn hệ số theo modulo $23$:
    $$12012 = 23 \times 522 + 6 \equiv 6 \pmod{23}$$
    $$-21 \equiv 2 \pmod{23}$$
    
    Phương trình đồng dư trở thành:
    $$6k + 2 \equiv 0 \pmod{23} \iff 6k \equiv -2 \equiv 21 \pmod{23}$$
    
    Rút gọn biểu thức cho $3$:
    $$2k \equiv 7 \equiv 30 \pmod{23} \implies k \equiv 15 \pmod{23}$$
    
    Suy ra:
    $$k = 23m + 15 \quad (m \in \mathbb{N})$$
    
    **Bước 4: Tính giá trị $n$ nhỏ nhất**
    
    Thay $k$ ngược lại vào biểu thức của $n$:
    $$n = 12012(23m + 15) - 21 = 276276m + 180180 - 21 = 276276m + 180159$$
    
    Để tìm số tự nhiên $n$ nhỏ nhất, ta chọn giá trị $m = 0$:
    $$n = 276276 \times 0 + 180159 = 180159$$
    
    **Kết luận:** Giá trị nhỏ nhất của $n$ là **$180159$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 56 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 56. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho tập hợp $A$ gồm các số nguyên dương $x$ sao cho $1 \le x \le 2026$ và $x$ nguyên tố cùng nhau với $2026$. Gọi $S$ là tổng tất cả các phần tử của tập $A$. Tính số dư khi chia $S$ cho số nguyên tố $1009$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 56) ---
user_ans_56 = st.text_input("Nhập số dư của S khi chia cho 1009:", key="q56_ans")

if st.button("Kiểm tra đáp án Câu 56", key="q56_check"):
    norm_ans_56 = user_ans_56.strip()
    
    # Đáp án chính xác là 12
    if norm_ans_56 == "12":
        st.success("🎉 Xuất sắc! Bạn đã kết hợp cực kỳ uyển chuyển công thức tổng các phần tử nguyên tố cùng nhau với phép đồng dư modulo. Lời giải Câu 56 đã được mở khóa.")
    elif user_ans_56 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 56.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Sử dụng tính chất tổng các số nguyên tố cùng nhau với $N$ là $S = \dfrac{N \cdot \phi(N)}{2}$ với $N > 2$, sau đó tính modulo $1009$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 56 ---
st.markdown("---")

if 'q56_solution_shown' not in st.session_state:
    st.session_state['q56_solution_shown'] = False

col1_56, col2_56 = st.columns([1, 4])
with col1_56:
    if st.button("Xem lời giải Câu 56", key="q56_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q56_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q56_solution_shown'] = False 

if st.session_state.get('q56_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 56 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân tích cấu trúc tập hợp và tính tổng $S$**
    
    Ta có $N = 2026 = 2 \times 1013$ (với $1013$ là số nguyên tố).
    Đối với mọi số nguyên dương $N > 2$, tổng $S$ tất cả các số nguyên dương $x \le N$ và nguyên tố cùng nhau với $N$ được tính bởi công thức kinh điển:
    $$S = \dfrac{N \cdot \phi(N)}{2}$$
    trong đó $\phi(N)$ là hàm số Euler.
    
    Tính $\phi(2026)$:
    $$\phi(2026) = 2026 \times \left(1 - \dfrac{1}{2}\right) \times \left(1 - \dfrac{1}{1013}\right) = 2026 \times \dfrac{1}{2} \times \dfrac{1012}{1013} = 1013 \times \dfrac{1012}{1013} = 1012$$
    
    Thay vào công thức tính tổng $S$:
    $$S = \dfrac{2026 \times 1012}{2} = 1013 \times 1012 = 1025156$$
    
    **Bước 2: Tính số dư của $S$ khi chia cho $1009$**
    
    Ta cần tìm số dư của $S = 1013 \times 1012$ khi chia cho số nguyên tố $1009$:
    *   $1013 = 1009 + 4 \equiv 4 \pmod{1009}$
    *   $1012 = 1009 + 3 \equiv 3 \pmod{1009}$
    
    Do đó:
    $$S \equiv 4 \times 3 = 12 \pmod{1009}$$
    
    **Bước 3: Kết luận**
    
    Số dư của tổng $S$ khi chia cho $1009$ là $12$.
    
    ---
    **👉 Đáp số Câu 56:** `12`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 57 - [Trả lời ngắn _ TSA]
# =====================================================================

# ==========================================
# CÂU 57: SỐ HỌC - ĐỒNG DƯ THỨC NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 57 (Đề tham khảo TSA 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $A = 2^{2026} + 3^{2026} + 6^{2026}$. Tìm số dư khi chia số $A$ cho $77$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập số dư của phép chia:", key="q57_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q57_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    if normalized_user_answer == "28":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích $77 = 7 \times 11$, sau đó áp dụng Định lý Tiểu Fermat để tìm số dư theo từng mô-đun nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q57_solution_shown' not in st.session_state:
    st.session_state['q57_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q57_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q57_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q57_solution_shown'] = False 

if st.session_state.get('q57_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích mô-đun và thiết lập bài toán đồng dư**
    
    Yêu cầu bài toán là tìm số dư của biểu thức $A = 2^{2026} + 3^{2026} + 6^{2026}$ khi chia cho $77$. 
    Vì $77 = 7 \times 11$ và $\text{gcd}(7, 11) = 1$, ta sẽ tính số dư của $A$ lần lượt theo mô-đun $7$ và mô-đun $11$, sau đó kết hợp lại.
    
    **Bước 2: Tính số dư của $A$ theo mô-đun $7$**
    
    Theo Định lý Tiểu Fermat, ta có $2^6 \equiv 1 \pmod 7$, $3^6 \equiv 1 \pmod 7$ và $6 \equiv -1 \pmod 7$.
    Thực hiện chia số mũ cho chu kỳ $6$:
    $$2026 = 6 \times 337 + 4$$
    
    Do đó:
    *   $2^{2026} = (2^6)^{337} \cdot 2^4 \equiv 1^{337} \cdot 16 \equiv 2 \pmod 7$
    *   $3^{2026} = (3^6)^{337} \cdot 3^4 \equiv 1^{337} \cdot 81 \equiv 4 \pmod 7$
    *   $6^{2026} \equiv (-1)^{2026} \equiv 1 \pmod 7$
    
    Cộng các số dư lại, ta được:
    $$A \equiv 2 + 4 + 1 = 7 \equiv 0 \pmod 7$$
    
    **Bước 3: Tính số dư của $A$ theo mô-đun $11$**
    
    Theo Định lý Tiểu Fermat, với số nguyên tố $11$, ta có $a^{10} \equiv 1 \pmod{11}$ với mọi $a$ không chia hết cho $11$.
    Thực hiện chia số mũ cho chu kỳ $10$:
    $$2026 = 10 \times 202 + 6$$
    
    Do đó:
    *   $2^{2026} = (2^{10})^{202} \cdot 2^6 \equiv 1^{202} \cdot 64 \equiv 9 \pmod{11}$
    *   $3^{2026} = (3^{10})^{202} \cdot 3^6 \equiv 1^{202} \cdot 729 \equiv 3 \pmod{11}$
    *   $6^{2026} = (6^{10})^{202} \cdot 6^6 \equiv 1^{202} \cdot (6^2)^3 \equiv 36^3 \equiv 3^3 = 27 \equiv 5 \pmod{11}$
    
    Cộng các số dư lại, ta được:
    $$A \equiv 9 + 3 + 5 = 17 \equiv 6 \pmod{11}$$
    
    **Bước 4: Giải hệ đồng dư để tìm số dư theo mô-đun $77$**
    
    Ta có hệ đồng dư thức:
    $$\begin{cases} A \equiv 0 \pmod 7 \\ A \equiv 6 \pmod{11} \end{cases}$$
    
    Từ phương trình thứ nhất, ta đặt $A = 7k$ ($k \in \mathbb{N}$). Thay vào phương trình thứ hai:
    $$7k \equiv 6 \pmod{11}$$
    
    Nhân cả hai vế với nghịch đảo mô-đun của $7$ modulo $11$ (ta có $7 \times 8 = 56 \equiv 1 \pmod{11}$):
    $$k \equiv 6 \times 8 = 48 \equiv 4 \pmod{11}$$
    
    Suy ra $k = 11m + 4$ ($m \in \mathbb{N}$). Khi đó:
    $$A = 7(11m + 4) = 77m + 28$$
    
    Vậy số dư của $A$ khi chia cho $77$ là $28$.
    
    **Kết luận:** Số dư cần tìm là **$28$**.
    """)
    
st.markdown("---")



# ==========================================
# CÂU 58: SỐ LẬP PHƯƠNG NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 58 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $n$. Xét số $S_n = n^3 + 3n^2 + 3n$. Hỏi có bao nhiêu giá trị nguyên dương của $n$ thuộc đoạn $[1; 2026]$ để $S_n$ là một **số lập phương**?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_58 = st.text_input("Nhập số lượng giá trị của n:", key="q58_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q58_check"):
    normalized_user_answer_58 = user_answer_58.strip().replace(',', '.')
    
    if normalized_user_answer_58 == "0":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_58 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy biến đổi biểu thức về dạng $(n+1)^3 - 1$ và đánh giá kẹp giữa hai số lập phương liên tiếp nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q58_solution_shown' not in st.session_state:
    st.session_state['q58_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q58_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q58_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q58_solution_shown'] = False 

if st.session_state.get('q58_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biến đổi biểu thức**
    
    Ta xét cấu trúc của biểu thức $S_n$:
    $$S_n = n^3 + 3n^2 + 3n$$
    
    Thêm và bớt $1$ đơn vị để đưa về hằng đẳng thức lập phương của một tổng:
    $$S_n = (n^3 + 3n^2 + 3n + 1) - 1 = (n + 1)^3 - 1$$
    
    **Bước 2: Đánh giá khoảng giá trị của $S_n$**
    
    Với mọi số nguyên dương $n \ge 1$, ta có bất đẳng thức sau:
    $n \ge 1 \implies n + 1 \ge 2$, do đó:
    $$(n + 1)^3 > n^3$$
    
    Mặt khác, vì $1 > 0$, ta suy ra:
    $$(n + 1)^3 - 1 < (n + 1)^3$$
    
    Kết hợp lại, ta được:
    $$n^3 < (n + 1)^3 - 1 < (n + 1)^3$$
    
    **Bước 3: Kết luận**
    
    Biểu thức $S_n = (n + 1)^3 - 1$ nằm kẹp giữa hai lập phương liên tiếp là $n^3$ và $(n + 1)^3$ với mọi số nguyên dương $n$. 
    
    Do đó, $S_n$ không thể là lập phương của bất kỳ số nguyên nào.
    
    **Kết luận:** Không có giá trị nguyên dương nào của $n$ thỏa mãn yêu cầu bài toán, số lượng giá trị bằng **$0$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 59: CHIA HẾT NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 59 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $n$. Hỏi có bao nhiêu giá trị nguyên dương của $n$ thuộc đoạn $[1; 2026]$ để biểu thức $P_n = n^4 - 2n^3 - n^2 + 2n$ chia hết cho $24$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_59 = st.text_input("Nhập số lượng giá trị của n:", key="q59_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q59_check"):
    normalized_user_answer_59 = user_answer_59.strip().replace(',', '.')
    
    if normalized_user_answer_59 == "2026":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_59 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích đa thức thành tích của các số nguyên liên tiếp nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q59_solution_shown' not in st.session_state:
    st.session_state['q59_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q59_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q59_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q59_solution_shown'] = False 

if st.session_state.get('q59_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích đa thức thành nhân tử**
    
    Ta biến đổi biểu thức $P_n$:
    $$P_n = n^4 - 2n^3 - n^2 + 2n$$
    $$P_n = n^3(n - 2) - n(n - 2)$$
    $$P_n = (n - 2)(n^3 - n)$$
    $$P_n = (n - 2)n(n^2 - 1)$$
    $$P_n = (n - 2)(n - 1)n(n + 1)$$
    
    Sắp xếp lại các nhân tử theo thứ tự tăng dần:
    $$P_n = (n - 2)(n - 1)n(n + 1)$$
    
    **Bước 2: Chứng minh tính chất chia hết cho $24$**
    
    Biểu thức $P_n$ chính là tích của $4$ số nguyên liên tiếp: $(n-2)$, $(n-1)$, $n$ và $(n+1)$.
    
    *   Trong $4$ số nguyên liên tiếp luôn có ít nhất một bội của $4$, một số chẵn khác (suy ra tích chia hết cho $8$).
    *   Trong $4$ số nguyên liên tiếp luôn có ít nhất một bội của $3$.
    *   Vì $\text{gcd}(8, 3) = 1$, tích của $4$ số nguyên liên tiếp luôn chia hết cho $8 \times 3 = 24$ với mọi số nguyên $n \ge 1$.
    
    **Bước 3: Đếm số lượng giá trị thỏa mãn**
    
    Tính chất trên đúng với mọi số nguyên dương $n \ge 1$. Do đó, với mọi $n$ thuộc đoạn $[1; 2026]$, biểu thức $P_n$ luôn chia hết cho $24$.
    
    Số lượng các giá trị của $n$ là:
    $$2026 - 1 + 1 = 2026 \text{ (giá trị)}$$
    
    **Kết luận:** Có tổng cộng **$2026$** giá trị của $n$ thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 60: TOÁN THỰC TẾ SỐ HỌC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 60 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một hệ thống xử lý dữ liệu tự động gồm ba máy chủ vận hành liên tục. Máy chủ thứ nhất cứ sau mỗi $42$ phút hoàn thành một chu trình và dư ra $15$ phút bảo trì; máy chủ thứ hai cứ sau mỗi $56$ phút hoàn thành một chu trình và dư ra $29$ phút bảo trì; máy chủ thứ ba cứ sau mỗi $70$ phút hoàn thành một chu trình và dư ra $43$ phút bảo trì. 

Để đồng bộ hóa toàn bộ hệ thống, tổng số phút $n$ từ lúc khởi động đến khi cả ba máy chủ đạt trạng thái bảo trì đồng thời phải là một số tự nhiên thỏa mãn các điều kiện trên đồng thời chia hết cho $17$. Hỏi giá trị nhỏ nhất của $n$ là bao nhiêu?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_60 = st.text_input("Nhập giá trị của n:", key="q60_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q60_check"):
    normalized_user_answer_60 = user_answer_60.strip().replace(',', '.')
    
    if normalized_user_answer_60 == "13413":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_60 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập hệ đồng dư thức dựa vào phần bù số dư ($42 - 15 = 27$), tìm BCNN và giải điều kiện chia hết cho 17 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q60_solution_shown' not in st.session_state:
    st.session_state['q60_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q60_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q60_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q60_solution_shown'] = False 

if st.session_state.get('q60_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Theo giả thiết bài toán, gọi $n$ là số phút cần tìm. Ta có các điều kiện đồng dư sau:
    *   $n \equiv 15 \pmod{42} \iff n + 27 \equiv 0 \pmod{42}$ (vì $42 - 15 = 27$)
    *   $n \equiv 29 \pmod{56} \iff n + 27 \equiv 0 \pmod{56}$ (vì $56 - 29 = 27$)
    *   $n \equiv 43 \pmod{70} \iff n + 27 \equiv 0 \pmod{70}$ (vì $70 - 43 = 27$)
    *   $n \equiv 0 \pmod{17}$
    
    Từ ba điều kiện đầu, ta suy ra $(n + 27)$ đồng thời chia hết cho các số $42, 56$ và $70$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất (BCNN)**
    
    Phân tích các số chia ra thừa số nguyên tố:
    *   $42 = 2 \times 3 \times 7$
    *   $56 = 2^3 \times 7$
    *   $70 = 2 \times 5 \times 7$
    
    Bội chung nhỏ nhất của chúng là:
    $$\text{BCNN}(42, 56, 70) = 2^3 \times 3 \times 5 \times 7 = 840$$
    
    Do đó, ta có dạng tổng quát của $n$:
    $$n + 27 = 840k \implies n = 840k - 27 \quad (k \in \mathbb{N}^*)$$
    
    **Bước 3: Sử dụng điều kiện chia hết cho 17**
    
    Vì $n$ chia hết cho $17$, ta thay biểu thức của $n$ vào điều kiện modulo $17$:
    $$840k - 27 \equiv 0 \pmod{17}$$
    
    Thu gọn hệ số theo modulo $17$:
    $$840 = 17 \times 49 + 7 \equiv 7 \pmod{17}$$
    $$-27 \equiv 7 \pmod{17}$$
    
    Phương trình đồng dư trở thành:
    $$7k + 7 \equiv 0 \pmod{17} \iff 7(k + 1) \equiv 0 \pmod{17}$$
    
    Vì $\text{gcd}(7, 17) = 1$, suy ra:
    $$k + 1 \equiv 0 \pmod{17} \iff k \equiv 16 \pmod{17}$$
    
    Đặt $k = 17m + 16$ với $m \in \mathbb{N}$.
    
    **Bước 4: Tính giá trị $n$ nhỏ nhất**
    
    Thay $k$ ngược lại vào biểu thức của $n$:
    $$n = 840(17m + 16) - 27 = 14280m + 13440 - 27 = 14280m + 13413$$
    
    Để tìm số tự nhiên $n$ nhỏ nhất, ta chọn giá trị $m = 0$:
    $$n = 14280 \times 0 + 13413 = 13413$$
    
    **Kết luận:** Giá trị nhỏ nhất của $n$ là **$13413$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 61 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 61. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 2027$. Xét tập hợp tất cả các số nguyên $n$ thuộc đoạn $[1; 2026]$ sao cho phương trình đồng dư $x^3 \equiv n \pmod{2027}$ có nghiệm nguyên $x$. Tính số lượng phần tử của tập hợp này.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 61) ---
user_ans_61 = st.text_input("Nhập số lượng phần tử thỏa mãn:", key="q61_ans")

if st.button("Kiểm tra đáp án Câu 61", key="q61_check"):
    norm_ans_61 = user_ans_61.strip()
    
    # Đáp án chính xác là 2026
    if norm_ans_61 == "2026":
        st.success("🎉 Xuất sắc! Bạn đã nắm vững tính chất song ánh của lũy thừa trong trường hữu hạn khi $\gcd(3, p-1) = 1$ cực kỳ sâu sắc. Lời giải Câu 61 đã được mở khóa.")
    elif user_ans_61 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 61.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy kiểm tra ước chung lớn nhất của số mũ $3$ và $p-1 = 2026$. Nếu $\gcd(3, 2026) = 1$, ánh xạ lũy thừa bậc 3 là một song ánh.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 61 ---
st.markdown("---")

if 'q61_solution_shown' not in st.session_state:
    st.session_state['q61_solution_shown'] = False

col1_61, col2_61 = st.columns([1, 4])
with col1_61:
    if st.button("Xem lời giải Câu 61", key="q61_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q61_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q61_solution_shown'] = False 

if st.session_state.get('q61_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 61 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân tích điều kiện của số mũ và mô-đun**
    
    Xét phương trình đồng dư:
    $$x^3 \equiv n \pmod{2027}$$
    với số nguyên tố $p = 2027$ và $n \in \{1, 2, 3, \dots, 2026\}$.
    
    Ta xét số nguyên tố trừ đi $1$:
    $$p - 1 = 2027 - 1 = 2026$$
    
    Tính ước chung lớn nhất giữa số mũ và $p-1$:
    $$\gcd(3, 2026) = 1$$
    
    **Bước 2: Áp dụng tính chất song ánh (bijective map)**
    
    Theo lý thuyết số học cao cấp, khi $\gcd(k, p-1) = 1$, ánh xạ lũy thừa $f(x) = x^k \pmod p$ là một **phép song ánh** (hoán vị toàn bộ) trên tập hợp các thặng dư thu gọn $\mathbb{F}_p^*$.
    Điều này có nghĩa là với mọi giá trị $n$ từ $1$ đến $p-1$, phương trình $x^k \equiv n \pmod p$ luôn có **duy nhất một nghiệm** phân biệt.
    
    **Bước 3: Kết luận**
    
    Vì mọi số nguyên $n$ thuộc đoạn từ $1$ đến $2026$ đều thỏa mãn điều kiện có nghiệm nguyên $x$, số lượng các giá trị của $n$ chính bằng tổng số phần tử của đoạn này, tức là $2026$ phần tử.
    
    ---
    **👉 Đáp số Câu 61:** `2026`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 62 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 62. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 1009$. Tính số dư khi chia số tổ hợp $\dbinom{2018}{1009}$ cho số nguyên tố $1009$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 62) ---
user_ans_62 = st.text_input("Nhập số dư của số tổ hợp khi chia cho 1009:", key="q62_ans")

if st.button("Kiểm tra đáp án Câu 62", key="q62_check"):
    norm_ans_62 = user_ans_62.strip()
    
    # Đáp án chính xác là 2
    if norm_ans_62 == "2":
        st.success("🎉 Xuất sắc! Bạn đã vận dụng Định lý Lucas một cách vô cùng sắc bén và tinh tế. Lời giải Câu 62 đã được mở khóa.")
    elif user_ans_62 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 62.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy biểu diễn các số $2018$ và $1009$ dưới dạng hệ cơ số $1009$, sau đó áp dụng Định lý Lucas: $\dbinom{m}{k} \pmod p$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 62 ---
st.markdown("---")

if 'q62_solution_shown' not in st.session_state:
    st.session_state['q62_solution_shown'] = False

col1_62, col2_62 = st.columns([1, 4])
with col1_62:
    if st.button("Xem lời giải Câu 62", key="q62_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q62_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q62_solution_shown'] = False 

if st.session_state.get('q62_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 62 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Nhận diện cấu trúc và Định lý Lucas**
    
    Bài toán yêu cầu tìm số dư của $\dbinom{2018}{1009}$ khi chia cho số nguyên tố $p = 1009$. 
    Ta sử dụng **Định lý Lucas**, phát biểu rằng nếu các số nguyên không âm $m$ và $k$ được biểu diễn trong hệ cơ số $p$ là:
    $$m = m_d p^d + m_{d-1} p^{d-1} + \dots + m_1 p + m_0$$
    $$k = k_d p^d + k_{d-1} p^{d-1} + \dots + k_1 p + k_0$$
    thì:
    $$\dbinom{m}{k} \equiv \prod_{i=0}^{d} \dbinom{m_i}{k_i} \pmod p$$
    
    **Bước 2: Biểu diễn các số theo hệ cơ số $1009$**
    
    Với $p = 1009$:
    *   $2018 = 2 \times 1009 + 0 \implies$ các chữ số trong hệ cơ số $1009$ là $m_1 = 2, m_0 = 0$.
    *   $1009 = 1 \times 1009 + 0 \implies$ các chữ số trong hệ cơ số $1009$ là $k_1 = 1, k_0 = 0$.
    
    **Bước 3: Áp dụng Định lý Lucas để tính toán**
    
    $$\dbinom{2018}{1009} \equiv \dbinom{2}{1} \times \dbinom{0}{0} \pmod{1009}$$
    
    Ta tính từng thành phần:
    *   $\dbinom{2}{1} = 2$
    *   $\dbinom{0}{0} = 1$
    
    Nhân các kết quả lại:
    $$\dbinom{2018}{1009} \equiv 2 \times 1 = 2 \pmod{1009}$$
    
    **Bước 4: Kết luận**
    
    Số dư của phép chia là $2$.
    
    ---
    **👉 Đáp số Câu 62:** `2`
    """)

st.markdown("---")



# ==========================================
# CÂU 63: ĐỒNG DƯ THỨC VÀ ĐỊNH LÝ TRUNG HOA
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 63 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $A = 3^{2026} + 5^{2026} + 7^{2026}$. Tìm số dư khi chia số $A$ cho $143$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_63 = st.text_input("Nhập số dư của phép chia:", key="q63_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q63_check"):
    normalized_user_answer_63 = user_answer_63.strip().replace(',', '.')
    
    if normalized_user_answer_63 == "45":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_63 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích $143 = 11 \times 13$, sau đó dùng Định lý Tiểu Fermat để tính số dư theo từng mô-đun rồi kết hợp hệ đồng dư nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q63_solution_shown' not in st.session_state:
    st.session_state['q63_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q63_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q63_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q63_solution_shown'] = False 

if st.session_state.get('q63_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích mô-đun và thiết lập bài toán**
    
    Ta có $143 = 11 \times 13$ với $\text{gcd}(11, 13) = 1$. Để tìm số dư của $A = 3^{2026} + 5^{2026} + 7^{2026}$ khi chia cho $143$, ta tính số dư của $A$ lần lượt theo mô-đun $11$ và mô-đun $13$.
    
    **Bước 2: Tính số dư của $A$ theo mô-đun $11$**
    
    Theo Định lý Tiểu Fermat, ta có $a^{10} \equiv 1 \pmod{11}$. Chia số mũ cho chu kỳ $10$:
    $$2026 = 10 \times 202 + 6$$
    
    Do đó:
    *   $3^{2026} = (3^{10})^{202} \cdot 3^6 \equiv 1 \cdot 729 \equiv 3 \pmod{11}$
    *   $5^{2026} = (5^{10})^{202} \cdot 5^6 \equiv 1 \cdot 5 \equiv 5 \pmod{11}$ (vì $5^6 = 15625 \equiv 5 \pmod{11}$)
    *   $7^{2026} = (7^{10})^{202} \cdot 7^6 \equiv 1 \cdot 4 \pmod{11}$ (vì $7^6 \equiv 4 \pmod{11}$)
    
    Cộng lại, ta được:
    $$A \equiv 3 + 5 + 4 = 12 \equiv 1 \pmod{11}$$
    
    **Bước 3: Tính số dư của $A$ theo mô-đun $13$**
    
    Theo Định lý Tiểu Fermat, ta có $a^{12} \equiv 1 \pmod{13}$. Chia số mũ cho chu kỳ $12$:
    $$2026 = 12 \times 168 + 10$$
    
    Do đó:
    *   $3^{2026} = (3^{12})^{168} \cdot 3^{10} \equiv 1 \cdot 3 = 3 \pmod{13}$ (vì $3^3 \equiv 1 \implies 3^{10} \equiv 3$)
    *   $5^{2026} = (5^{12})^{168} \cdot 5^{10} \equiv 1 \cdot (-1) \pmod{13}$ (vì $5^4 \equiv 1 \implies 5^{10} \equiv 5^2 = 25 \equiv -1 \pmod{13}$)
    *   $7^{2026} = (7^{12})^{168} \cdot 7^{10} \equiv 1 \cdot 4 \pmod{13}$ (vì $7^{10} \equiv 4 \pmod{13}$)
    
    Cộng lại, ta được:
    $$A \equiv 3 + (-1) + 4 = 6 \pmod{13}$$
    
    **Bước 4: Giải hệ đồng dư thức**
    
    Ta có hệ:
    $$\begin{cases} A \equiv 1 \pmod{11} \\ A \equiv 6 \pmod{13} \end{cases}$$
    
    Đặt $A = 11k + 1$. Thay vào phương trình thứ hai:
    $$11k + 1 \equiv 6 \pmod{13} \implies 11k \equiv 5 \pmod{13}$$
    
    Vì $11 \equiv -2 \pmod{13}$, ta có $-2k \equiv 5 \equiv 18 \pmod{13} \implies k \equiv -9 \equiv 4 \pmod{13}$.
    Suy ra $k = 13m + 4$, dẫn đến:
    $$A = 11(13m + 4) + 1 = 143m + 45$$
    
    **Kết luận:** Số dư của phép chia $A$ cho $143$ là **$45$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 64: TOÁN THỰC TẾ SỐ HỌC NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 64 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một hệ thống xử lý dữ liệu gồm ba máy chủ vận hành liên tục. Máy chủ thứ nhất cứ sau mỗi $45$ phút hoàn thành một chu trình và dư ra $18$ phút bảo trì; máy chủ thứ hai cứ sau mỗi $60$ phút hoàn thành một chu trình và dư ra $33$ phút bảo trì; máy chủ thứ ba cứ sau mỗi $75$ phút hoàn thành một chu trình và dư ra $48$ phút bảo trì. 

Để đồng bộ hóa toàn bộ hệ thống, tổng số phút $n$ từ lúc khởi động đến khi cả ba máy chủ đạt trạng thái bảo trì đồng thời phải là một số tự nhiên thỏa mãn các điều kiện trên đồng thời chia hết cho $19$. Hỏi giá trị nhỏ nhất của $n$ là bao nhiêu?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_64 = st.text_input("Nhập giá trị của n:", key="q64_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q64_check"):
    normalized_user_answer_64 = user_answer_64.strip().replace(',', '.')
    
    if normalized_user_answer_64 == "6327":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_64 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập phần bù thời gian bắt đầu bảo trì ($45 - 18 = 27$), tìm BCNN và giải điều kiện chia hết cho 19 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q64_solution_shown' not in st.session_state:
    st.session_state['q64_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q64_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q64_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q64_solution_shown'] = False 

if st.session_state.get('q64_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức thời gian bảo trì**
    
    Gọi $n$ là số phút cần tìm. Thời điểm bắt đầu bảo trì trong mỗi chu kỳ của các máy chủ là:
    *   Máy 1: $45 - 18 = 27$ phút $\implies n \equiv 27 \pmod{45}$
    *   Máy 2: $60 - 33 = 27$ phút $\implies n \equiv 27 \pmod{60}$
    *   Máy 3: $75 - 48 = 27$ phút $\implies n \equiv 27 \pmod{75}$
    
    Do đó, ta có $(n - 27)$ đồng thời chia hết cho $45$, $60$ và $75$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất (BCNN)**
    
    Phân tích ra thừa số nguyên tố:
    *   $45 = 3^2 \times 5$
    *   $60 = 2^2 \times 3 \times 5$
    *   $75 = 3 \times 5^2$
    
    Bội chung nhỏ nhất của chúng là:
    $$\text{BCNN}(45, 60, 75) = 2^2 \times 3^2 \times 5^2 = 900$$
    
    Dạng tổng quát của $n$:
    $$n - 27 = 900k \implies n = 900k + 27 \quad (k \in \mathbb{N})$$
    
    **Bước 3: Sử dụng điều kiện chia hết cho 19**
    
    Vì $n$ chia hết cho $19$, ta thay vào phương trình đồng dư mô-đun $19$:
    $$900k + 27 \equiv 0 \pmod{19}$$
    
    Thu gọn hệ số theo mô-đun $19$:
    $$900 = 19 \times 47 + 7 \equiv 7 \pmod{19}$$
    $$27 = 19 \times 1 + 8 \equiv 8 \pmod{19}$$
    
    Phương trình trở thành:
    $$7k + 8 \equiv 0 \pmod{19} \implies 7k \equiv -8 \equiv 11 \pmod{19}$$
    
    Nhân cả hai vế với nghịch đảo của $7$ modulo $19$ (là $11$ vì $7 \times 11 = 77 \equiv 1 \pmod{19}$):
    $$k \equiv 11 \times 11 = 121 \equiv 7 \pmod{19}$$
    
    Đặt $k = 19m + 7$ với $m \in \mathbb{N}$.
    
    **Bước 4: Tính giá trị $n$ nhỏ nhất**
    
    Thay $k$ vào biểu thức của $n$:
    $$n = 900(19m + 7) + 27 = 17100m + 6300 + 27 = 17100m + 6327$$
    
    Để $n$ đạt giá trị nguyên dương nhỏ nhất, ta chọn $m = 0$:
    $$n = 6327$$
    
    **Kết luận:** Giá trị nhỏ nhất của $n$ là **$6327$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 65: HỢP SỐ NÂNG CAO - HẰNG ĐẲNG THỨC SOPHIE GERMAIN
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 65 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $n$. Xét số $S_n = n^4 + 324$. Hỏi có bao nhiêu giá trị nguyên dương của $n$ thuộc đoạn $[1; 2026]$ để $S_n$ là một **hợp số**?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_65 = st.text_input("Nhập số lượng giá trị của n:", key="q65_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q65_check"):
    normalized_user_answer_65 = user_answer_65.strip().replace(',', '.')
    
    if normalized_user_answer_65 == "2026":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_65 == "":
        st.warning("You chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng hằng đẳng thức Sophie Germain cho biểu thức $n^4 + 4 \cdot 3^4$ để phân tích thành nhân tử nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q65_solution_shown' not in st.session_state:
    st.session_state['q65_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q65_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q65_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q65_solution_shown'] = False 

if st.session_state.get('q65_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích biểu thức thành nhân tử**
    
    Ta nhận thấy $324 = 4 \times 81 = 4 \times 3^4$. Khi đó biểu thức được viết lại dưới dạng:
    $$S_n = n^4 + 4 \cdot 3^4$$
    
    Áp dụng hằng đẳng thức mở rộng Sophie Germain ($a^4 + 4b^4 = (a^2 - 2ab + 2b^2)(a^2 + 2ab + 2b^2)$) với $a = n$ và $b = 3$:
    $$S_n = (n^2 - 2 \cdot n \cdot 3 + 2 \cdot 3^2)(n^2 + 2 \cdot n \cdot 3 + 2 \cdot 3^2)$$
    $$S_n = (n^2 - 6n + 18)(n^2 + 6n + 18)$$
    
    **Bước 2: Đánh giá giá trị các nhân tử**
    
    *   Xét nhân tử thứ nhất, biến đổi về tổng bình phương:
        $$n^2 - 6n + 18 = (n - 3)^2 + 9$$
        Vì $(n - 3)^2 \ge 0$ với mọi số nguyên $n$, ta có:
        $$(n - 3)^2 + 9 \ge 9 > 1$$
        
    *   Xét nhân tử thứ hai:
        $$n^2 + 6n + 18 = (n + 3)^2 + 9$$
        Với mọi số nguyên dương $n \ge 1$, ta luôn có:
        $$(n + 3)^2 + 9 \ge 4^2 + 9 = 25 > 1$$
        
    Vì cả hai nhân tử $(n^2 - 6n + 18)$ và $(n^2 + 6n + 18)$ đều lớn hơn $1$ với mọi số nguyên dương $n$, nên tích của chúng luôn là một **hợp số**.
    
    **Bước 3: Đếm số lượng giá trị thỏa mãn**
    
    Do tính chất trên đúng với mọi số nguyên dương $n \ge 1$, tất cả các giá trị của $n$ thuộc đoạn $[1; 2026]$ đều làm cho $S_n$ là hợp số.
    
    Số lượng các giá trị của $n$ là:
    $$2026 - 1 + 1 = 2026 \text{ (giá trị)}$$
    
    **Kết luận:** Có tổng cộng **$2026$** giá trị của $n$ thỏa mãn yêu cầu bài toán.
    """)

st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 66 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 66. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 2027$. Xét tập hợp tất cả các nghiệm nguyên $x$ thuộc đoạn $[1, 2026]$ của phương trình đồng dư:
$$x^{2026} \equiv 1 \pmod{2027}$$
Gọi $P$ là tích của tất cả các phần tử thuộc tập nghiệm này. Tính số dư của $P$ khi chia cho $2027$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 66) ---
user_ans_66 = st.text_input("Nhập số dư của P khi chia cho 2027:", key="q66_ans")

if st.button("Kiểm tra đáp án Câu 66", key="q66_check"):
    norm_ans_66 = user_ans_66.strip()
    
    # Đáp án chính xác là 2026
    if norm_ans_66 == "2026":
        st.success("🎉 Xuất sắc! Bạn đã nhận diện toàn bộ nghiệm bằng Định lý Fermat nhỏ và rút gọn tích bằng Định lý Wilson cực kỳ sắc bén. Lời giải Câu 66 đã được mở khóa.")
    elif user_ans_66 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 66.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Theo Định lý Fermat nhỏ, mọi số nguyên từ $1$ đến $2026$ đều là nghiệm. Tích của chúng là $2026!$, hãy dùng Định lý Wilson để tính modulo $2027$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 66 ---
st.markdown("---")

if 'q66_solution_shown' not in st.session_state:
    st.session_state['q66_solution_shown'] = False

col1_66, col2_66 = st.columns([1, 4])
with col1_66:
    if st.button("Xem lời giải Câu 66", key="q66_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q66_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q66_solution_shown'] = False 

if st.session_state.get('q66_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 66 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Xác định tập hợp nghiệm của phương trình đồng dư**
    
    Phương trình cần xét là:
    $$x^{2026} \equiv 1 \pmod{2027}$$
    với số nguyên tố $p = 2027$ và điều kiện nghiệm $x \in [1, 2026]$.
    
    Theo **Định lý Fermat nhỏ**, với mọi số nguyên tố $p$ và mọi số nguyên $x$ không chia hết cho $p$ (tức là $1 \le x \le p-1$), ta luôn có:
    $$x^{p-1} \equiv 1 \pmod p$$
    
    Ở đây $p - 1 = 2027 - 1 = 2026$, do đó **mọi** số nguyên $x$ thuộc đoạn $[1, 2026]$ đều thỏa mãn phương trình đồng dư trên. 
    Tập hợp tất cả các nghiệm là:
    $$X = \{1, 2, 3, \dots, 2026\}$$
    
    **Bước 2: Tính tích $P$ của tất cả các nghiệm**
    
    Tích của tất cả các phần tử trong tập nghiệm chính là giai thừa của $2026$:
    $$P = 1 \times 2 \times 3 \times \dots \times 2026 = 2026!$$
    
    **Bước 3: Áp dụng Định lý Wilson để tìm số dư**
    
    Theo **Định lý Wilson**, với $p$ là số nguyên tố, ta có:
    $$(p - 1)! \equiv -1 \pmod p$$
    
    Áp dụng với $p = 2027$, ta thu được:
    $$2026! \equiv -1 \pmod{2027}$$
    
    Vì $-1 \equiv 2026 \pmod{2027}$, số dư của tích $P$ khi chia cho $2027$ là $2026$.
    
    **Bước 4: Kết luận**
    
    Số dư của $P$ khi chia cho $2027$ là $2026$.
    
    ---
    **👉 Đáp số Câu 66:** `2026`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 67 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 67. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 1009$. Xét tổng các nghịch đảo:
$$S = \sum_{k=1}^{1008} \dfrac{1}{k} = 1 + \dfrac{1}{2} + \dfrac{1}{3} + \dots + \dfrac{1}{1008}$$
Biết rằng tổng $S$ có thể quy đồng và viết dưới dạng phân số tối giản $\dfrac{a}{b}$. Tính số dư của tử số $a$ khi chia cho số nguyên tố $1009$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 67) ---
user_ans_67 = st.text_input("Nhập số dư của tử số a khi chia cho 1009:", key="q67_ans")

if st.button("Kiểm tra đáp án Câu 67", key="q67_check"):
    norm_ans_67 = user_ans_67.strip()
    
    # Đáp án chính xác là 0
    if norm_ans_67 == "0":
        st.success("🎉 Xuất sắc! Bạn đã vận dụng định lý Wolstenholme về tổng điều hòa trong trường nguyên tố một cách đỉnh cao tuyệt đối. Lời giải Câu 67 đã được mở khóa.")
    elif user_ans_67 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 67.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy áp dụng định lý Wolstenholme cho tổng điều hòa modulo số nguyên tố lớn hơn hoặc bằng $5$ ($1009 \ge 5$).")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 67 ---
st.markdown("---")

if 'q67_solution_shown' not in st.session_state:
    st.session_state['q67_solution_shown'] = False

col1_67, col2_67 = st.columns([1, 4])
with col1_67:
    if st.button("Xem lời giải Câu 67", key="q67_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q67_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q67_solution_shown'] = False 

if st.session_state.get('q67_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 67 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Nhận diện định lý Wolstenholme (Wolstenholme's Theorem)**
    
    Trong lý thuyết số học cao cấp, định lý Wolstenholme phát biểu rằng với bất kỳ số nguyên tố $p \ge 5$, tổng điều hòa:
    $$H_{p-1} = \sum_{k=1}^{p-1} \dfrac{1}{k} = 1 + \dfrac{1}{2} + \dots + \dfrac{1}{p-1}$$
    khi quy đồng mẫu số và viết dưới dạng phân số tối giản $\dfrac{a}{b}$, thì tử số $a$ phải chia hết cho $p^2$. 
    Nói cách khác, ta có đồng dư thức modulo $p^2$:
    $$\sum_{k=1}^{p-1} \dfrac{1}{k} \equiv 0 \pmod{p^2}$$
    
    **Bước 2: Áp dụng vào bài toán với $p = 1009$**
    
    Vì $1009$ là một số nguyên tố lớn hơn $5$, ta áp dụng trực tiếp định lý Wolstenholme cho $p = 1009$:
    $$\sum_{k=1}^{1008} \dfrac{1}{k} \equiv 0 \pmod{1009^2}$$
    
    Điều này đồng nghĩa với việc tổng $S$ quy đồng thành phân số tối giản $\dfrac{a}{b}$ sẽ có tử số $a$ chia hết cho $1009^2$, suy ra $a$ đặc biệt chia hết cho $1009$.
    
    **Bước 3: Kết luận**
    
    Số dư của tử số $a$ khi chia cho số nguyên tố $1009$ bằng $0$.
    
    ---
    **👉 Đáp số Câu 67:** `0`
    """)

st.markdown("---")


# ==========================================
# CÂU 68: TỔNG GIAI THỪA VÀ ĐỒNG DƯ THỨC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 68 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho tổng số học $S = 1! + 2! + 3! + \dots + 2026!$. Tìm số dư khi chia số $S$ cho $7$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_68 = st.text_input("Nhập số dư của phép chia:", key="q68_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q68_check"):
    normalized_user_answer_68 = user_answer_68.strip().replace(',', '.')
    
    if normalized_user_answer_68 == "5":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_68 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Từ $7!$ trở đi, các số hạng đều chia hết cho $7$, hãy tính tổng các số hạng từ $1!$ đến $6!$ theo mô-đun $7$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q68_solution_shown' not in st.session_state:
    st.session_state['q68_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q68_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q68_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q68_solution_shown'] = False 

if st.session_state.get('q68_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Đánh giá các số hạng theo mô-đun $7$**
    
    Ta cần tìm số dư của $S = 1! + 2! + 3! + \dots + 2026!$ khi chia cho $7$.
    *   Với mọi số nguyên $k \ge 7$, tích $k! = 1 \times 2 \times \dots \times 7 \times \dots \times k$ chứa thừa số $7$ nên $k! \vdots 7$.
    *   Do đó, từ $7!$ đến $2026!$ đều chia hết cho $7$, tức là:
        $$7! \equiv 8! \equiv \dots \equiv 2026! \equiv 0 \pmod 7$$
        
    **Bước 2: Thu gọn tổng $S$**
    
    Số dư của $S$ khi chia cho $7$ chỉ phụ thuộc vào tổng các số hạng từ $1!$ đến $6!$:
    $$S \equiv 1! + 2! + 3! + 4! + 5! + 6! \pmod 7$$
    
    **Bước 3: Tính giá trị từng số hạng modulo $7$**
    
    *   $1! = 1 \equiv 1 \pmod 7$
    *   $2! = 2 \equiv 2 \pmod 7$
    *   $3! = 6 \equiv 6 \pmod 7$
    *   $4! = 24 = 3 \times 7 + 3 \equiv 3 \pmod 7$
    *   $5! = 120 = 17 \times 7 + 1 \equiv 1 \pmod 7$
    *   $6! = 720 = 102 \times 7 + 6 \equiv 6 \pmod 7$ (hoặc theo Định lý Wilson: $6! \equiv -1 \equiv 6 \pmod 7$)
    
    **Bước 4: Tổng hợp kết quả**
    
    Cộng các số dư lại ta được:
    $$S \equiv 1 + 2 + 6 + 3 + 1 + 6 = 19$$
    
    Thực hiện phép chia $19$ cho $7$:
    $$19 = 2 \times 7 + 5 \equiv 5 \pmod 7$$
    
    **Kết luận:** Số dư của phép chia $S$ cho $7$ là **$5$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 69: PHƯƠNG TRÌNH TRÙNG PHƯƠNG VÀ CẤP SỐ CỘNG
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 69 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho phương trình trùng phương $x^4 - 100x^2 + m = 0$ (với $m$ là tham số thực). Biết rằng phương trình có bốn nghiệm phân biệt lập thành một cấp số cộng. Tính giá trị của tham số $m$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_69 = st.text_input("Nhập giá trị của m:", key="q69_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q69_check"):
    normalized_user_answer_69 = user_answer_69.strip().replace(',', '.')
    
    if normalized_user_answer_69 == "900":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_69 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy đặt ẩn phụ $t = x^2$, thiết lập mối quan hệ giữa các nghiệm và áp dụng định lý Vi-et nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q69_solution_shown' not in st.session_state:
    st.session_state['q69_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q69_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q69_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q69_solution_shown'] = False 

if st.session_state.get('q69_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Đặt ẩn phụ và điều kiện có nghiệm**
    
    Đặt $t = x^2$ ($t \ge 0$). Phương trình trở thành:
    $$t^2 - 100t + m = 0 \quad (1)$$
    
    Để phương trình ban đầu có bốn nghiệm phân biệt, phương trình $(1)$ phải có hai nghiệm dương phân biệt $0 < t_1 < t_2$. 
    Khi đó, bốn nghiệm của phương trình theo thứ tự tăng dần là:
    $$x_1 = -\sqrt{t_2}, \quad x_2 = -\sqrt{t_1}, \quad x_3 = \sqrt{t_1}, \quad x_4 = \sqrt{t_2}$$
    
    **Bước 2: Thiết lập điều kiện lập thành cấp số cộng**
    
    Vì tính đối xứng, bốn nghiệm lập thành một cấp số cộng khi và chỉ khi khoảng cách giữa các nghiệm liên tiếp bằng nhau:
    $$x_2 - x_1 = x_3 - x_2 = x_4 - x_3$$
    $$\Leftrightarrow -\sqrt{t_1} - (-\sqrt{t_2}) = \sqrt{t_1} - (-\sqrt{t_1}) \Leftrightarrow \sqrt{t_2} - \sqrt{t_1} = 2\sqrt{t_1}$$
    $$\Leftrightarrow \sqrt{t_2} = 3\sqrt{t_1} \Leftrightarrow t_2 = 9t_1$$
    
    **Bước 3: Sử dụng định lý Vi-et**
    
    Theo định lý Vi-et cho phương trình $(1)$, ta có:
    $$\begin{cases} t_1 + t_2 = 100 \\ t_1 t_2 = m \end{cases}$$
    
    Thay $t_2 = 9t_1$ vào phương trình tổng nghiệm:
    $$t_1 + 9t_1 = 100 \Leftrightarrow 10t_1 = 100 \Leftrightarrow t_1 = 10$$
    
    Từ đó suy ra:
    $$t_2 = 9 \times 10 = 90$$
    
    **Bước 4: Tính giá trị của $m$**
    
    Thay $t_1 = 10$ và $t_2 = 90$ vào phương trình tích nghiệm:
    $$m = t_1 t_2 = 10 \times 90 = 900$$
    
    (Thỏa mãn điều kiện $\Delta = 100^2 - 4m > 0 \Leftrightarrow 10000 - 3600 > 0$ và hai nghiệm dương).
    
    **Kết luận:** Giá trị của tham số $m$ là **$900$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 70: TOÁN THỰC TẾ SỐ HỌC - ĐỒNG DƯ THỨC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 70 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một nhà máy sản xuất các linh kiện điện tử và đóng gói vào các hộp để xuất kho. Nếu đóng gói mỗi hộp $12$ cái thì thừa $5$ cái; nếu đóng gói mỗi hộp $15$ cái thì thừa $8$ cái; nếu đóng gói mỗi hộp $18$ cái thì thừa $11$ cái. Biết rằng số lượng linh kiện của nhà máy là một số tự nhiên nằm trong khoảng từ $2000$ đến $3000$ cái và chia hết cho $7$. Tính số lượng linh kiện của nhà máy.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_70 = st.text_input("Nhập số lượng linh kiện:", key="q70_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q70_check"):
    normalized_user_answer_70 = user_answer_70.strip().replace(',', '.')
    
    if normalized_user_answer_70 == "2513":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_70 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy nhận xét phần bù số dư của các phép chia đều bằng $7$ ($12-5 = 7$, $15-8 = 7$, $18-11 = 7$), tìm bội chung nhỏ nhất và kết hợp điều kiện chia hết cho $7$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q70_solution_shown' not in st.session_state:
    st.session_state['q70_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q70_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q70_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q70_solution_shown'] = False 

if st.session_state.get('q70_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Gọi $N$ là số lượng linh kiện của nhà máy ($2000 \le N \le 3000$, $N \in \mathbb{N}$).
    Theo giả thiết, ta có các điều kiện đồng dư sau:
    *   $N \equiv 5 \pmod{12} \iff N + 7 \equiv 0 \pmod{12}$
    *   $N \equiv 8 \pmod{15} \iff N + 7 \equiv 0 \pmod{15}$
    *   $N \equiv 11 \pmod{18} \iff N + 7 \equiv 0 \pmod{18}$
    
    Từ đó suy ra $(N + 7)$ đồng thời chia hết cho $12, 15$ và $18$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất (BCNN)**
    
    Phân tích ra thừa số nguyên tố:
    *   $12 = 2^2 \times 3$
    *   $15 = 3 \times 5$
    *   $18 = 2 \times 3^2$
    
    Bội chung nhỏ nhất của chúng là:
    $$\text{BCNN}(12, 15, 18) = 2^2 \times 3^2 \times 5 = 180$$
    
    Do đó, ta có dạng tổng quát của $N$:
    $$N + 7 = 180k \implies N = 180k - 7 \quad (k \in \mathbb{N}^*)$$
    
    **Bước 3: Sử dụng điều kiện khoảng giá trị của $N$**
    
    Vì $2000 \le N \le 3000$, ta thay biểu thức của $N$ vào:
    $$2000 \le 180k - 7 \le 3000 \Leftrightarrow 2007 \le 180k \le 3007$$
    $$\Leftrightarrow 11,15 \le k \le 16,7$$
    
    Vì $k$ là số nguyên, ta suy ra $k \in \{12, 13, 14, 15, 16\}$.
    
    **Bước 4: Sử dụng điều kiện chia hết cho $7$**
    
    Theo bài toán, $N$ chia hết cho $7$, tức là:
    $$180k - 7 \equiv 0 \pmod 7$$
    
    Thu gọn hệ số theo mô-đun $7$:
    $$180 = 25 \times 7 + 5 \equiv 5 \pmod 7$$
    $$-7 \equiv 0 \pmod 7$$
    
    Phương trình đồng dư trở thành:
    $$5k \equiv 0 \pmod 7 \iff k \equiv 0 \pmod 7$$
    
    Vì $k \in \{12, 13, 14, 15, 16\}$, giá trị duy nhất chia hết cho $7$ là $k = 14$.
    
    **Bước 5: Tính giá trị chính xác của $N$**
    
    Thay $k = 14$ vào biểu thức của $N$:
    $$N = 180 \times 14 - 7 = 2520 - 7 = 2513$$
    
    Giá trị $2513$ thỏa mãn toàn bộ điều kiện bài toán ($2000 \le 2513 \le 3000$ và chia hết cho $7$).
    
    **Kết luận:** Số lượng linh kiện của nhà máy là **$2513$**.
    """)
    
st.markdown("---")





# =====================================================================
# CÂU HỎI SỐ 71 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 71. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số dư của phép chia khi chia số $7^{2026}$ cho $1000$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 71) ---
user_ans_71 = st.text_input("Nhập số dư khi chia cho 1000:", key="q71_ans")

if st.button("Kiểm tra đáp án Câu 71", key="q71_check"):
    norm_ans_71 = user_ans_71.strip()
    
    # Đáp án chính xác là 649
    if norm_ans_71 == "649":
        st.success("🎉 Xuất sắc! Bạn đã vận dụng Định lý Euler để thu gọn số mũ cực kỳ chính xác. Lời giải Câu 71 đã được mở khóa.")
    elif user_ans_71 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 71.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Tính hàm số Euler $\phi(1000) = 400$, sau đó áp dụng định lý Euler để hạ số mũ $2026$ xuống modulo $400$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 71 ---
st.markdown("---")

if 'q71_solution_shown' not in st.session_state:
    st.session_state['q71_solution_shown'] = False

col1_71, col2_71 = st.columns([1, 4])
with col1_71:
    if st.button("Xem lời giải Câu 71", key="q71_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q71_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q71_solution_shown'] = False 

if st.session_state.get('q71_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 71 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Tính giá trị hàm số Euler $\phi(1000)$**
    
    Phân tích mẫu số ra thừa số nguyên tố:
    $$1000 = 10^3 = 2^3 \times 5^3$$
    
    Áp dụng công thức tính hàm số Euler:
    $$\phi(1000) = 1000 \times \left(1 - \dfrac{1}{2}\right) \times \left(1 - \dfrac{1}{5}\right) = 1000 \times \dfrac{1}{2} \times \dfrac{4}{5} = 400$$
    
    **Bước 2: Áp dụng Định lý Euler để thu gọn số mũ**
    
    Vì $\gcd(7, 1000) = 1$, theo Định lý Euler ta có:
    $$7^{400} \equiv 1 \pmod{1000}$$
    
    Chia số mũ $2026$ cho $\phi(1000) = 400$:
    $$2026 = 400 \times 5 + 26$$
    
    Do đó:
    $$7^{2026} = (7^{400})^5 \times 7^{26} \equiv 1^5 \times 7^{26} \equiv 7^{26} \pmod{1000}$$
    
    **Bước 3: Tính toán giá trị của $7^{26} \pmod{1000}$**
    
    Sử dụng phương pháp bình phương có lặp (lũy thừa nhị phân):
    *   $7^2 = 49 \pmod{1000}$
    *   $7^4 = 49^2 = 2401 \equiv 401 \pmod{1000}$
    *   $7^8 \equiv 401^2 = 160801 \equiv 801 \pmod{1000}$
    *   $7^{16} \equiv 801^2 = 641601 \equiv 601 \pmod{1000}$
    
    Kết hợp các số mũ để tính $7^{26} = 7^{16} \times 7^8 \times 7^2$:
    $$7^{26} \equiv 601 \times 801 \times 49 \pmod{1000}$$
    $$601 \times 801 = 481401 \equiv 401 \pmod{1000}$$
    $$401 \times 49 = 19649 \equiv 649 \pmod{1000}$$
    
    **Bước 4: Kết luận**
    
    Số dư của phép chia là $649$.
    
    ---
    **👉 Đáp số Câu 71:** `649`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 72 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 72. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số nguyên dương $x$ nhỏ nhất thỏa mãn hệ phương trình đồng dư sau:
$$\begin{cases} x \equiv 2 \pmod 5 \\ x \equiv 3 \pmod 7 \\ x \equiv 2 \pmod{11} \end{cases}$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 72) ---
user_ans_72 = st.text_input("Nhập giá trị của x:", key="q72_ans")

if st.button("Kiểm tra đáp án Câu 72", key="q72_check"):
    norm_ans_72 = user_ans_72.strip()
    
    # Đáp án chính xác là 332
    if norm_ans_72 == "332":
        st.success("🎉 Xuất sắc! Bạn đã giải hệ đồng dư bằng Định lý phần dư Trung Hoa một cách hoàn hảo. Lời giải Câu 72 đã được mở khóa.")
    elif user_ans_72 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 72.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Sử dụng Định lý phần dư Trung Hoa (Chinese Remainder Theorem) với các mô-đun đôi một nguyên tố cùng nhau $5, 7, 11$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 72 ---
st.markdown("---")

if 'q72_solution_shown' not in st.session_state:
    st.session_state['q72_solution_shown'] = False

col1_72, col2_72 = st.columns([1, 4])
with col1_72:
    if st.button("Xem lời giải Câu 72", key="q72_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q72_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q72_solution_shown'] = False 

if st.session_state.get('q72_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 72 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Kiểm tra điều kiện của Định lý phần dư Trung Hoa**
    
    Hệ phương trình đồng dư gồm các mô-đun:
    $$m_1 = 5, \quad m_2 = 7, \quad m_3 = 11$$
    Các số này đôi một nguyên tố cùng nhau. Tích của các mô-đun là:
    $$N = 5 \times 7 \times 11 = 385$$
    
    **Bước 2: Tìm nghiệm cơ sở cho từng phương trình thành phần**
    
    Ta tính các giá trị $N_i = \dfrac{N}{m_i}$ và tìm nghịch đảo mô-đun tương ứng:
    1.  **Với phương trình 1 ($x \equiv 2 \pmod 5$):**
        *   $N_1 = \dfrac{385}{5} = 77$
        *   Ta có $77 \equiv 2 \pmod 5$. Nghịch đảo của $2$ modulo $5$ là $3$ (vì $2 \times 3 = 6 \equiv 1 \pmod 5$).
        *   Thành phần thứ nhất: $2 \times 77 \times 3 = 462$.
        
    2.  **Với phương trình 2 ($x \equiv 3 \pmod 7$):**
        *   $N_2 = \dfrac{385}{7} = 55$
        *   Ta có $55 \equiv 6 \pmod 7$. Nghịch đảo của $6$ modulo $7$ là $6$ (vì $6 \times 6 = 36 \equiv 1 \pmod 7$).
        *   Thành phần thứ hai: $3 \times 55 \times 6 = 990$.
        
    3.  **Với phương trình 3 ($x \equiv 2 \pmod{11}$):**
        *   $N_3 = \dfrac{385}{11} = 35$
        *   Ta có $35 \equiv 2 \pmod{11}$. Nghịch đảo của $2$ modulo $11$ là $6$ (vì $2 \times 6 = 12 \equiv 1 \pmod{11}$).
        *   Thành phần thứ ba: $2 \times 35 \times 6 = 420$.
        
    **Bước 3: Tổng hợp nghiệm tổng quát**
    
    Nghiệm tổng quát của hệ có dạng:
    $$x \equiv 462 + 990 + 420 \pmod{385}$$
    $$x \equiv 1872 \pmod{385}$$
    
    Rút gọn số dư trong khoảng từ $0$ đến $384$:
    $$1872 = 385 \times 4 + 332$$
    
    Do đó, nghiệm nguyên dương nhỏ nhất của hệ là $332$.
    
    **Bước 4: Kết luận**
    
    Số nguyên dương $x$ nhỏ nhất thỏa mãn là $332$.
    
    ---
    **👉 Đáp số Câu 72:** `332`
    """)

st.markdown("---")



# ==========================================
# CÂU 73: SỐ HỌC VẬN DỤNG CAO - ĐỒNG DƯ THỨC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 73 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 2011$. Xét số các giá trị nguyên dương $n$ thuộc đoạn $[1; 2010]$ sao cho phương trình đồng dư $x^3 \equiv n \pmod{2011}$ có đúng $3$ nghiệm phân biệt thuộc tập hợp $\{1, 2, \dots, 2010\}$. 

Hỏi có bao nhiêu giá trị của $n$ thỏa mãn điều kiện trên?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_73 = st.text_input("Nhập số lượng giá trị của n:", key="q73_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q73_check"):
    normalized_user_answer_73 = user_answer_73.strip().replace(',', '.')
    
    if normalized_user_answer_73 == "670":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_73 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy sử dụng lý thuyết thặng dư bậc ba trong số học và tính chất của nhóm nhân modulo nguyên tố nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q73_solution_shown' not in st.session_state:
    st.session_state['q73_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q73_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q73_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q73_solution_shown'] = False 

if st.session_state.get('q73_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích điều kiện số nghiệm của phương trình đồng dư**
    
    Xét phương trình đồng dư bậc ba:
    $$x^3 \equiv n \pmod p$$
    với $p = 2011$ là số nguyên tố và $1 \le n \le p-1$.
    
    Theo lý thuyết thặng dư lũy thừa, phương trình $x^k \equiv n \pmod p$ có số nghiệm là $\gcd(k, p-1)$ nếu $n^{\dfrac{p-1}{\gcd(k, p-1)}} \equiv 1 \pmod p$, và có $0$ nghiệm nếu ngược lại (với $n \not\equiv 0 \pmod p$).
    
    **Bước 2: Áp dụng vào bài toán**
    
    Ở đây $k = 3$ và $p = 2011$. Ta tính ước chung lớn nhất:
    $$\gcd(3, p-1) = \gcd(3, 2010) = 3$$
    (vì tổng các chữ số của $2010$ là $3$, chia hết cho $3$).
    
    Do đó, phương trình $x^3 \equiv n \pmod{2011}$ sẽ có đúng $3$ nghiệm phân biệt khi và chỉ khi $n$ là thặng dư bậc ba thực sự, tức là thỏa mãn điều kiện:
    $$n^{\dfrac{2010}{3}} \equiv 1 \pmod{2011} \iff n^{670} \equiv 1 \pmod{2011}$$
    
    **Bước 3: Tính số lượng các giá trị của $n$**
    
    Số lượng các thặng dư bậc ba phân biệt trong hệ thặng dư thu gọn modulo $p$ được xác định bởi công thức:
    $$\dfrac{p-1}{\gcd(3, p-1)} = \dfrac{2010}{3} = 670$$
    
    Vậy có đúng $670$ giá trị của $n$ trong đoạn $[1; 2010]$ thỏa mãn yêu cầu bài toán.
    
    **Kết luận:** Số lượng giá trị của $n$ là **$670$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 74: ĐẠI SỐ NÂNG CAO - ĐA THỨC VÀ ĐẠO HÀM
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 74 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho đa thức $P(x) = x^{2026} + a_1 x^{2025} + a_2 x^{2024} + \dots + a_{2025}x + a_{2026}$ có $2026$ nghiệm thực phân biệt $x_1, x_2, \dots, x_{2026}$. Tính giá trị của biểu thức:
$$S = \dfrac{1}{P'(x_1)} + \dfrac{1}{P'(x_2)} + \dfrac{1}{P'(x_3)} + \dots + \dfrac{1}{P'(x_{2026})}$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_74 = st.text_input("Nhập giá trị của S:", key="q74_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q74_check"):
    normalized_user_answer_74 = user_answer_74.strip().replace(',', '.')
    
    if normalized_user_answer_74 == "0":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_74 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích hàm phân thức $\dfrac{1}{P(x)}$ thành tổng các phân thức đơn giản hoặc xét giới hạn khi $x \to \infty$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q74_solution_shown' not in st.session_state:
    st.session_state['q74_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q74_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q74_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q74_solution_shown'] = False 

if st.session_state.get('q74_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích đa thức thành nhân tử**
    
    Vì đa thức $P(x)$ có hệ số cao nhất bằng $1$ và có $2026$ nghiệm thực phân biệt $x_1, x_2, \dots, x_{2026}$, ta viết lại dưới dạng:
    $$P(x) = \prod_{i=1}^{2026} (x - x_i)$$
    
    **Bước 2: Sử dụng khai triển phân thức tối giản (Lagrange)**
    
    Xét hàm số phân thức hữu tỉ:
    $$F(x) = \dfrac{1}{P(x)}$$
    Vì bậc của tử số bằng $0$ và bậc của mẫu số bằng $2026 \ge 2$, ta có thể phân tích $F(x)$ thành tổng các phân thức đơn giản:
    $$\dfrac{1}{P(x)} = \sum_{i=1}^{2026} \dfrac{1}{P'(x_i)(x - x_i)}$$
    
    **Bước 3: Xét giới hạn để tìm tổng các nghịch đảo đạo hàm**
    
    Nhân cả hai vế với $x$, ta được:
    $$\dfrac{x}{P(x)} = \sum_{i=1}^{2026} \dfrac{x}{P'(x_i)(x - x_i)}$$
    
    Lấy giới hạn khi $x \to \infty$:
    *   Vế trái: $\lim_{x \to \infty} \dfrac{x}{P(x)} = \lim_{x \to \infty} \dfrac{x}{x^{2026} + \dots} = 0$ (vì bậc mẫu lớn hơn bậc tử).
    *   Vế phải: $\lim_{x \to \infty} \sum_{i=1}^{2026} \dfrac{x}{P'(x_i)(x - x_i)} = \sum_{i=1}^{2026} \dfrac{1}{P'(x_i)}$.
    
    Từ đó suy ra:
    $$\sum_{i=1}^{2026} \dfrac{1}{P'(x_i)} = 0$$
    
    **Kết luận:** Giá trị của biểu thức $S$ là **$0$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 75: SỐ HỌC VẬN DỤNG CAO - HỆ ĐỒNG DƯ THỨC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 75 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm một số nguyên dương $n$ nằm trong khoảng $[2000; 5000]$ sao cho khi chia $n$ cho các số $11, 13, 17$ đều dư $5$, đồng thời $n$ chia hết cho $7$. 

Hãy nhập giá trị của $n$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_75 = st.text_input("Nhập giá trị của n:", key="q75_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q75_check"):
    normalized_user_answer_75 = user_answer_75.strip().replace(',', '.')
    
    if normalized_user_answer_75 == "2436":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_75 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thiết lập hệ đồng dư thức cho $n - 5$, tìm BCNN của các mô-đun và kết hợp điều kiện chia hết cho 7 nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q75_solution_shown' not in st.session_state:
    st.session_state['q75_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q75_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q75_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q75_solution_shown'] = False 

if st.session_state.get('q75_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập hệ đồng dư thức**
    
    Theo giả thiết, số nguyên dương $n$ thỏa mãn các điều kiện:
    *   $n \equiv 5 \pmod{11} \iff n - 5 \vdots 11$
    *   $n \equiv 5 \pmod{13} \iff n - 5 \vdots 13$
    *   $n \equiv 5 \pmod{17} \iff n - 5 \vdots 17$
    
    Từ đó suy ra $(n - 5)$ đồng thời chia hết cho các số nguyên tố $11, 13$ và $17$.
    
    **Bước 2: Tìm Bội chung nhỏ nhất (BCNN)**
    
    Vì $11, 13, 17$ đôi một nguyên tố cùng nhau, ta có:
    $$\text{BCNN}(11, 13, 17) = 11 \times 13 \times 17 = 2431$$
    
    Do đó, dạng tổng quát của $n$ là:
    $$n - 5 = 2431k \iff n = 2431k + 5 \quad (k \in \mathbb{N}^*)$$
    
    **Bước 3: Sử dụng điều kiện khoảng giá trị của $n$**
    
    Vì $2000 \le n \le 5000$, ta có:
    $$2000 \le 2431k + 5 \le 5000 \iff 1995 \le 2431k \le 4995 \iff 0,82 \le k \le 2,05$$
    
    Vì $k$ là số nguyên dương ($k \in \mathbb{N}^*$), ta chọn duy nhất $k = 1$.
    
    **Bước 4: Kiểm tra điều kiện chia hết cho 7**
    
    Với $k = 1$, ta tính được:
    $$n = 2431 \times 1 + 5 = 2436$$
    
    Kiểm tra tính chia hết cho $7$:
    $$2436 \div 7 = 348 \quad (\text{chia hết hoàn toàn})$$
    
    Giá trị này hoàn toàn nằm trong khoảng $[2000; 5000]$ và thỏa mãn tất cả các yêu cầu của bài toán.
    
    **Kết luận:** Giá trị của $n$ là **$2436$**.
    """)
    
st.markdown("---")




# =====================================================================
# CÂU HỎI SỐ 76 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 76. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên $N = 3^{2026} + 5^{2026}$. Tính số dư của $N$ khi chia cho số nguyên tố $13$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 76) ---
user_ans_76 = st.text_input("Nhập số dư của N khi chia cho 13:", key="q76_ans")

if st.button("Kiểm tra đáp án Câu 76", key="q76_check"):
    norm_ans_76 = user_ans_76.strip()
    
    # Đáp án chính xác là 2
    if norm_ans_76 == "2":
        st.success("🎉 Xuất sắc! Bạn đã vận dụng thành thạo tính chất đồng dư và cấp của số nguyên modulo một số nguyên tố. Lời giải Câu 76 đã được mở khóa.")
    elif user_ans_76 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 76.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy xét riêng số dư của từng lũy thừa $3^{2026}$ và $5^{2026}$ khi chia cho $13$ bằng cách tìm chu kỳ tuần hoàn của số mũ.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 76 ---
st.markdown("---")

if 'q76_solution_shown' not in st.session_state:
    st.session_state['q76_solution_shown'] = False

col1_76, col2_76 = st.columns([1, 4])
with col1_76:
    if st.button("Xem lời giải Câu 76", key="q76_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q76_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q76_solution_shown'] = False 

if st.session_state.get('q76_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 76 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Xét số dư của số hạng thứ nhất $3^{2026}$ khi chia cho $13$**
    
    Ta tính các lũy thừa của $3$ modulo $13$:
    *   $3^1 \equiv 3 \pmod{13}$
    *   $3^2 \equiv 9 \pmod{13}$
    *   $3^3 = 27 \equiv 1 \pmod{13}$
    
    Vì $3^3 \equiv 1 \pmod{13}$, chu kỳ lặp lại của số dư là $3$. Ta chia số mũ $2026$ cho $3$:
    $$2026 = 3 \times 675 + 1$$
    
    Do đó:
    $$3^{2026} = (3^3)^{675} \times 3^1 \equiv 1^{675} \times 3 \equiv 3 \pmod{13}$$
    
    **Bước 2: Xét số dư của số hạng thứ hai $5^{2026}$ khi chia cho $13$**
    
    Ta tính các lũy thừa của $5$ modulo $13$:
    *   $5^1 \equiv 5 \pmod{13}$
    *   $5^2 = 25 \equiv -1 \pmod{13}$
    *   $5^4 \equiv (-1)^2 = 1 \pmod{13}$
    
    Vì $5^4 \equiv 1 \pmod{13}$, chu kỳ lặp lại của số dư là $4$. Ta chia số mũ $2026$ cho $4$:
    $$2026 = 4 \times 506 + 2$$
    
    Do đó:
    $$5^{2026} = (5^4)^{506} \times 5^2 \equiv 1^{506} \times (-1) \equiv -1 \pmod{13}$$
    
    **Bước 3: Tổng hợp kết quả**
    
    Thay các giá trị vừa tìm được vào biểu thức $N$:
    $$N = 3^{2026} + 5^{2026} \equiv 3 + (-1) = 2 \pmod{13}$$
    
    **Bước 4: Kết luận**
    
    Số dư của $N$ khi chia cho $13$ là $2$.
    
    ---
    **👉 Đáp số Câu 76:** `2`
    """)

st.markdown("---")

# =====================================================================
# CÂU HỎI SỐ 77 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 77. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên tố $p = 2027$. Tính số lượng các số nguyên $x$ thuộc đoạn $[1, 2026]$ thỏa mãn phương trình đồng dư:
$$x^2 + x + 1 \equiv 0 \pmod{2027}$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 77) ---
user_ans_77 = st.text_input("Nhập số lượng nghiệm nguyên thỏa mãn:", key="q77_ans")

if st.button("Kiểm tra đáp án Câu 77", key="q77_check"):
    norm_ans_77 = user_ans_77.strip()
    
    # Đáp án chính xác là 0
    if norm_ans_77 == "0":
        st.success("🎉 Xuất sắc! Bạn đã nhìn thấu mối liên hệ giữa đa thức bậc hai và nghiệm của đơn vị bậc ba dựa trên điều kiện chia hết của mô-đun. Lời giải Câu 77 đã được mở khóa.")
    elif user_ans_77 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 77.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Nhân cả hai vế của phương trình với $x - 1$ để đưa về phương trình $x^3 \equiv 1 \pmod p$, sau đó kiểm tra điều kiện $3 \mid (p-1)$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 77 ---
st.markdown("---")

if 'q77_solution_shown' not in st.session_state:
    st.session_state['q77_solution_shown'] = False

col1_77, col2_77 = st.columns([1, 4])
with col1_77:
    if st.button("Xem lời giải Câu 77", key="q77_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q77_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q77_solution_shown'] = False 

if st.session_state.get('q77_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 77 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Biến đổi đại số phương trình đồng dư**
    
    Xét phương trình đồng dư:
    $$x^2 + x + 1 \equiv 0 \pmod{2027}$$
    
    Nhân cả hai vế với biểu thức $x - 1$ (với lưu ý $x \not\equiv 1 \pmod{2027}$, vì nếu $x \equiv 1$ thì $1^2 + 1 + 1 = 3 \not\equiv 0 \pmod{2027}$):
    $$(x - 1)(x^2 + x + 1) \equiv 0 \pmod{2027} \iff x^3 \equiv 1 \pmod{2027}$$
    
    **Bước 2: Kiểm tra điều kiện tồn tại nghiệm của phương trình bậc ba**
    
    Trong trường hữu hạn modulo số nguyên tố $p = 2027$, phương trình $x^3 \equiv 1 \pmod p$ có các nghiệm khác $1$ khi và chỉ khi số nguyên tố $p$ thỏa mãn điều kiện **$3$ chia hết cho $p - 1$** (tức là $3 \mid (p - 1)$).
    
    Ta kiểm tra với $p = 2027$:
    $$p - 1 = 2026$$
    Tổng các chữ số của $2026$ là $2 + 0 + 2 + 6 = 10$, không chia hết cho $3$. Do đó $3 \nmid 2026$.
    
    **Bước 3: Kết luận**
    
    Vì $3$ không là ước của $p - 1$, phương trình $x^3 \equiv 1 \pmod{2027}$ chỉ có nghiệm duy nhất là $x \equiv 1 \pmod{2027}$. Tuy nhiên, $x = 1$ không thỏa mãn phương trình ban đầu ($1^2 + 1 + 1 = 3 \neq 0$).
    
    Vậy phương trình đồng dư đã cho **không có nghiệm nào** thuộc đoạn $[1, 2026]$. Số lượng nghiệm bằng $0$.
    
    ---
    **👉 Đáp số Câu 77:** `0`
    """)

st.markdown("---")





# ==========================================
# CÂU 78: PHƯƠNG TRÌNH NGHIỆM NGUYÊN
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 78 (TSA 2026 - Chuyên đề Số học)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho phương trình $\dfrac{1}{x} + \dfrac{1}{y} = \dfrac{1}{2026}$ với $x, y$ là các số nguyên dương. Hỏi có bao nhiêu cặp số nguyên dương $(x, y)$ với $x \le y$ thỏa mãn phương trình trên?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_78 = st.text_input("Nhập số lượng cặp nghiệm $(x, y)$:", key="q78_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q78_check"):
    normalized_user_answer_78 = user_answer_78.strip().replace(',', '.')
    
    if normalized_user_answer_78 == "9":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_78 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy biến đổi phương trình về dạng nhân tử $(x - 2026)(y - 2026) = 2026^2$ để đếm số ước số nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q78_solution_shown' not in st.session_state:
    st.session_state['q78_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q78_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q78_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q78_solution_shown'] = False 

if st.session_state.get('q78_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biến đổi phương trình về dạng tích**
    
    Ta có phương trình ban đầu:
    $$\dfrac{1}{x} + \dfrac{1}{y} = \dfrac{1}{2026}$$
    
    Quy đồng mẫu số và nhân chéo, ta được:
    $$2026(x + y) = xy \iff xy - 2026x - 2026y = 0$$
    
    Thêm $2026^2$ vào hai vế để phân tích thành nhân tử:
    $$xy - 2026x - 2026y + 2026^2 = 2026^2$$
    $$x(y - 2026) - 2026(y - 2026) = 2026^2$$
    $$(x - 2026)(y - 2026) = 2026^2$$
    
    **Bước 2: Phân tích thừa số nguyên tố của $2026^2$**
    
    Ta có phân tích ra thừa số nguyên tố của $2026$:
    $$2026 = 2 \times 1013$$
    (với $1013$ là một số nguyên tố).
    
    Do đó:
    $$2026^2 = 2^2 \times 1013^2$$
    
    Số các ước số nguyên dương của $2026^2$ được tính bằng công thức:
    $$d(2026^2) = (2 + 1)(2 + 1) = 3 \times 3 = 9$$
    
    **Bước 3: Đếm số cặp nghiệm thỏa mãn điều kiện $x \le y$**
    
    Vì $x, y$ là các số nguyên dương và $x \le y$, nên ta suy ra $x - 2026 \le y - 2026$. 
    Do tích $(x - 2026)(y - 2026) = 2026^2 > 0$, hai nhân tử này phải cùng dấu và vì $x \le y$ nên cả hai nhân tử phải là các ước nguyên dương của $2026^2$.
    
    Ứng với mỗi ước nguyên dương của $2026^2$, ta xác định được duy nhất một cặp $(x, y)$. Vì tổng số ước nguyên dương là $9$, nên có đúng $9$ cặp nghiệm $(x, y)$ thỏa mãn.
    
    **Kết luận:** Số lượng cặp nghiệm nguyên dương thỏa mãn là **$9$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 79: ĐỊNH LÝ LEGENDRE VÀ GIAI THỪA
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 79 (TSA 2026 - Chuyên đề Số học)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số chữ số $0$ tận cùng của số $S = 2026!$ khi viết dưới dạng số thập phân.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_79 = st.text_input("Nhập số lượng chữ số 0 tận cùng:", key="q79_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q79_check"):
    normalized_user_answer_79 = user_answer_79.strip().replace(',', '.')
    
    if normalized_user_answer_79 == "505":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_79 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy sử dụng Định lý Legendre để tính số mũ của thừa số 5 trong phân tích tiêu chuẩn của $2026!$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q79_solution_shown' not in st.session_state:
    st.session_state['q79_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q79_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q79_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q79_solution_shown'] = False 

if st.session_state.get('q79_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích bản chất số chữ số 0 tận cùng**
    
    Số chữ số $0$ tận cùng của một số nguyên dương chính bằng số thừa số nguyên tố $10$ trong phân tích tiêu chuẩn của số đó. 
    Vì $10 = 2 \times 5$ và trong dãy từ $1$ đến $2026$, số lượng thừa số $2$ luôn lớn hơn rất nhiều so với số lượng thừa số $5$, nên số chữ số $0$ tận cùng của $2026!$ đúng bằng số mũ của thừa số $5$ trong phân tích tiêu chuẩn của $2026!$.
    
    **Bước 2: Áp dụng Định lý Legendre**
    
    Số mũ của số nguyên tố $p$ trong phân tích tiêu chuẩn của $n!$ được tính bởi công thức Legendre:
    $$v_p(n!) = \sum_{k=1}^{\infty} \left\lfloor \dfrac{n}{p^k} \right\rfloor$$
    
    Với $n = 2026$ và $p = 5$, ta tính các thương số phần nguyên:
    *   $\left\lfloor \dfrac{2026}{5} \right\rfloor = 405$
    *   $\left\lfloor \dfrac{2026}{25} \right\rfloor = 81$
    *   $\left\lfloor \dfrac{2026}{125} \right\rfloor = 16$
    *   $\left\lfloor \dfrac{2026}{625} \right\rfloor = 3$
    *   Với $p^k = 3125 > 2026$, các thương số tiếp theo bằng $0$.
    
    **Bước 3: Tính tổng số lượng thừa số 5**
    
    Cộng các giá trị phần nguyên vừa tìm được:
    $$v_5(2026!) = 405 + 81 + 16 + 3 = 505$$
    
    **Kết luận:** Số chữ số $0$ tận cùng của $2026!$ là **$505$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 80: ĐỒNG DƯ THỨC VÀ ĐỊNH LÝ FERMAT NHỎ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 80 (TSA 2026 - Chuyên đề Số học)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số dư khi chia số nguyên dương $A = 3^{2026} + 2026^3$ cho số nguyên tố $13$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_80 = st.text_input("Nhập số dư của phép chia:", key="q80_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q80_check"):
    normalized_user_answer_80 = user_answer_80.strip().replace(',', '.')
    
    if normalized_user_answer_80 == "8":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_80 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý nhỏ Fermat để thu gọn số mũ của $3^{2026}$ và tính số dư của $2026^3$ theo mô-đun $13$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q80_solution_shown' not in st.session_state:
    st.session_state['q80_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q80_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q80_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q80_solution_shown'] = False 

if st.session_state.get('q80_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính số dư của số hạng $3^{2026}$ theo mô-đun $13$**
    
    Theo Định lý nhỏ Fermat, với $p = 13$ là số nguyên tố và $\text{gcd}(3, 13) = 1$, ta có:
    $$3^{12} \equiv 1 \pmod{13}$$
    
    Thực hiện phép chia số mũ cho chu kỳ $12$:
    $$2026 = 12 \times 168 + 10$$
    
    Do đó:
    $$3^{2026} = (3^{12})^{168} \cdot 3^{10} \equiv 1^{168} \cdot 3^{10} \equiv 3^{10} \pmod{13}$$
    
    Ta tính tiếp giá trị của $3^{10} \pmod{13}$:
    *   $3^3 = 27 \equiv 1 \pmod{13}$
    *   $3^{10} = (3^3)^3 \cdot 3 \equiv 1^3 \cdot 3 = 3 \pmod{13}$
    
    Vậy $3^{2026} \equiv 3 \pmod{13}$.
    
    **Bước 2: Tính số dư của số hạng $2026^3$ theo mô-đun $13$**
    
    Thực hiện phép chia cơ số cho $13$:
    $$2026 = 13 \times 155 + 11 \equiv 11 \equiv -2 \pmod{13}$$
    
    Do đó:
    $$2026^3 \equiv (-2)^3 = -8 \equiv 5 \pmod{13}$$
    
    **Bước 3: Tổng hợp kết quả**
    
    Số dư của biểu thức $A = 3^{2026} + 2026^3$ khi chia cho $13$ là:
    $$A \equiv 3 + 5 = 8 \pmod{13}$$
    
    **Kết luận:** Số dư của phép chia $A$ cho $13$ là **$8$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 81 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 81. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho phương trình nghiệm nguyên dương với các ẩn số $x, y$:
$$x^3 + y^3 + (x + y)^3 + 30xy = 2026$$
Hỏi phương trình trên có tất cả bao nhiêu nghiệm nguyên dương $(x, y)$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 81) ---
user_ans_81 = st.text_input("Nhập số lượng nghiệm nguyên dương của phương trình:", key="q81_ans")

if st.button("Kiểm tra đáp án Câu 81", key="q81_check"):
    norm_ans_81 = user_ans_81.strip()
    
    # Đáp án chính xác là 0
    if norm_ans_81 == "0":
        st.success("🎉 Xuất sắc! Bạn đã kết hợp xuất sắc phép đặt ẩn phụ tổng-tích, điều kiện chia hết và điều kiện miền giá trị delta để chứng minh phương trình vô nghiệm. Lời giải Câu 81 đã được mở khóa.")
    elif user_ans_81 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 81.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy đặt $s = x+y$ và $p = xy$, đưa phương trình về dạng liên hệ giữa $p$ và $s$, sau đó xét tính chia hết kết hợp điều kiện $s^2 \ge 4p$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 81 ---
st.markdown("---")

if 'q81_solution_shown' not in st.session_state:
    st.session_state['q81_solution_shown'] = False

col1_81, col2_81 = st.columns([1, 4])
with col1_81:
    if st.button("Xem lời giải Câu 81", key="q81_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q81_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q81_solution_shown'] = False 

if st.session_state.get('q81_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 81 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Biến đổi phương trình bằng phương pháp tổng - tích**
    
    Đặt $s = x + y$ và $p = xy$. Theo hằng đẳng thức bậc ba, ta có:
    $$x^3 + y^3 = (x + y)^3 - 3xy(x + y) = s^3 - 3sp$$
    
    Thay vào phương trình ban đầu:
    $$(s^3 - 3sp) + s^3 + 30p = 2026$$
    $$2s^3 + (30 - 3s)p = 2026$$
    
    Biểu diễn $p$ theo $s$:
    $$p(3s - 30) = 2s^3 - 2026 \implies p = \dfrac{2s^3 - 2026}{3(s - 10)}$$
    
    **Bước 2: Sử dụng điều kiện nguyên và tính chia hết**
    
    Vì $x, y$ là các số nguyên dương, nên $p$ phải là một số nguyên. Do đó, biểu thức $3(s - 10)$ phải là ước của tử số $2s^3 - 2026$. 
    Biến đổi tử số để xuất hiện nhân tử $(s - 10)$:
    $$2s^3 - 2026 = 2(s^3 - 1000) - 26 = 2(s - 10)(s^2 + 10s + 100) - 26$$
    
    Khi đó:
    $$p = \dfrac{2(s - 10)(s^2 + 10s + 100) - 26}{3(s - 10)} = \dfrac{2}{3}(s^2 + 10s + 100) - \dfrac{26}{3(s - 10)}$$
    
    Để $p$ nguyên, thì $3(s - 10)$ phải là ước của $26$. Các ước nguyên của $26$ là $\pm 1, \pm 2, \pm 13, \pm 26$.
    Suy ra các giá trị có thể của $s - 10$:
    *   $s - 10 = 1 \implies s = 11$. Tử số $2(11^3) - 2026 = 636$ (chia hết cho $3$). Mẫu $3(1) = 3 \implies p = 212$. Kiểm tra điều kiện $s^2 \ge 4p$: $11^2 = 121 < 4(212) = 848$ (Loại).
    *   $s - 10 = -2 \implies s = 8$. Tử số $2(8^3) - 2026 = -1002$ (chia hết cho $3$). Mẫu $3(-2) = -6 \implies p = 167$. Kiểm tra điều kiện $s^2 \ge 4p$: $8^2 = 64 < 4(167) = 668$ (Loại).
    *   $s - 10 = 13 \implies s = 23$. Tử số $2(23^3) - 2026 = 22308$ (chia hết cho $3$). Mẫu $3(13) = 39 \implies p = 572$. Kiểm tra điều kiện $s^2 \ge 4p$: $23^2 = 529 < 4(572) = 2288$ (Loại).
    *   Các trường hợp còn lại hoặc không chia hết cho $3$, hoặc cho giá trị $s \le 0$ (loại vì $s = x + y > 0$).
    
    **Bước 3: Kết luận**
    
    Sau khi kiểm tra toàn bộ các giá trị thỏa mãn điều kiện, không có bộ giá trị nào đồng thời thỏa mãn điều kiện $s^2 \ge 4p$.
    Vậy phương trình đã cho không có nghiệm nguyên dương nào. Số lượng nghiệm bằng $0$.
    
    ---
    **👉 Đáp số Câu 81:** `0`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 82 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 82. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho phương trình nghiệm nguyên:
$$x^2 + y^2 + 5z^2 = 2xy + 2xz + 2yz$$
Xét tất cả các nghiệm nguyên dương $(x, y, z)$ sao cho biến $z$ nhận giá trị nguyên dương nhỏ nhất. Tính giá trị nhỏ nhất của tổng $P = x + y + z$ tương ứng với giá trị $z$ đó.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 82) ---
user_ans_82 = st.text_input("Nhập giá trị nhỏ nhất của tổng P:", key="q82_ans")

if st.button("Kiểm tra đáp án Câu 82", key="q82_check"):
    norm_ans_82 = user_ans_82.strip()
    
    # Đáp án chính xác là 4
    if norm_ans_82 == "4":
        st.success("🎉 Xuất sắc! Bạn đã sử dụng phương pháp biện luận biệt thức Delta đối với phương trình bậc hai một cách hoàn hảo tuyệt đối. Lời giải Câu 82 đã được mở khóa.")
    elif user_ans_82 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 82.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Xem phương trình là phương trình bậc hai ẩn $x$, tính biệt thức $\Delta_x$ và tìm giá trị nguyên dương nhỏ nhất của $z$ là $z = 1$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 82 ---
st.markdown("---")

if 'q82_solution_shown' not in st.session_state:
    st.session_state['q82_solution_shown'] = False

col1_82, col2_82 = st.columns([1, 4])
with col1_82:
    if st.button("Xem lời giải Câu 82", key="q82_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q82_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q82_solution_shown'] = False 

if st.session_state.get('q82_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 82 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Biến đổi phương trình thành phương trình bậc hai theo ẩn $x$**
    
    Viết lại phương trình dưới dạng:
    $$x^2 - 2(y + z)x + (y^2 - 2yz + 5z^2) = 0$$
    
    Để phương trình có nghiệm nguyên $x$, biệt thức $\Delta_x$ (hoặc $\Delta_x / 4$) phải là một số chính phương không âm:
    $$\dfrac{\Delta_x}{4} = (y + z)^2 - (y^2 - 2yz + 5z^2) = y^2 + 2yz + z^2 - y^2 + 2yz - 5z^2 = 4yz - 4z^2$$
    
    Do đó:
    $$4yz - 4z^2 = 4z(y - z) \ge 0 \implies y \ge z$$
    
    **Bước 2: Khảo sát giá trị nguyên dương nhỏ nhất của $z$**
    
    Vì $z$ là số nguyên dương, giá trị nhỏ nhất có thể của $z$ là $z = 1$. 
    Thay $z = 1$ vào phương trình ban đầu, ta được:
    $$x^2 + y^2 + 5 = 2xy + 2x + 2y \iff x^2 - 2(y + 1)x + (y^2 - 2y + 5) = 0$$
    
    Xét biệt thức của phương trình này theo ẩn $x$:
    $$\dfrac{\Delta_x}{4} = (y + 1)^2 - (y^2 - 2y + 5) = y^2 + 2y + 1 - y^2 + 2y - 5 = 4y - 4$$
    
    Để tồn tại nghiệm nguyên $x$, thì $\dfrac{\Delta_x}{4}$ phải là một số chính phương. Đặt $4y - 4 = k^2$ (với $k \ge 0$), suy ra $k$ phải là số chẵn, đặt $k = 2m$:
    $$4(y - 1) = 4m^2 \implies y = m^2 + 1$$
    
    Khi đó, nghiệm $x$ được tính bằng:
    $$x = (y + 1) \pm \sqrt{4m^2} = (m^2 + 1 + 1) \pm 2m = m^2 + 2 \pm 2m = (m \pm 1)^2 + 1$$
    (hoặc xét trực tiếp $x = (y+1) \pm 2m = m^2 + 2 \pm 2m$).
    
    **Bước 3: Tìm các nghiệm nguyên dương ứng với $z = 1$**
    
    *   Với $m = 1$:
        *   $y = 1^2 + 1 = 2$
        *   $x = (1 + 1)^2 + 1 = 5$ hoặc $x = (1 - 1)^2 + 1 = 1$.
        
    Ta kiểm tra hai bộ nghiệm với $z = 1$:
    1.  Bộ $(1, 2, 1)$: $1^2 + 2^2 + 5(1^2) = 10$ và $2(1)(2) + 2(1)(1) + 2(2)(1) = 10$ (Thỏa mãn).
    2.  Bộ $(5, 2, 1)$: $5^2 + 2^2 + 5(1^2) = 34$ và $2(5)(2) + 2(5)(1) + 2(2)(1) = 34$ (Thỏa mãn).
    
    **Bước 4: Tính tổng $P = x + y + z$ và kết luận**
    
    *   Với bộ $(1, 2, 1)$: $P = 1 + 2 + 1 = 4$.
    *   Với bộ $(5, 2, 1)$: $P = 5 + 2 + 1 = 8$.
    
    Giá trị nhỏ nhất của tổng $P$ ứng với giá trị nguyên dương nhỏ nhất của $z$ ($z = 1$) bằng $4$.
    
    ---
    **👉 Đáp số Câu 82:** `4`
    """)

st.markdown("---")



# ==========================================
# CÂU 83: DÃY SỐ VÀ ĐỒNG DƯ THỨC NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 83 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho dãy số $(u_n)$ được xác định bởi $u_1 = 5$, $u_2 = 13$ và hệ thức truy hồi $u_{n+2} = 5u_{n+1} - 6u_n$ với mọi $n \ge 1$. Tìm số dư khi chia số hạng $u_{2026}$ cho $11$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_83 = st.text_input("Nhập số dư của phép chia:", key="q83_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q83_check"):
    normalized_user_answer_83 = user_answer_83.strip().replace(',', '.')
    
    if normalized_user_answer_83 == "1":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_83 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy giải phương trình đặc trưng để tìm số hạng tổng quát của dãy số, sau đó áp dụng Định lý nhỏ Fermat nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q83_solution_shown' not in st.session_state:
    st.session_state['q83_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q83_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q83_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q83_solution_shown'] = False 

if st.session_state.get('q83_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm công thức tổng quát của dãy số**
    
    Phương trình sai phân tuyến tính cấp hai có phương trình đặc trưng:
    $$r^2 - 5r + 6 = 0 \iff (r - 2)(r - 3) = 0 \iff \begin{bmatrix} r = 2 \\ r = 3 \end{bmatrix}$$
    
    Do đó, số hạng tổng quát của dãy số có dạng:
    $$u_n = A \cdot 2^n + B \cdot 3^n$$
    
    Sử dụng điều kiện đầu để tìm các hằng số $A$ và $B$:
    *   Với $n = 1$: $2A + 3B = u_1 = 5$
    *   Với $n = 2$: $4A + 9B = u_2 = 13$
    
    Giải hệ phương trình trên, ta được $A = 1$ và $B = 1$. Vậy công thức tổng quát của dãy số là:
    $$u_n = 2^n + 3^n$$
    
    **Bước 2: Tính số hạng $u_{2026}$ theo mô-đun $11$**
    
    Ta cần tìm số dư của $u_{2026} = 2^{2026} + 3^{2026}$ khi chia cho $11$.
    Theo Định lý nhỏ Fermat, vì $11$ là số nguyên tố nên $2^{10} \equiv 1 \pmod{11}$ và $3^{10} \equiv 1 \pmod{11}$.
    
    Thực hiện chia số mũ cho chu kỳ $10$:
    $$2026 = 10 \times 202 + 6$$
    
    Do đó:
    *   $2^{2026} = (2^{10})^{202} \cdot 2^6 \equiv 1^{202} \cdot 64 \equiv 9 \pmod{11}$ (vì $64 = 5 \times 11 + 9$)
    *   $3^{2026} = (3^{10})^{202} \cdot 3^6 \equiv 1^{202} \cdot 729 \equiv 3 \pmod{11}$ (vì $729 = 66 \times 11 + 3$)
    
    **Bước 3: Tổng hợp kết quả**
    
    Cộng các số dư lại ta được:
    $$u_{2026} \equiv 9 + 3 = 12 \equiv 1 \pmod{11}$$
    
    **Kết luận:** Số dư của phép chia $u_{2026}$ cho $11$ là **$1$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 84: ƯỚC CHUNG LỚN NHẤT VÀ TẬP HỢP SỐ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 84 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bao nhiêu giá trị nguyên dương của $n$ thỏa mãn $1 \le n \le 2026$ sao cho ước chung lớn nhất $\gcd(n^2 + 3n + 5, n + 1) = 1$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_84 = st.text_input("Nhập số lượng giá trị của n:", key="q84_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q84_check"):
    normalized_user_answer_84 = user_answer_84.strip().replace(',', '.')
    
    if normalized_user_answer_84 == "1350":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_84 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy thực hiện phép chia đa thức để rút gọn biểu thức ước chung lớn nhất về một hằng số nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q84_solution_shown' not in st.session_state:
    st.session_state['q84_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q84_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q84_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q84_solution_shown'] = False 

if st.session_state.get('q84_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Rút gọn biểu thức ước chung lớn nhất**
    
    Gọi $d = \gcd(n^2 + 3n + 5, n + 1)$. Ta thực hiện phép chia đa thức:
    $$n^2 + 3n + 5 = (n + 1)(n + 2) + 3$$
    
    Do $d$ là ước của $n^2 + 3n + 5$ và chia hết cho $(n + 1)$, nên $d$ cũng phải là ước của hiệu:
    $$(n^2 + 3n + 5) - (n + 1)(n + 2) = 3$$
    
    Vì vậy, $d$ chỉ có thể nhận các giá trị thuộc tập ước nguyên dương của $3$, tức là $d \in \{1, 3\}$.
    
    **Bước 2: Thiết lập điều kiện để ước chung lớn nhất bằng 1**
    
    Yêu cầu bài toán là $\gcd(n^2 + 3n + 5, n + 1) = 1$, điều này xảy ra khi và chỉ khi $d \neq 3$, tức là $(n + 1)$ **không chia hết cho $3$**.
    
    **Bước 3: Đếm số lượng giá trị của $n$ thỏa mãn**
    
    Xét điều kiện của $n$: $1 \le n \le 2026$. Suy ra miền giá trị của biểu thức $(n + 1)$ là:
    $$2 \le n + 1 \le 2027$$
    
    Tổng số các số nguyên liên tiếp trong đoạn $[2; 2027]$ là:
    $$2027 - 2 + 1 = 2026 \text{ (số)}$$
    
    Trong đoạn này, số các số là bội của $3$ (tức là $n + 1 \vdots 3$) bắt đầu từ $3$ đến $2025$ là một cấp số cộng công sai $3$:
    $$\text{Số các bội của } 3 = \dfrac{2025 - 3}{3} + 1 = 675 + 1 = 676 \text{ (số)}$$
    
    Số các giá trị của $n$ sao cho $(n + 1)$ không chia hết cho $3$ là:
    $$2026 - 676 = 1350 \text{ (giá trị)}$$
    
    **Kết luận:** Có tổng cộng **$1350$** giá trị của $n$ thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 85: PHƯƠNG TRÌNH BẬC HAI VÀ TỔNG LẬP PHƯƠNG NGHIỆM
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 85 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho phương trình bậc hai $x^2 - mx + m^2 - 3 = 0$ (với $m$ là tham số thực). Có bao nhiêu giá trị nguyên của $m$ để phương trình có hai nghiệm phân biệt $x_1, x_2$ sao cho tổng lập phương các nghiệm $S = x_1^3 + x_2^3$ là một số nguyên chia hết cho $7$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_85 = st.text_input("Nhập số lượng giá trị nguyên của m:", key="q85_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q85_check"):
    normalized_user_answer_85 = user_answer_85.strip().replace(',', '.')
    
    if normalized_user_answer_85 == "3":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_85 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy đặt điều kiện delta dương để có hai nghiệm phân biệt, sau đó dùng định lý Vi-et biểu diễn $x_1^3 + x_2^3$ theo $m$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q85_solution_shown' not in st.session_state:
    st.session_state['q85_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q85_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q85_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q85_solution_shown'] = False 

if st.session_state.get('q85_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm điều kiện để phương trình có hai nghiệm phân biệt**
    
    Phương trình $x^2 - mx + m^2 - 3 = 0$ có hai nghiệm phân biệt $x_1, x_2$ khi và chỉ khi biệt thức $\Delta > 0$:
    $$\Delta = m^2 - 4(1)(m^2 - 3) = -3m^2 + 12 > 0$$
    $$-3m^2 > -12 \iff m^2 < 4 \iff -2 < m < 2$$
    
    Vì $m$ là số nguyên, ta suy ra các giá trị có thể của $m$ là:
    $$m \in \{-1, 0, 1\}$$
    
    **Bước 2: Biểu diễn tổng lập phương nghiệm theo tham số $m$**
    
    Theo định lý Vi-et, ta có:
    $$\begin{cases} x_1 + x_2 = m \\ x_1 x_2 = m^2 - 3 \end{cases}$$
    
    Biến đổi biểu thức tổng lập phương các nghiệm:
    $$S = x_1^3 + x_2^3 = (x_1 + x_2)^3 - 3x_1 x_2 (x_1 + x_2)$$
    $$S = m^3 - 3(m^2 - 3)m = m^3 - 3m^3 + 9m = 9m - 2m^3$$
    
    **Bước 3: Kiểm tra điều kiện chia hết cho $7$**
    
    Ta xét giá trị của $S$ với từng giá trị nguyên của $m$ thuộc tập $\{-1, 0, 1\}$:
    *   Với $m = 0$: $S = 9(0) - 2(0)^3 = 0$. Vì $0$ chia hết cho $7$ nên $m = 0$ thỏa mãn.
    *   Với $m = 1$: $S = 9(1) - 2(1)^3 = 7$. Vì $7$ chia hết cho $7$ nên $m = 1$ thỏa mãn.
    *   Với $m = -1$: $S = 9(-1) - 2(-1)^3 = -9 + 2 = -7$. Vì $-7$ chia hết cho $7$ nên $m = -1$ thỏa mãn.
    
    Cả ba giá trị $m \in \{-1, 0, 1\}$ đều thỏa mãn tất cả các điều kiện của bài toán.
    
    **Kết luận:** Có tổng cộng **$3$** giá trị nguyên của $m$ thỏa mãn yêu cầu bài toán.
    """)
    
st.markdown("---")


# =====================================================================
# CÂU HỎI SỐ 86 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 86. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho các số nguyên dương $x, y, z$ thỏa mãn phương trình nghiệm nguyên:
$$3^x + 2^{2y} = z^2$$
Tính giá trị của biểu thức $T = x + y + z$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 86) ---
user_ans_86 = st.text_input("Nhập giá trị của biểu thức T:", key="q86_ans")

if st.button("Kiểm tra đáp án Câu 86", key="q86_check"):
    norm_ans_86 = user_ans_86.strip()
    
    # Đáp án chính xác là 9
    if norm_ans_86 == "9":
        st.success("🎉 Xuất sắc! Bạn đã biến đổi và khai thác tính chất lũy thừa của số nguyên tố một cách cực kỳ tinh tế. Lời giải Câu 86 đã được mở khóa.")
    elif user_ans_86 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 86.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Chuyển $2^{2y}$ sang vế phải để tạo hằng đẳng thức hiệu hai bình phương $z^2 - (2^y)^2 = 3^x$, sau đó phân tích thành nhân tử.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 86 ---
st.markdown("---")

if 'q86_solution_shown' not in st.session_state:
    st.session_state['q86_solution_shown'] = False

col1_86, col2_86 = st.columns([1, 4])
with col1_86:
    if st.button("Xem lời giải Câu 86", key="q86_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q86_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q86_solution_shown'] = False 

if st.session_state.get('q86_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 86 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Biến đổi phương trình về dạng tích**
    
    Phương trình đã cho được viết lại thành:
    $$3^x = z^2 - (2^y)^2$$
    
    Áp dụng hằng đẳng thức hiệu hai bình phương ở vế phải:
    $$3^x = (z - 2^y)(z + 2^y)$$
    
    **Bước 2: Phân tích ước số của $3^x$**
    
    Vì $3^x$ là một lũy thừa của số nguyên tố $3$ và $z - 2^y < z + 2^y$, cả hai thừa số $(z - 2^y)$ và $(z + 2^y)$ buộc phải là các lũy thừa của $3$. 
    Đặt:
    $$\begin{cases} z - 2^y = 3^a \\ z + 2^y = 3^b \end{cases}$$
    với $a < b$ và $a + b = x$ ($a, b$ là các số nguyên không âm).
    
    **Bước 3: Giải hệ phương trình mũ**
    
    Lấy phương trình dưới trừ phương trình trên:
    $$(z + 2^y) - (z - 2^y) = 3^b - 3^a \implies 2 \cdot 2^y = 2^{y+1} = 3^a(3^{b-a} - 1)$$
    
    Vì vế trái $2^{y+1}$ chỉ có ước nguyên tố là $2$, nên thừa số $3^a$ ở vế phải bắt buộc phải bằng $1$ (nếu $3^a > 1$ thì vế phải sẽ chia hết cho $3$, vô lý). 
    Do đó:
    $$3^a = 1 \implies a = 0$$
    
    Khi đó phương trình trở thành:
    $$2^{y+1} = 3^b - 1$$
    
    **Bước 4: Tìm nghiệm cụ thể**
    
    Thử các giá trị nguyên dương của $b$:
    *   Nếu $b = 1$: $2^{y+1} = 3^1 - 1 = 2 \implies y + 1 = 1 \implies y = 0$ (loại vì $y$ là số nguyên dương).
    *   Nếu $b = 2$: $2^{y+1} = 3^2 - 1 = 8 = 2^3 \implies y + 1 = 3 \implies y = 2$.
    *   Nếu $b \ge 3$: $3^b - 1$ chia hết cho $3^{2} - 1 = 8$ (hoặc dùng tính chất đồng dư modulo $8$), khi xét các giá trị lớn hơn sẽ thấy không thỏa mãn.
    
    Với $b = 2$ và $y = 2$:
    *   Ta có $a = 0 \implies x = a + b = 0 + 2 = 2$.
    *   Tính $z$ từ phương trình $z + 2^y = 3^b \implies z + 2^2 = 3^2 \implies z + 4 = 9 \implies z = 5$.
    
    Kiểm tra lại các nghiệm: $x = 2, y = 2, z = 5$ đều là các số nguyên dương và thỏa mãn $3^2 + 2^{2(2)} = 9 + 16 = 25 = 5^2$ (thỏa mãn).
    
    **Bước 5: Tính giá trị biểu thức $T$ và kết luận**
    
    Giá trị của biểu thức $T = x + y + z = 2 + 2 + 5 = 9$.
    
    ---
    **👉 Đáp số Câu 86:** `9`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 87 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 87. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho $S$ là tổng tất cả các số nguyên $n$ thuộc đoạn $[-2026, 2026]$ sao cho giá trị của phân số $\dfrac{n^3 - 2n^2 + 3}{n - 1}$ là một số nguyên. Tính giá trị của tổng $S$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 87) ---
user_ans_87 = st.text_input("Nhập giá trị của tổng S:", key="q87_ans")

if st.button("Kiểm tra đáp án Câu 87", key="q87_check"):
    norm_ans_87 = user_ans_87.strip()
    
    # Đáp án chính xác là 4
    if norm_ans_87 == "4":
        st.success("🎉 Xuất sắc! Bạn đã thực hiện phép chia đa thức và tìm ước số nguyên một cách hoàn hảo. Lời giải Câu 87 đã được mở khóa.")
    elif user_ans_87 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 87.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Thực hiện phép chia đa thức tử cho mẫu để tách phần nguyên và phần phân thức $\dfrac{2}{n-1}$, sau đó tìm các ước của $2$.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 87 ---
st.markdown("---")

if 'q87_solution_shown' not in st.session_state:
    st.session_state['q87_solution_shown'] = False

col1_87, col2_87 = st.columns([1, 4])
with col1_87:
    if st.button("Xem lời giải Câu 87", key="q87_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q87_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q87_solution_shown'] = False 

if st.session_state.get('q87_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 87 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Rút gọn biểu thức phân số bằng phép chia đa thức**
    
    Xét phân số cần tìm giá trị nguyên:
    $$P(n) = \dfrac{n^3 - 2n^2 + 3}{n - 1}$$
    
    Thực hiện phép chia đa thức $n^3 - 2n^2 + 3$ cho $n - 1$:
    *   $n^3 - 2n^2 + 3 = n^2(n - 1) - n(n - 1) - (n - 1) + 2$
    *   Hay: $n^3 - 2n^2 + 3 = (n - 1)(n^2 - n - 1) + 2$
    
    Do đó, phân số được viết lại thành:
    $$P(n) = n^2 - n - 1 + \dfrac{2}{n - 1}$$
    
    **Bước 2: Lập điều kiện để phân số nhận giá trị nguyên**
    
    Vì $n$ là số nguyên, biểu thức $n^2 - n - 1$ luôn là một số nguyên. Do đó, để $P(n)$ là một số nguyên thì phần dư $\dfrac{2}{n - 1}$ bắt buộc phải là một số nguyên.
    
    Điều này xảy ra khi và chỉ khi $(n - 1)$ là ước nguyên của $2$.
    
    **Bước 3: Tìm các giá trị của $n$**
    
    Các ước nguyên của $2$ gồm: $\pm 1, \pm 2$. Ta giải các trường hợp sau:
    1.  $n - 1 = 1 \implies n = 2$.
    2.  $n - 1 = -1 \implies n = 0$.
    3.  $n - 1 = 2 \implies n = 3$.
    4.  $n - 1 = -2 \implies n = -1$.
    
    **Bước 4: Kiểm tra điều kiện thuộc đoạn $[-2026, 2026]$ và tính tổng $S$**
    
    Tất cả các giá trị tìm được là $n \in \{2, 0, 3, -1\}$, đều thỏa mãn nằm trong đoạn $[-2026, 2026]$.
    
    Tính tổng $S$ của các giá trị này:
    $$S = 2 + 0 + 3 + (-1) = 4$$
    
    ---
    **👉 Đáp số Câu 87:** `4`
    """)

st.markdown("---")



# ==========================================
# CÂU 88: ĐỒNG DƯ THỨC VÀ ĐỊNH LÝ NHỎ FERMAT
# ==========================================
st.markdown(
    '<b style="color: blue;">Câu 88 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $A = 2025^{2026^{2027}}$. Tìm số dư khi chia $A$ cho số nguyên tố $17$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_88 = st.text_input("Nhập số dư của phép chia:", key="q88_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q88_check"):
    normalized_user_answer_88 = user_answer_88.strip().replace(',', '.')
    
    if normalized_user_answer_88 == "1":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_88 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý nhỏ Fermat kết hợp với tính chu kỳ số mũ theo mô-đun nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q88_solution_shown' not in st.session_state:
    st.session_state['q88_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q88_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q88_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q88_solution_shown'] = False 

if st.session_state.get('q88_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Xét cơ số theo mô-đun $17$**
    
    Ta có $2025 = 17 \times 119 + 2$, suy ra:
    $$2025 \equiv 2 \pmod{17}$$
    
    Do đó, biểu thức trở thành:
    $$A \equiv 2^{2026^{2027}} \pmod{17}$$
    
    **Bước 2: Xác định chu kỳ số mũ theo Định lý nhỏ Fermat**
    
    Vì $17$ là số nguyên tố và $\gcd(2, 17) = 1$, theo Định lý nhỏ Fermat, ta có:
    $$2^{16} \equiv 1 \pmod{17}$$
    
    Do đó, ta cần tìm số dư của số mũ $E = 2026^{2027}$ khi chia cho chu kỳ $16$.
    
    **Bước 3: Xét số mũ $E = 2026^{2027}$ theo mô-đun $16$**
    
    Ta có $2026 = 16 \times 126 + 10 \equiv 10 \pmod{16}$. Suy ra:
    $$E \equiv 10^{2027} \pmod{16}$$
    
    Vì các lũy thừa của $10$ với số mũ từ $4$ trở lên đều chia hết cho $16$:
    *   $10^1 \equiv 10 \pmod{16}$
    *   $10^2 \equiv 4 \pmod{16}$
    *   $10^3 \equiv 8 \pmod{16}$
    *   $10^4 \equiv 0 \pmod{16}$ và với mọi $k \ge 4$, $10^k \equiv 0 \pmod{16}$.
    
    Vì $2027 \ge 4$, nên $10^{2027} \equiv 0 \pmod{16}$. Điều này có nghĩa là $2026^{2027}$ là một số chia hết cho $16$, tức là $2026^{2027} = 16m$ với $m$ là số nguyên dương.
    
    **Bước 4: Tính giá trị của $A$ theo mô-đun $17$**
    
    Thay số mũ vừa tìm được vào biểu thức:
    $$A \equiv 2^{16m} = (2^{16})^m \equiv 1^m = 1 \pmod{17}$$
    
    **Kết luận:** Số dư khi chia $A$ cho $17$ là **$1$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 89: CHIA ĐA THỨC VÀ ĐỒNG DƯ THỨC ĐA THỨC
# ==========================================
st.markdown(
    '<b style="color: blue;">Câu 89 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho đa thức $P(x) = x^{2026} + x^{2025} + 1$. Khi chia đa thức $P(x)$ cho đa thức $Q(x) = x^2 + x + 1$, ta được số dư là đa thức bậc nhất $R(x) = ax + b$. Tính giá trị của biểu thức $T = a^2 + b^2$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_89 = st.text_input("Nhập giá trị của biểu thức T:", key="q89_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q89_check"):
    normalized_user_answer_89 = user_answer_89.strip().replace(',', '.')
    
    if normalized_user_answer_89 == "5":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_89 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy sử dụng hằng đẳng thức $x^3 - 1 = (x-1)(x^2 + x + 1)$ để thu gọn số mũ của đa thức nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q89_solution_shown' not in st.session_state:
    st.session_state['q89_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q89_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q89_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q89_solution_shown'] = False 

if st.session_state.get('q89_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập mối liên hệ đa thức**
    
    Ta có hằng đẳng thức đáng chú ý:
    $$x^3 - 1 = (x - 1)(x^2 + x + 1)$$
    
    Do đó, trong vành đa thức, khi xét phép chia cho $Q(x) = x^2 + x + 1$, ta có thể thay thế tương đương từ hệ thức:
    $$x^3 \equiv 1 \pmod{x^2 + x + 1}$$
    
    **Bước 2: Thu gọn số mũ của các hạng tử trong $P(x)$**
    
    *   Đối với số hạng $x^{2026}$:
        Thực hiện phép chia số mũ cho $3$: $2026 = 3 \times 675 + 1$.
        $$x^{2026} = (x^3)^{675} \cdot x \equiv 1^{675} \cdot x = x \pmod{x^2 + x + 1}$$
        
    *   Đối với số hạng $x^{2025}$:
        Thực hiện phép chia số mũ cho $3$: $2025 = 3 \times 675$.
        $$x^{2025} = (x^3)^{675} \equiv 1^{675} = 1 \pmod{x^2 + x + 1}$$
        
    **Bước 3: Xác định đa thức số dư $R(x)$**
    
    Thay các kết quả thu gọn vào đa thức $P(x)$:
    $$P(x) = x^{2026} + x^{2025} + 1 \equiv x + 1 + 1 = x + 2 \pmod{x^2 + x + 1}$$
    
    Vì đa thức dư có dạng $R(x) = ax + b$, đồng nhất hệ số ta thu được:
    $$a = 1, \quad b = 2$$
    
    **Bước 4: Tính giá trị biểu thức $T$**
    
    Thay giá trị $a$ và $b$ vào biểu thức $T$:
    $$T = a^2 + b^2 = 1^2 + 2^2 = 5$$
    
    **Kết luận:** Giá trị của biểu thức $T$ là **$5$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 90: TỔNG PHẦN NGUYÊN VÀ HÀM ƯỚC SỐ
# ==========================================
st.markdown(
    '<b style="color: blue;">Câu 90 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tính giá trị của biểu thức $S = \sum_{k=1}^{2026} \left\lfloor \dfrac{2026}{k} \right\rfloor$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_90 = st.text_input("Nhập giá trị của biểu thức S:", key="q90_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q90_check"):
    normalized_user_answer_90 = user_answer_90.strip().replace(',', '.')
    
    if normalized_user_answer_90 == "16157":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_90 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy đổi thứ tự tổng để đưa bài toán về tổng số ước số của các số nguyên từ $1$ đến $2026$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q90_solution_shown' not in st.session_state:
    st.session_state['q90_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q90_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q90_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q90_solution_shown'] = False 

if st.session_state.get('q90_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích bản chất của tổng phần nguyên**
    
    Ký hiệu $\left\lfloor \dfrac{2026}{k} \right\rfloor$ biểu diễn số lượng các bội số của $k$ nhỏ hơn hoặc bằng $2026$.
    
    **Bước 2: Đổi thứ tự tổng (Phương pháp đếm theo ước số)**
    
    Xét mỗi số nguyên dương $m$ trong đoạn từ $1$ đến $2026$. Số $m$ này sẽ xuất hiện bao nhiêu lần trong tổng $S$? 
    Số $m$ chỉ xuất hiện ở những số hạng mà $m$ là bội của $k$, điều này tương đương với việc $k$ là một ước số của $m$. Do đó, số lần xuất hiện của $m$ trong tổng đúng bằng số ước số của $m$, ký hiệu là $d(m)$.
    
    Vì vậy, ta có thể đổi thứ tự tổng:
    $$S = \sum_{m=1}^{2026} d(m) = \sum_{k=1}^{2026} \left\lfloor \dfrac{2026}{k} \right\rfloor$$
    
    **Bước 3: Áp dụng công thức tính nhanh tổng ước số**
    
    Với $n = 2026$, ta có $\sqrt{2026} \approx 45{,}01$, suy ra phần nguyên lớn nhất là $m = \lfloor \sqrt{2026} \rfloor = 45$.
    
    Sử dụng phương pháp phân hoạch (kỹ thuật nhóm đối xứng Dirichlet):
    $$\sum_{k=1}^{n} \left\lfloor \dfrac{n}{k} \right\rfloor = 2 \sum_{k=1}^{m} \left\lfloor \dfrac{n}{k} \right\rfloor - m^2$$
    
    **Bước 4: Tính toán giá trị cụ thể**
    
    *   Tính tổng các thương số phần nguyên từ $k = 1$ đến $m = 45$:
        $$\sum_{k=1}^{45} \left\lfloor \dfrac{2026}{k} \right\rfloor = 9091$$
    *   Thay vào công thức trên:
        $$S = 2 \times 9091 - 45^2 = 18182 - 2025 = 16157$$
    
    **Kết luận:** Giá trị của biểu thức $S$ là **$16157$**.
    """)
    
st.markdown("---")



# =====================================================================
# CÂU HỎI SỐ 91 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 91. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho các số nguyên dương $x, y, z$ thỏa mãn phương trình:
$$x! + y! = 2^z$$
với điều kiện $x \le y$. Gọi $S$ là tổng tất cả các giá trị của biểu thức $T = x + y + z$ ứng với mọi bộ nghiệm nguyên dương $(x, y, z)$ thỏa mãn. Tính giá trị của tổng $S$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 91) ---
user_ans_91 = st.text_input("Nhập giá trị của tổng S:", key="q91_ans")

if st.button("Kiểm tra đáp án Câu 91", key="q91_check"):
    norm_ans_91 = user_ans_91.strip()
    
    # Đáp án chính xác là 17
    if norm_ans_91 == "17":
        st.success("🎉 Xuất sắc! Bạn đã khai thác triệt để tính chất chia hết modulo 4 đối với giai thừa để tìm trọn vẹn các nghiệm. Lời giải Câu 91 đã được mở khóa.")
    elif user_ans_91 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 91.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Hãy xét các trường hợp của $x$ và $y$ kết hợp với tính chất chia hết cho $4$ của các giai thừa từ $4!$ trở lên.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 91 ---
st.markdown("---")

if 'q91_solution_shown' not in st.session_state:
    st.session_state['q91_solution_shown'] = False

col1_91, col2_91 = st.columns([1, 4])
with col1_91:
    if st.button("Xem lời giải Câu 91", key="q91_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q91_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q91_solution_shown'] = False 

if st.session_state.get('q91_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 91 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Phân tích trường hợp khi $y \ge 4$**
    
    Với mọi số nguyên dương $y \ge 4$, giá trị của $y!$ luôn chia hết cho $4$ (vì chứa thừa số $2 \times 4 = 8$ hoặc $3 \times 4$, v.v.).
    *   Nếu $x \ge 4$ và $y \ge 4$, thì cả $x!$ và $y!$ đều chia hết cho $4$, dẫn đến tổng $x! + y! \equiv 0 \pmod 4$.
        Trong khi đó, vế phải $2^z$ chia hết cho $4$ khi và chỉ khi $z \ge 2$. Nếu $z = 1$, $2^1 = 2 \not\equiv 0 \pmod 4$, nhưng nếu $z \ge 2$ thì $x! + y!$ rất lớn so với $2^z$ hoặc không thỏa mãn (thử trực tiếp thấy không có nghiệm).
    *   Do đó, để phương trình có nghiệm, các biến $x, y$ phải nhỏ hơn $4$.
    
    **Bước 2: Khảo sát các giá trị nhỏ của $x$ và $y$ (với $1 \le x \le y < 4$ và $x \le y$)**
    
    Ta xét các trường hợp cụ thể:
    1.  **Nếu $x = 1$:** Phương trình trở thành $1! + y! = 2^z \implies 1 + y! = 2^z$.
        *   Nếu $y = 1$: $1 + 1 = 2 = 2^1 \implies z = 1$. Ta được bộ nghiệm **$(1, 1, 1)$**. Giá trị $T = 1 + 1 + 1 = 3$.
        *   Nếu $y = 2$: $1 + 2! = 3 \neq 2^z$ (loại).
        *   Nếu $y = 3$: $1 + 3! = 7 \neq 2^z$ (loại).
        
    2.  **Nếu $x = 2$:** Phương trình trở thành $2! + y! = 2^z \implies 2 + y! = 2^z$.
        *   Nếu $y = 2$: $2 + 2! = 4 = 2^2 \implies z = 2$. Ta được bộ nghiệm **$(2, 2, 2)$**. Giá trị $T = 2 + 2 + 2 = 6$.
        *   Nếu $y = 3$: $2 + 3! = 8 = 2^3 \implies z = 3$. Ta được bộ nghiệm **$(2, 3, 3)$**. Giá trị $T = 2 + 3 + 3 = 8$.
        
    3.  **Nếu $x = 3$:** Phương trình trở thành $3! + y! = 2^z \implies 6 + y! = 2^z$.
        *   Nếu $y = 3$: $6 + 6 = 12 \neq 2^z$ (loại).
        
    **Bước 3: Tổng hợp các bộ nghiệm và tính tổng $S$**
    
    Tất cả các bộ nghiệm nguyên dương $(x, y, z)$ thỏa mãn điều kiện đề bài gồm:
    *   Bộ 1: $(1, 1, 1) \implies T_1 = 3$
    *   Bộ 2: $(2, 2, 2) \implies T_2 = 6$
    *   Bộ 3: $(2, 3, 3) \implies T_3 = 8$
    
    Tổng tất cả các giá trị của $T$ là:
    $$S = 3 + 6 + 8 = 17$$
    
    ---
    **👉 Đáp số Câu 91:** `17`
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================================
# CÂU HỎI SỐ 92 - [Trả lời ngắn _ TSA]
# =====================================================================

st.markdown(
    '<b style="color: blue;">Câu 92. [Trả lời ngắn _ TSA]</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số lượng nghiệm nguyên dương $(x, y)$ của phương trình:
$$x^3 - y^3 = xy + 61$$
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA (CÂU 92) ---
user_ans_92 = st.text_input("Nhập số lượng nghiệm nguyên dương:", key="q92_ans")

if st.button("Kiểm tra đáp án Câu 92", key="q92_check"):
    norm_ans_92 = user_ans_92.strip()
    
    # Đáp án chính xác là 1
    if norm_ans_92 == "1":
        st.success("🎉 Xuất sắc! Bạn đã biến đổi phương trình bằng hiệu hai lập phương và sử dụng biện luận biệt thức Delta cực kỳ sắc bén. Lời giải Câu 92 đã được mở khóa.")
    elif user_ans_92 == "":
        st.warning("⚠️ Bạn chưa nhập đáp án cho Câu 92.")
    else:
        st.error("❌ Chưa đúng. Gợi ý: Đặt $d = x - y$ (với $d \ge 1$), đưa phương trình về phương trình bậc hai theo ẩn $y$ và dùng điều kiện biệt thức $\Delta$ là số chính phương.")

# --- XEM LỜI GIẢI CHI TIẾT CÂU 92 ---
st.markdown("---")

if 'q92_solution_shown' not in st.session_state:
    st.session_state['q92_solution_shown'] = False

col1_92, col2_92 = st.columns([1, 4])
with col1_92:
    if st.button("Xem lời giải Câu 92", key="q92_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q92_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q92_solution_shown'] = False 

if st.session_state.get('q92_solution_shown') and st.session_state.get('logged_in'):
    st.info("### 💡 Hướng dẫn giải chi tiết Câu 92 (Tư duy TSA):")
    st.markdown(r"""
    **Bước 1: Đặt ẩn phụ chuyển đổi cấu trúc phương trình**
    
    Nhận xét rằng nếu $x \le y$, vế trái $x^3 - y^3 \le 0$ trong khi vế phải $xy + 61 > 0$, do đó bắt buộc phải có $x > y$. 
    Đặt $d = x - y$ với $d$ là số nguyên dương ($d \ge 1$). Khi đó $x = y + d$.
    
    Thay vào phương trình ban đầu:
    $$(y + d)^3 - y^3 = (y + d)y + 61$$
    $$3y^2d + 3yd^2 + d^3 = y^2 + dy + 61$$
    
    **Bước 2: Viết lại thành phương trình bậc hai ẩn $y$**
    
    Chuyển vế và nhóm các số hạng theo lũy thừa của $y$:
    $$y^2(3d - 1) + y(3d^2 - d) + (d^3 - 61) = 0$$
    
    Để phương trình tồn tại nghiệm nguyên $y$, biệt thức $\Delta$ của phương trình bậc hai này phải là một số chính phương không âm:
    $$\Delta = (3d^2 - d)^2 - 4(3d - 1)(d^3 - 61)$$
    
    Khai triển và rút gọn biểu thức $\Delta$:
    $$\Delta = 9d^4 - 6d^3 + d^2 - 4(3d^4 - d^3 - 183d + 61)$$
    $$\Delta = 9d^4 - 6d^3 + d^2 - 12d^4 + 4d^3 + 732d - 244$$
    $$\Delta = -3d^4 - 2d^3 + d^2 + 732d - 244$$
    
    **Bước 3: Khảo sát giá trị của $d$ để $\Delta$ là số chính phương**
    
    Vì $d$ là số nguyên dương, ta đánh giá giá trị của $\Delta$ với các số nguyên dương $d$:
    *   Với $d = 1$: 
        $$\Delta = -3(1) - 2(1) + 1 + 732(1) - 244 = 484 = 22^2 \quad (\text{thỏa mãn})$$
    *   Với $d = 2$: 
        $$\Delta = -3(16) - 2(8) + 4 + 732(2) - 244 = 1160 \quad (\text{không phải số chính phương})$$
    *   Với $d \ge 6$: Biểu thức chứa $-3d^4$ tăng trưởng âm rất nhanh, khiến $\Delta < 0$. Các giá trị $d = 3, 4, 5$ cũng được kiểm tra trực tiếp và đều không cho giá trị $\Delta$ là số chính phương.
    
    **Bước 4: Tìm nghiệm nguyên dương $(x, y)$ tương ứng**
    
    Với $d = 1$, ta thay vào phương trình bậc hai theo $y$:
    $$(3(1) - 1)y^2 + (3(1)^2 - 1)y + (1^3 - 61) = 0$$
    $$2y^2 + 2y - 60 = 0 \iff y^2 + y - 30 = 0$$
    
    Giải phương trình này ta được hai nghiệm: $y = 5$ hoặc $y = -6$. Vì $y$ là số nguyên dương, ta chọn **$y = 5$**.
    
    Từ đó tính được $x = y + d = 5 + 1 = 6$.
    
    Kiểm tra lại với bộ nghiệm $(6, 5)$:
    $$6^3 - 5^3 = 216 - 125 = 91$$
    $$6 \times 5 + 61 = 30 + 61 = 91 \quad (\text{thỏa mãn})$$
    
    **Bước 5: Kết luận**
    
    Phương trình chỉ có duy nhất $1$ nghiệm nguyên dương $(x, y) = (6, 5)$. Số lượng nghiệm bằng $1$.
    
    ---
    **👉 Đáp số Câu 92:** `1`
    """)

st.markdown("---")



# ==========================================
# CÂU 93: ĐỒNG DƯ THỨC VÀ ĐỊNH LÝ NHỎ FERMAT
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 93 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $A = 2^{2026} + 5^{2026}$. Tìm số dư khi chia số $A$ cho số nguyên tố $17$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_93 = st.text_input("Nhập số dư của phép chia:", key="q93_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q93_check"):
    normalized_user_answer_93 = user_answer_93.strip().replace(',', '.')
    
    if normalized_user_answer_93 == "13":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_93 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng Định lý nhỏ Fermat với chu kỳ mô-đun $16$ để thu gọn số mũ của từng hạng tử nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q93_solution_shown' not in st.session_state:
    st.session_state['q93_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q93_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q93_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q93_solution_shown'] = False 

if st.session_state.get('q93_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Áp dụng Định lý nhỏ Fermat**
    
    Vì $17$ là số nguyên tố và $\gcd(2, 17) = \gcd(5, 17) = 1$, theo Định lý nhỏ Fermat, ta có:
    $$2^{16} \equiv 1 \pmod{17}$$
    $$5^{16} \equiv 1 \pmod{17}$$
    
    **Bước 2: Thu gọn số mũ theo chu kỳ $16$**
    
    Thực hiện phép chia số mũ cho chu kỳ $16$:
    $$2026 = 16 \times 126 + 10$$
    
    Do đó, các số hạng được thu gọn như sau:
    * Đối với hạng tử $2^{2026}$:
      $$2^{2026} = (2^{16})^{126} \cdot 2^{10} \equiv 1^{126} \cdot 2^{10} = 1024 \pmod{17}$$
      Ta có $1024 = 17 \times 60 + 4$, suy ra $2^{2026} \equiv 4 \pmod{17}$.
      
    * Đối với hạng tử $5^{2026}$:
      $$5^{2026} = (5^{16})^{126} \cdot 5^{10} \equiv 1^{126} \cdot 5^{10} \pmod{17}$$
      Ta tính lần lượt:
      * $5^2 = 25 \equiv 8 \pmod{17}$
      * $5^4 \equiv 8^2 = 64 \equiv 13 \equiv -4 \pmod{17}$
      * $5^8 \equiv (-4)^2 = 16 \equiv -1 \pmod{17}$
      * $5^{10} = 5^8 \cdot 5^2 \equiv (-1) \cdot 8 = -8 \equiv 9 \pmod{17}$
      
    **Bước 3: Tổng hợp kết quả**
    
    Tổng số dư của biểu thức $A$ theo mô-đun $17$ là:
    $$A \equiv 4 + 9 = 13 \pmod{17}$$
    
    **Kết luận:** Số dư khi chia $A$ cho $17$ là **$13$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 94: CHIA ĐA THỨC VÀ ĐƠN VỊ ẢO ĐẠI SỐ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 94 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho đa thức $P(x) = x^{2026} - 2x^{1013} + 3$. Khi chia đa thức $P(x)$ cho đa thức $Q(x) = x^2 - x + 1$, ta được số dư là đa thức $R(x) = ax + b$. Tính giá trị của biểu thức $T = a^3 + b^3$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_94 = st.text_input("Nhập giá trị của biểu thức T:", key="q94_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q94_check"):
    normalized_user_answer_94 = user_answer_94.strip().replace(',', '.')
    
    if normalized_user_answer_94 == "2":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_94 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy sử dụng hằng đẳng thức $x^3 + 1 = (x + 1)(x^2 - x + 1)$ để hạ bậc số mũ của đa thức nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q94_solution_shown' not in st.session_state:
    st.session_state['q94_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q94_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q94_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q94_solution_shown'] = False 

if st.session_state.get('q94_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập mối quan hệ chia hết đa thức**
    
    Ta có hằng đẳng thức:
    $x^3 + 1 = (x + 1)(x^2 - x + 1)$
    
    Do đó, trong phép chia cho đa thức $x^2 - x + 1$, ta có quan hệ đồng dư đa thức:
    $x^3 \equiv -1 \pmod{x^2 - x + 1}$
    
    **Bước 2: Thu gọn các hạng tử của $P(x)$**
    
    * Xét số hạng $x^{2026}$:
      Thực hiện chia số mũ cho $3$: $2026 = 3 \times 675 + 1$.
      $$x^{2026} = (x^3)^{675} \cdot x \equiv (-1)^{675} \cdot x = -x \pmod{x^2 - x + 1}$$
      
    * Xét số hạng $x^{1013}$:
      Thực hiện chia số mũ cho $3$: $1013 = 3 \times 337 + 2$.
      $$x^{1013} = (x^3)^{337} \cdot x^2 \equiv (-1)^{337} \cdot x^2 = -x^2 \pmod{x^2 - x + 1}$$
      Mặt khác, từ $x^2 - x + 1 = 0$, ta suy ra $x^2 = x - 1$. Do đó:
      $$-x^2 = -(x - 1) = -x + 1$$
      
    **Bước 3: Xác định đa thức số dư $R(x)$**
    
    Thay thế các giá trị vừa thu gọn vào đa thức $P(x)$:
    $$P(x) \equiv -x - 2(-x + 1) + 3 \pmod{x^2 - x + 1}$$
    $$P(x) \equiv -x + 2x - 2 + 3 = x + 1 \pmod{x^2 - x + 1}$$
    
    Đồng nhất với dạng số dư tổng quát $R(x) = ax + b$, ta thu được:
    $$a = 1, \quad b = 1$$
    
    **Bước 4: Tính giá trị biểu thức $T$**
    
    $$T = a^3 + b^3 = 1^3 + 1^3 = 2$$
    
    **Kết luận:** Giá trị của biểu thức $T$ là **$2$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 95: PHƯƠNG TRÌNH NGHIỆM NGUYÊN VÀ ƯỚC SỐ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 95 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho phương trình $\dfrac{1}{x} + \dfrac{1}{y} = \dfrac{1}{2026^2}$ với $x, y$ là các số nguyên dương. Hỏi có bao nhiêu cặp số nguyên dương $(x, y)$ thỏa mãn phương trình trên?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_95 = st.text_input("Nhập số lượng cặp nghiệm $(x, y)$:", key="q95_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q95_check"):
    normalized_user_answer_95 = user_answer_95.strip().replace(',', '.')
    
    if normalized_user_answer_95 == "25":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_95 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy biến đổi phương trình về dạng nhân tử $(x - N)(y - N) = N^2$ với $N = 2026^2$ để đếm số ước số nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q95_solution_shown' not in st.session_state:
    st.session_state['q95_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q95_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q95_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q95_solution_shown'] = False 

if st.session_state.get('q95_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biến đổi phương trình về dạng nhân tử**
    
    Đặt $N = 2026^2$. Phương trình đã cho trở thành:
    $$\dfrac{1}{x} + \dfrac{1}{y} = \dfrac{1}{N}$$
    
    Quy đồng mẫu số và nhân chéo:
    $$N(x + y) = xy \iff xy - Nx - Ny = 0$$
    
    Cộng thêm $N^2$ vào hai vế để phân tích thành nhân tử:
    $$xy - Nx - Ny + N^2 = N^2$$
    $$x(y - N) - N(y - N) = N^2$$
    $$(x - N)(y - N) = N^2$$
    
    **Bước 2: Lập luận điều kiện nghiệm nguyên dương**
    
    Vì $x, y > 0$ và $\dfrac{1}{x} + \dfrac{1}{y} = \dfrac{1}{N}$, ta dễ dàng suy ra $x > N$ và $y > N$. Do đó các nhân tử $(x - N)$ và $(y - N)$ đều là các số nguyên dương.
    
    Số các cặp nghiệm nguyên dương $(x, y)$ thỏa mãn đúng bằng số các ước số nguyên dương của $N^2$.
    
    **Bước 3: Tính số lượng ước số của $N^2$**
    
    Ta có phân tích ra thừa số nguyên tố của $2026$:
    $$2026 = 2 \times 1013$$
    
    Suy ra:
    $$N = 2026^2 = 2^2 \times 1013^2$$
    $$N^2 = (2^2 \times 1013^2)^2 = 2^4 \times 1013^4$$
    
    Số các ước số nguyên dương của $N^2$ là:
    $$d(N^2) = (4 + 1)(4 + 1) = 5 \times 5 = 25$$
    
    **Kết luận:** Số lượng cặp số nguyên dương $(x, y)$ thỏa mãn là **$25$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 96: ĐỊNH LÝ LEGENDRE VÀ TỔ HỢP
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 96 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Tìm số mũ của thừa số nguyên tố $3$ trong phân tích tiêu chuẩn của số tổ hợp $S = C_{2026}^{1013}$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_96 = st.text_input("Nhập số mũ của thừa số 3:", key="q96_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q96_check"):
    normalized_user_answer_96 = user_answer_96.strip().replace(',', '.')
    
    if normalized_user_answer_96 == "4":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_96 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy áp dụng công thức Legendre để tính số mũ của $3$ trong phân tích giai thừa $v_3(n!) = \sum \left\lfloor \dfrac{n}{3^k} \right\rfloor$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q96_solution_shown' not in st.session_state:
    st.session_state['q96_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q96_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q96_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q96_solution_shown'] = False 

if st.session_state.get('q96_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Biểu diễn số tổ hợp qua giai thừa**
    
    Ta có công thức số tổ hợp:
    $$S = C_{2026}^{1013} = \dfrac{2026!}{1013! \cdot 1013!}$$
    
    Số mũ của số nguyên tố $3$ trong phân tích tiêu chuẩn của $S$ được tính bởi:
    $$v_3(S) = v_3(2026!) - 2v_3(1013!)$$
    
    **Bước 2: Áp dụng Định lý Legendre để tính số mũ**
    
    Công thức Legendre cho số mũ của nguyên tố $p$ trong $n!$ là:
    $$v_p(n!) = \sum_{k=1}^{\infty} \left\lfloor \dfrac{n}{p^k} \right\rfloor$$
    
    * Tính $v_3(2026!)$ với $n = 2026$:
      * $\left\lfloor \dfrac{2026}{3} \right\rfloor = 675$
      * $\left\lfloor \dfrac{2026}{9} \right\rfloor = 225$
      * $\left\lfloor \dfrac{2026}{27} \right\rfloor = 75$
      * $\left\lfloor \dfrac{2026}{81} \right\rfloor = 25$
      * $\left\lfloor \dfrac{2026}{243} \right\rfloor = 8$
      * $\left\lfloor \dfrac{2026}{729} \right\rfloor = 2$
      * Các lũy thừa cao hơn cho thương số bằng $0$.
      
      Cộng lại: $v_3(2026!) = 675 + 225 + 75 + 25 + 8 + 2 = 1010$.
      
    * Tính $v_3(1013!)$ với $n = 1013$:
      * $\left\lfloor \dfrac{1013}{3} \right\rfloor = 337$
      * $\left\lfloor \dfrac{1013}{9} \right\rfloor = 112$
      * $\left\lfloor \dfrac{1013}{27} \right\rfloor = 37$
      * $\left\lfloor \dfrac{1013}{81} \right\rfloor = 12$
      * $\left\lfloor \dfrac{1013}{243} \right\rfloor = 4$
      * $\left\lfloor \dfrac{1013}{729} \right\rfloor = 1$
      
      Cộng lại: $v_3(1013!) = 337 + 112 + 37 + 12 + 4 + 1 = 503$.
      
    **Bước 3: Tính số mũ của $3$ trong $S$**
    
    $$v_3(S) = 1010 - 2 \times 503 = 1010 - 1006 = 4$$
    
    **Kết luận:** Số mũ của thừa số nguyên tố $3$ trong phân tích tiêu chuẩn của $C_{2026}^{1013}$ là **$4$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 97: DÃY SỐ VÀ ĐỒNG DƯ THỨC
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 97 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho dãy số $(u_n)$ được xác định bởi $u_1 = 3$, $u_2 = 11$ và hệ thức truy hồi $u_{n+2} = 5u_{n+1} - 6u_n$ với mọi $n \ge 1$. Tìm số dư khi chia số hạng $u_{2026}$ cho số nguyên tố $13$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_97 = st.text_input("Nhập số dư của phép chia:", key="q97_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q97_check"):
    normalized_user_answer_97 = user_answer_97.strip().replace(',', '.')
    
    if normalized_user_answer_97 == "8":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_97 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy giải phương trình đặc trưng tìm công thức tổng quát của dãy số rồi dùng Định lý nhỏ Fermat nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q97_solution_shown' not in st.session_state:
    st.session_state['q97_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q97_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q97_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q97_solution_shown'] = False 

if st.session_state.get('q97_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm công thức tổng quát của dãy số**
    
    Phương trình đặc trưng của hệ thức sai phân tuyến tính cấp hai là:
    $$r^2 - 5r + 6 = 0 \iff (r - 2)(r - 3) = 0 \iff \begin{bmatrix} r = 2 \\ r = 3 \end{bmatrix}$$
    
    Do đó, công thức tổng quát của dãy số có dạng:
    $$u_n = A \cdot 2^n + B \cdot 3^n$$
    
    Sử dụng điều kiện đầu để tìm các hằng số $A$ và $B$:
    * Với $n = 1$: $2A + 3B = 3$
    * Với $n = 2$: $4A + 9B = 11$
    
    Giải hệ phương trình này, ta thu được $A = -1$ và $B = \dfrac{5}{3}$. Vậy số hạng tổng quát là:
    $$u_n = -2^n + \dfrac{5}{3} \cdot 3^n = -2^n + 5 \cdot 3^{n-1}$$
    
    **Bước 2: Tính số hạng $u_{2026}$ theo mô-đun $13$**
    
    Ta cần tìm số dư của biểu thức:
    $$u_{2026} = -2^{2026} + 5 \cdot 3^{2025} \pmod{13}$$
    
    * Xét phần $-2^{2026} \pmod{13}$:
      Theo Định lý nhỏ Fermat, $2^{12} \equiv 1 \pmod{13}$.
      Thực hiện chia số mũ cho chu kỳ $12$: $2026 = 12 \times 168 + 10$.
      $$2^{2026} = (2^{12})^{168} \cdot 2^{10} \equiv 1^{168} \cdot 1024 \pmod{13}$$
      Vì $1024 = 13 \times 78 + 10 \equiv 10 \pmod{13}$, nên $-2^{2026} \equiv -10 \equiv 3 \pmod{13}$.
      
    * Xét phần $5 \cdot 3^{2025} \pmod{13}$:
      Theo Định lý nhỏ Fermat, $3^{12} \equiv 1 \pmod{13}$, hoặc đơn giản hơn $3^3 = 27 \equiv 1 \pmod{13}$.
      Thực hiện chia số mũ cho $3$: $2025 = 3 \times 675$ (chia hết cho $3$).
      $$3^{2025} = (3^3)^{675} \equiv 1^{675} = 1 \pmod{13}$$
      Do đó: $5 \cdot 3^{2025} \equiv 5 \cdot 1 = 5 \pmod{13}$.
      
    **Bước 3: Tổng hợp kết quả**
    
    $$u_{2026} \equiv 3 + 5 = 8 \pmod{13}$$
    
    **Kết luận:** Số dư khi chia $u_{2026}$ cho $13$ là **$8$**.
    """)
    
st.markdown("---")



# ==========================================
# CÂU 98: HÀM SỐ PHẦN NGUYÊN VÀ ĐỒNG DƯ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 98 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho hàm số $f(x) = \lfloor x \rfloor + \lfloor 2x \rfloor + \lfloor 3x \rfloor$ với $x \ge 0$. Gọi $S$ là tập hợp tất cả các giá trị nguyên $m$ thuộc đoạn $[0; 2026]$ sao cho phương trình $f(x) = m$ có nghiệm thực. Hỏi tập hợp $S$ có bao nhiêu phần tử?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_98 = st.text_input("Nhập số lượng phần tử của tập S:", key="q98_ans")

# Khối chèn hình ảnh minh họa

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q98_check"):
    normalized_user_answer_98 = user_answer_98.strip().replace(',', '.')
    
    if normalized_user_answer_98 == "1352":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_98 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích các giá trị mà hàm số đạt được trên các đoạn $[n, n+1)$ để tìm ra các giá trị $m$ bị khuyết nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q98_solution_shown' not in st.session_state:
    st.session_state['q98_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q98_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q98_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q98_solution_shown'] = False 

if st.session_state.get('q98_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích hàm số trên đoạn $[n, n+1)$ với $n \in \mathbb{N}$**
    
    Với mỗi $x \in [n, n+1)$, ta đặt $x = n + \{x\}$ trong đó $\{x\} \in [0, 1)$. Khi đó:
    * $\lfloor x \rfloor = n$
    * $\lfloor 2x \rfloor = \lfloor 2n + 2\{x\} \rfloor = 2n + \lfloor 2\{x\} \rfloor$
    * $\lfloor 3x \rfloor = \lfloor 3n + 3\{x\} \rfloor = 3n + \lfloor 3\{x\} \rfloor$
    
    Do đó, hàm số trở thành:
    $$f(x) = 6n + \lfloor 2\{x\} \rfloor + \lfloor 3\{x\} \rfloor$$
    
    **Bước 2: Khảo sát các giá trị của $f(x)$ khi $\{x\}$ thay đổi trong $[0, 1)$**
    
    Khi $\{x\}$ chạy từ $0$ đến $1$, biểu thức $\lfloor 2\{x\} \rfloor + \lfloor 3\{x\} \rfloor$ nhận các giá trị:
    * Nếu $\{x\} \in \left[0, \dfrac{1}{3}\right)$: $\lfloor 2\{x\} \rfloor = 0, \lfloor 3\{x\} \rfloor = 0 \implies f(x) = 6n$
    * Nếu $\{x\} \in \left[\dfrac{1}{3}, \dfrac{1}{2}\right)$: $\lfloor 2\{x\} \rfloor = 0, \lfloor 3\{x\} \rfloor = 1 \implies f(x) = 6n + 1$
    * Nếu $\{x\} \in \left[\dfrac{1}{2}, \dfrac{2}{3}\right)$: $\lfloor 2\{x\} \rfloor = 1, \lfloor 3\{x\} \rfloor = 1 \implies f(x) = 6n + 2$
    * Nếu $\{x\} \in \left[\dfrac{2}{3}, 1\right)$: $\lfloor 2\{x\} \rfloor = 1, \lfloor 3\{x\} \rfloor = 2 \implies f(x) = 6n + 3$
    
    Như vậy, với mỗi số nguyên không âm $n$, phương trình $f(x) = m$ có nghiệm khi và chỉ khi $m$ có dạng $6n, 6n+1, 6n+2, 6n+3$. Các giá trị $6n+4$ và $6n+5$ không bao giờ là giá trị của hàm số $f(x)$.
    
    **Bước 3: Đếm số lượng giá trị hợp lệ trong đoạn $[0; 2026]$**
    
    Thực hiện phép chia $2026$ cho $6$:
    $$2026 = 6 \times 337 + 4$$
    
    * Có $337$ chu kỳ hoàn chỉnh từ $0$ đến $6 \times 337 - 1$. Mỗi chu kỳ gồm $6$ số nguyên liên tiếp, trong đó có đúng $4$ giá trị hợp lệ thuộc tập $S$. Số lượng giá trị hợp lệ là:
      $$337 \times 4 = 1348$$
    * Xét các số còn lại từ $2022$ đến $2026$ (gồm $5$ số: $2022, 2023, 2024, 2025, 2026$), ta có các giá trị hợp lệ tương ứng với $n = 337$ là $6(337) = 2022$, $2023$, $2024$, $2025$ (tổng cộng có thêm $4$ giá trị hợp lệ, còn $2026 = 6(337) + 4$ là không hợp lệ).
    
    **Bước 4: Tổng hợp kết quả**
    
    Tổng số phần tử của tập $S$ là:
    $$1348 + 4 = 1352$$
    
    **Kết luận:** Tập hợp $S$ có **$1352$** phần tử.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 99: PHƯƠNG TRÌNH NGHIỆM NGUYÊN HÀM MŨ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 99 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Phương trình $2^x + 3^y = z^2$ có bao nhiêu nghiệm nguyên dương $(x, y, z)$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_99 = st.text_input("Nhập số lượng nghiệm nguyên dương:", key="q99_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q99_check"):
    normalized_user_answer_99 = user_answer_99.strip().replace(',', '.')
    
    if normalized_user_answer_99 == "1":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_99 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy xét tính chẵn lẻ của $y$ và xét phương trình theo mô-đun hoặc phân tích nhân tử nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q99_solution_shown' not in st.session_state:
    st.session_state['q99_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q99_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q99_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q99_solution_shown'] = False 

if st.session_state.get('q99_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Xét tính chẵn lẻ của $y$**
    
    Xét phương trình $2^x + 3^y = z^2$ với $x, y, z \in \mathbb{N}^*$.
    * Nếu $y$ là số lẻ: Ta xét phương trình theo mô-đun $3$.
      Vì $2^x \equiv (-1)^x \pmod 3$ và $3^y \equiv 0 \pmod 3$, nên $z^2 \equiv (-1)^x \pmod 3$.
      Nếu $x$ lẻ, $z^2 \equiv -1 \equiv 2 \pmod 3$ (vô lý vì số chính phương chia cho $3$ chỉ có số dư là $0$ hoặc $1$).
      Nếu $x$ chẵn, đặt $x = 2k$, phương trình trở thành $2^{2k} + 3^y = z^2 \iff 3^y = (z - 2^k)(z + 2^k)$.
      Vì cả hai thừa số là lũy thừa của $3$, ta có $z - 2^k = 3^a$ và $z + 2^k = 3^b$ với $a < b$ và $a + b = y$.
      Trừ hai vế ta được $2 \cdot 2^k = 3^a(3^{b-a} - 1) \implies 2^{k+1} = 3^a(3^{b-a} - 1)$. Do $3^a$ lẻ nên $3^a = 1 \implies a = 0$.
      Khi đó $2^{k+1} = 3^b - 1$. Thử các giá trị nhỏ của $b$ ta thấy chỉ có $b = 2$ cho nghiệm $k = 2$ (tức $x = 4$, $y = 2$, $z = 5$).
    
    **Bước 2: Xét trường hợp $y$ chẵn**
    
    Đặt $y = 2k$ ($k \in \mathbb{N}^*$), phương trình trở thành:
    $$2^x = z^2 - (3^k)^2 = (z - 3^k)(z + 3^k)$$
    
    Vì tích bằng lũy thừa của $2$, cả hai thừa số đều là lũy thừa của $2$. Đặt:
    $$\begin{cases} z - 3^k = 2^a \\ z + 3^k = 2^b \end{cases} \quad \text{với } a < b \text{ và } a + b = x$$
    
    Trừ hai vế phương trình, ta thu được:
    $$2 \cdot 3^k = 2^b - 2^a = 2^a(2^{b-a} - 1)$$
    
    Vì $3^k$ là số lẻ, thừa số $2^a$ phải chứa toàn bộ lũy thừa $2$ ở vế trái, suy ra $2^a = 2 \implies a = 1$.
    Phương trình rút gọn thành:
    $$3^k = 2^{b-1} - 1 \iff 3^k + 1 = 2^{b-1}$$
    
    **Bước 3: Giải phương trình $3^k + 1 = 2^{b-1}$**
    
    * Nếu $k = 1$: $3^1 + 1 = 4 = 2^2 \implies b - 1 = 2 \implies b = 3$.
      Từ đó $a = 1, b = 3 \implies x = a + b = 4$.
      Và $y = 2k = 2$.
      Tính $z$: $z + 3^1 = 2^3 = 8 \implies z = 5$.
      Ta tìm được nghiệm nguyên dương duy nhất: $(x, y, z) = (4, 2, 5)$.
    * Nếu $k \ge 2$: Xét theo mô-đun $3$, ta có $0 + 1 \equiv 2^{b-1} \pmod 3 \implies (-1)^{b-1} \equiv 1 \pmod 3$, suy ra $b-1$ là số chẵn, đặt $b-1 = 2m$.
      Khi đó $3^k = (2^m - 1)(2^m + 1)$. Vì hai thừa số bên phải là hai lũy thừa của $2$ chênh lệch nhau $2$ đơn vị, mà chỉ có $3^1 - 3^0 = 2$ trong lũy thừa của $3$, ta suy ra $2^m - 1 = 1 \implies m = 1$, dẫn đến $k = 1$ (mâu thuẫn với giả thiết $k \ge 2$).
    
    **Bước 4: Kết luận**
    
    Phương trình chỉ có duy nhất một nghiệm nguyên dương $(4, 2, 5)$.
    
    **Kết luận:** Số lượng nghiệm nguyên dương của phương trình là **$1$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 100: CỰC TRỊ HÀM SỐ BẬC BA VÀ ĐẠI SỐ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 100 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho hàm số $y = x^3 - 3mx^2 + 3(m^2 - 1)x - m^3$. Gọi $x_1, x_2$ là hai điểm cực trị của hàm số. Tìm tổng bình phương tất cả các giá trị thực của tham số $m$ sao cho $x_1^2 + x_2^2 - x_1x_2 = 7$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_100 = st.text_input("Nhập tổng bình phương các giá trị của m:", key="q100_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q100_check"):
    normalized_user_answer_100 = user_answer_100.strip().replace(',', '.')
    
    if normalized_user_answer_100 == "8":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_100 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy tính đạo hàm, sử dụng hệ thức Vi-ét để biến đổi biểu thức $x_1^2 + x_2^2 - x_1x_2$ về dạng $(x_1+x_2)^2 - 3x_1x_2$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q100_solution_shown' not in st.session_state:
    st.session_state['q100_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q100_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q100_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q100_solution_shown'] = False 

if st.session_state.get('q100_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính đạo hàm và tìm điều kiện có cực trị**
    
    Ta có đạo hàm của hàm số:
    $$y' = 3x^2 - 6mx + 3(m^2 - 1)$$
    
    Hàm số có hai điểm cực trị $x_1, x_2$ khi và chỉ khi phương trình $y' = 0$ có hai nghiệm phân biệt:
    $$x^2 - 2mx + m^2 - 1 = 0$$
    Delta phẩy của phương trình là:
    $$\Delta' = m^2 - (m^2 - 1) = 1 > 0 \quad (\text{luôn đúng với mọi } m)$$
    
    **Bước 2: Áp dụng hệ thức Vi-ét**
    
    Theo định lý Vi-ét, hoành độ hai điểm cực trị thỏa mãn:
    $$\begin{cases} x_1 + x_2 = 2m \\ x_1x_2 = m^2 - 1 \end{cases}$$
    
    **Bước 3: Biến đổi và giải phương trình chứa tham số $m$**
    
    Biểu thức bài toán cho là:
    $$x_1^2 + x_2^2 - x_1x_2 = 7 \iff (x_1 + x_2)^2 - 3x_1x_2 = 7$$
    
    Thay hệ thức Vi-ét vào phương trình trên:
    $$(2m)^2 - 3(m^2 - 1) = 7$$
    $$4m^2 - 3m^2 + 3 = 7 \iff m^2 + 3 = 7 \iff m^2 = 4 \iff \begin{bmatrix} m = 2 \\ m = -2 \end{bmatrix}$$
    
    Các giá trị này đều thỏa mãn điều kiện phương trình có hai nghiệm phân biệt.
    
    **Bước 4: Tính tổng bình phương các giá trị của $m$**
    
    Tổng bình phương các giá trị của $m$ tìm được là:
    $$T = 2^2 + (-2)^2 = 4 + 4 = 8$$
    
    **Kết luận:** Tổng bình phương các giá trị của $m$ là **$8$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 101: CHIA ĐA THỨC VÀ ĐỊNH LÝ DƯ
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 101 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho đa thức $P(x)$ khi chia cho đa thức $x^2 - 3x + 2$ và khi chia cho đa thức $x^2 - 5x + 6$ đều có chung số dư là $3x - 1$. Tìm số dư $R(x) = ax + b$ khi chia đa thức $P(x)$ cho đa thức $x^2 - 4x + 3$. Tính giá trị của biểu thức $T = a^2 + b^2$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_101 = st.text_input("Nhập giá trị của biểu thức T:", key="q101_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q101_check"):
    normalized_user_answer_101 = user_answer_101.strip().replace(',', '.')
    
    if normalized_user_answer_101 == "10":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_101 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích các đa thức chia thành nhân tử và tính giá trị của $P(x)$ tại các nghiệm nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q101_solution_shown' not in st.session_state:
    st.session_state['q101_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q101_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q101_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q101_solution_shown'] = False 

if st.session_state.get('q101_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích các đa thức chia thành nhân tử**
    
    Ta có các phân tích thành nhân tử:
    * $x^2 - 3x + 2 = (x - 1)(x - 2)$
    * $x^2 - 5x + 6 = (x - 2)(x - 3)$
    * $x^2 - 4x + 3 = (x - 1)(x - 3)$
    
    **Bước 2: Thiết lập giá trị của đa thức $P(x)$ tại các điểm mấu chốt**
    
    Theo giả thiết, khi chia $P(x)$ cho $x^2 - 3x + 2$, số dư là $3x - 1$:
    $$P(x) = Q_1(x)(x - 1)(x - 2) + 3x - 1$$
    Thay các nghiệm $x = 1$ và $x = 2$, ta được:
    * $P(1) = 3(1) - 1 = 2$
    * $P(2) = 3(2) - 1 = 5$
    
    Tương tự, khi chia $P(x)$ cho $x^2 - 5x + 6$, số dư cũng là $3x - 1$:
    $$P(x) = Q_2(x)(x - 2)(x - 3) + 3x - 1$$
    Thay nghiệm $x = 3$, ta được:
    * $P(3) = 3(3) - 1 = 8$
    
    **Bước 3: Xác định số dư khi chia $P(x)$ cho $x^2 - 4x + 3$**
    
    Gọi số dư khi chia $P(x)$ cho $x^2 - 4x + 3 = (x - 1)(x - 3)$ là đa thức bậc nhất $R(x) = ax + b$:
    $$P(x) = Q_3(x)(x - 1)(x - 3) + ax + b$$
    
    Thay lần lượt các giá trị $x = 1$ và $x = 3$ vào biểu thức trên:
    * Với $x = 1$: $P(1) = a(1) + b = a + b = 2$
    * Với $x = 3$: $P(3) = a(3) + b = 3a + b = 8$
    
    Giải hệ phương trình bậc nhất hai ẩn:
    $$\begin{cases} a + b = 2 \\ 3a + b = 8 \end{cases} \iff \begin{cases} 2a = 6 \\ b = 2 - a \end{cases} \iff \begin{cases} a = 3 \\ b = -1 \end{cases}$$
    
    Vậy số dư là $R(x) = 3x - 1$.
    
    **Bước 4: Tính giá trị biểu thức $T$**
    
    $$T = a^2 + b^2 = 3^2 + (-1)^2 = 9 + 1 = 10$$
    
    **Kết luận:** Giá trị của biểu thức $T$ là **$10$**.
    """)
    
st.markdown("---")


# ==========================================
# CÂU 102: TỔ HỢP VÀ SỐ HỌC NÂNG CAO
# ==========================================

st.markdown(
    '<b style="color: blue;">Câu 102 (Trả lời ngắn _ TSA)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Cho số nguyên dương $n$ thỏa mãn phương trình $C_{2n}^{0} + C_{2n}^{2} + C_{2n}^{4} + \dots + C_{2n}^{2n} = 2048$. Tìm số dư khi chia số $A = 2^n + 5^n$ cho số nguyên tố $13$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer_102 = st.text_input("Nhập số dư của phép chia:", key="q102_ans")

# Khối chèn hình ảnh minh họa


# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q102_check"):
    normalized_user_answer_102 = user_answer_102.strip().replace(',', '.')
    
    if normalized_user_answer_102 == "11":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer_102 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy dùng khai triển nhị thức Newton để tìm $n$, sau đó tính số dư theo mô-đun $13$ nhé!")

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q102_solution_shown' not in st.session_state:
    st.session_state['q102_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q102_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q102_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q102_solution_shown'] = False 

if st.session_state.get('q102_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm số nguyên dương $n$ từ khai triển nhị thức Newton**
    
    Xét khai triển nhị thức Newton của $(1 + x)^{2n}$ và $(1 - x)^{2n}$:
    $$(1 + x)^{2n} = C_{2n}^{0} + C_{2n}^{1}x + C_{2n}^{2}x^2 + \dots + C_{2n}^{2n}x^{2n}$$
    $$(1 - x)^{2n} = C_{2n}^{0} - C_{2n}^{1}x + C_{2n}^{2}x^2 - \dots + C_{2n}^{2n}x^{2n}$$
    
    Cộng hai vế lại với nhau và chọn $x = 1$, ta được:
    $$(1 + 1)^{2n} + (1 - 1)^{2n} = 2(C_{2n}^{0} + C_{2n}^{2} + C_{2n}^{4} + \dots + C_{2n}^{2n})$$
    $$2^{2n} = 2(C_{2n}^{0} + C_{2n}^{2} + C_{2n}^{4} + \dots + C_{2n}^{2n})$$
    $$\implies C_{2n}^{0} + C_{2n}^{2} + C_{2n}^{4} + \dots + C_{2n}^{2n} = 2^{2n-1}$$
    
    Theo giả thiết, ta có phương trình:
    $$2^{2n-1} = 2048 = 2^{11} \iff 2n - 1 = 11 \iff 2n = 12 \iff n = 6$$
    
    **Bước 2: Tính số dư của biểu thức $A = 2^6 + 5^6$ theo mô-đun $13$**
    
    Thay $n = 6$ vào biểu thức $A$:
    $$A = 2^6 + 5^6 = 64 + 15625 = 15689$$
    
    Xét từng số hạng theo mô-đun $13$:
    * Đối với hạng tử $2^6$:
      $$2^6 = 64 = 13 \times 4 + 12 \equiv 12 \pmod{13} \quad (\text{hoặc } 64 \equiv -1 \pmod{13})$$
    * Đối với hạng tử $5^6$:
      $$5^2 = 25 \equiv -1 \pmod{13}$$
      $$5^6 = (5^2)^3 \equiv (-1)^3 = -1 \equiv 12 \pmod{13}$$
    
    **Bước 3: Tổng hợp kết quả phép chia**
    
    $$A \equiv 12 + 12 = 24 \equiv 11 \pmod{13}$$
    
    **Kết luận:** Số dư khi chia $A$ cho $13$ là **$11$**.
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 103. [Trắc nghiệm]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh / đề bài
st.markdown(r"""
Tìm số dư khi chia biểu thức $A = 3^{2026}$ cho $11$.
""")

# --- CÁC LỰA CHỌN TRẮC NGHIỆM ---
options = ["A. 1", "B. 3", "C. 5", "D. 9"]

# Tạo bảng chọn trắc nghiệm (index=None để ban đầu chưa chọn đáp án)
user_choice = st.radio(
    "Chọn đáp án đúng:", 
    options, 
    key="q103_mcq", 
    index=None 
)

# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q103_check_mcq"):
    if user_choice == "B. 3":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_choice is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy áp dụng định lý Fermat nhỏ hoặc tính chất đồng dư thức nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q103_solution_shown' not in st.session_state:
    st.session_state['q103_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q103_solution_mcq"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q103_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q103_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q103_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Phương pháp:** Sử dụng **Định lý Fermat nhỏ** hoặc tính chất đồng dư thức.
    
    Vì $11$ là số nguyên tố và $\gcd(3, 11) = 1$, theo định lý Fermat nhỏ ta có:
    $$3^{10} \equiv 1 \pmod{11}$$
    
    **Bước 1: Phân tích số mũ $2026$**
    
    Chia $2026$ cho $10$, ta được:
    $$2026 = 10 \cdot 202 + 6$$
    
    **Bước 2: Biến đổi biểu thức $A$**
    
    $$A = 3^{2026} = 3^{10 \cdot 202 + 6} = (3^{10})^{202} \cdot 3^6$$
    
    Do $3^{10} \equiv 1 \pmod{11}$, suy ra:
    $$A \equiv (1)^{202} \cdot 3^6 \equiv 3^6 \pmod{11}$$
    
    **Bước 3: Tính số dư của $3^6$ khi chia cho $11$**
    
    Ta có: $3^3 = 27 = 11 \cdot 2 + 5 \equiv 5 \pmod{11}$.
    
    Suy ra:
    $$3^6 = (3^3)^2 \equiv 5^2 \equiv 25 \pmod{11}$$
    
    Vì $25 = 11 \cdot 2 + 3 \equiv 3 \pmod{11}$, nên $3^6 \equiv 3 \pmod{11}$.
    
    **Kết luận:** Số dư khi chia $A = 3^{2026}$ cho $11$ là **$3$**. Do đó, chọn đáp án **B**.
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 104. [Trắc nghiệm Đúng / Sai]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi (Câu dẫn)
st.markdown(r"""
Cho số nguyên dương $N = p^3 \cdot q^2$, với $p$ và $q$ là hai số nguyên tố phân biệt. Các phát biểu sau đây là Đúng hay Sai?
""")

# --- DANH SÁCH CÁC PHÁT BIỂU VÀ ĐÁP ÁN ---
statements = {
    "a": {
        "text": "Số lượng ước số nguyên dương của $N$ là $12$.",
        "answer": "Đúng"
    },
    "b": {
        "text": "Số lượng ước số nguyên dương của $N^2$ là $144$.",
        "answer": "Sai"
    },
    "c": {
        "text": "Tồn tại cặp số nguyên tố $(p, q)$ để $N$ là một số chính phương.",
        "answer": "Sai"
    },
    "d": {
        "text": "Tổng tất cả các ước số nguyên dương của $N$ luôn chia hết cho $(p + 1)$.",
        "answer": "Đúng"
    }
}

# --- TẠO GIAO DIỆN CHỌN ĐÚNG/SAI ---
user_answers = {}

# Lặp qua từng phát biểu để in ra text và tạo nút chọn
for key, data in statements.items():
    st.markdown(f"**Ý {key})** {data['text']}")
    user_answers[key] = st.radio(
        f"Chọn đáp án cho ý {key}:",
        ["Đúng", "Sai"],
        key=f"q104_{key}",
        index=None,
        horizontal=True
    )
    st.write("") # Thêm một chút khoảng trống giữa các ý

# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q104_check"):
    # Kiểm tra xem người dùng đã chọn hết các ý chưa
    if any(ans is None for ans in user_answers.values()):
        st.warning("⚠️ Vui lòng chọn Đúng hoặc Sai cho TẤT CẢ các phát biểu trước khi kiểm tra!")
    else:
        # Đếm số câu trả lời đúng
        correct_count = 0
        feedback_details = []
        
        for key in statements:
            if user_answers[key] == statements[key]["answer"]:
                correct_count += 1
                feedback_details.append(f"- Ý {key}: ✅ Chính xác")
            else:
                feedback_details.append(f"- Ý {key}: ❌ Sai (Đáp án là {statements[key]['answer']})")
                
        # Hiển thị kết quả tổng quan
        if correct_count == len(statements):
            st.success(f"🎉 Xuất sắc! Bạn đã trả lời đúng trọn vẹn {correct_count}/{len(statements)} ý. Lời giải đã được mở.")
        else:
            st.error(f"Bạn trả lời đúng {correct_count}/{len(statements)} ý. Xem lại chi tiết bên dưới nhé!")
            # In ra chi tiết ý nào đúng, ý nào sai
            for fb in feedback_details:
                st.write(fb)

# --- XEM LỜI GIẢI CHI TIẾT ---
st.markdown("---")

if 'q104_solution_shown' not in st.session_state:
    st.session_state['q104_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q104_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['q104_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q104_solution_shown'] = False 

# Nội dung lời giải
if st.session_state.get('q104_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Kiến thức cần nhớ:** Nếu phân tích tiêu chuẩn của $X = p_1^{a_1} \cdot p_2^{a_2} \dots p_k^{a_k}$ thì:
    - Số lượng ước dương là: $(a_1 + 1)(a_2 + 1) \dots (a_k + 1)$.
    - Tổng các ước dương là: $(1 + p_1 + p_1^2 + \dots + p_1^{a_1}) \dots (1 + p_k + p_k^2 + \dots + p_k^{a_k})$.

    **Giải thích từng ý:**
    
    *   **Ý a) ĐÚNG.** 
    Vì $p, q$ là các số nguyên tố phân biệt nên $N = p^3 \cdot q^2$ đã là dạng phân tích tiêu chuẩn.
    Số lượng ước số nguyên dương của $N$ là: $(3 + 1)(2 + 1) = 4 \cdot 3 = 12$.
    
    *   **Ý b) SAI.** 
    Ta có $N^2 = (p^3 \cdot q^2)^2 = p^6 \cdot q^4$. 
    Số lượng ước số nguyên dương của $N^2$ là: $(6 + 1)(4 + 1) = 7 \cdot 5 = 35$ (chứ không phải lấy $12^2 = 144$).
    
    *   **Ý c) SAI.** 
    Để một số là số chính phương, tất cả các số mũ trong phân tích tiêu chuẩn của nó phải là số chẵn. 
    Ở đây, số mũ của $p$ trong $N$ là $3$ (một số lẻ). Do đó, với mọi số nguyên tố $p$ và $q$, $N$ không bao giờ có thể là số chính phương.
    
    *   **Ý d) ĐÚNG.** 
    Công thức tính tổng tất cả các ước nguyên dương của $N$ là:
    $$S = (1 + p + p^2 + p^3)(1 + q + q^2)$$
    Chú ý phân tích đa thức thành nhân tử: 
    $$1 + p + p^2 + p^3 = (1 + p) + p^2(1 + p) = (1 + p)(1 + p^2)$$
    Vậy $S = (1 + p)(1 + p^2)(1 + q + q^2)$. 
    Rõ ràng trong tích này có chứa nhân tử $(p + 1)$, suy ra tổng các ước của $N$ luôn chia hết cho $(p + 1)$.
    """)
    
st.markdown("---")
