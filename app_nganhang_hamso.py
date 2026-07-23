import streamlit as st

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
st.title("Chuyên đề: Hàm số")
st.markdown("---")

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 1 (HSG 12 - Quảng Ninh 2026)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh image_cf94a3.png
st.markdown(r"""
Cho hàm số $y = \dfrac{2x+2}{x-1}$ có đồ thị $(C)$, hai đường tiệm cận của $(C)$ cắt nhau tại $I$. Đường thẳng $d$ cắt đồ thị $(C)$ tại hai điểm phân biệt $A, B$ đều có hoành độ lớn hơn 1 sao cho tam giác $IAB$ cân tại $I$ và có diện tích bằng $\dfrac{15}{2}$. Viết phương trình đường thẳng $d$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập phương trình đường thẳng $d$ (ví dụ: $y=x+1$):", key="q2_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q2_check"):
    # Chuẩn hóa đầu vào của người dùng để so sánh (loại bỏ khoảng trắng, dấu $, chuyển về chữ thường, v.v.)
    normalized_user_answer = user_answer.strip().replace(" ", "").replace("\$", "").lower()
    
    # Đáp án chính xác là y = -x + 8 hoặc x + y - 8 = 0
    if normalized_user_answer == "y=-x+8" or normalized_user_answer == "x+y-8=0":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại cách giải nhé!")

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
            st.session_state['q2_solution_shown'] = False # Đảm bảo ần nếu chưa đăng nhập

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q2_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm tọa độ điểm I và chuyển hệ tọa độ.**
    
    Hàm số $y = \frac{2x+2}{x-1}$ có các tiệm cận:
    *   Tiệm cận đứng: $x = 1$.
    *   Tiệm cận ngang: $y = 2$.
    Giao điểm $I$ của hai tiệm cận có tọa độ $I(1; 2)$.
    
    Để đơn giản hóa, ta chuyển hệ tọa độ về tâm đối xứng $I$. Đặt:
    *   $X = x - 1 \Rightarrow x = X + 1$
    *   $Y = y - 2 \Rightarrow y = Y + 2$
    
    Khi đó, phương trình $(C)$ trong hệ tọa độ $IXY$ là:
    $Y + 2 = \frac{2(X+1)+2}{X+1-1} \Rightarrow Y + 2 = \frac{2X+4}{X} \Rightarrow Y + 2 = 2 + \frac{4}{X} \Rightarrow XY = 4$.
    Gốc tọa độ mới là $I(0; 0)$. Hai đường tiệm cận là trục tung ($X=0$) và trục hoành ($Y=0$).
    Hai điểm $A, B$ có hoành độ lớn hơn 1 $\Rightarrow X_A, X_B > 0$.
    
    **Bước 2: Tìm phương trình đường thẳng $d$ trong hệ tọa độ $IXY$.**
    
    Tam giác $IAB$ cân tại $I \Rightarrow d$ vuông góc với một trong hai phân giác của các góc tạo bởi hai đường tiệm cận, đi qua $I$.
    Do $X_A, X_B > 0$, hai điểm $A, B$ thuộc nhánh của $(C)$ trong góc phần tư thứ nhất của hệ tọa độ $IXY$.
    Trục đối xứng của $A, B$ là phân giác của góc phần tư thứ nhất, có phương trình $Y=X$.
    Do $\triangle IAB$ cân tại $I$, $A, B$ đối xứng qua $Y=X$, nên $AB$ vuông góc với $Y=X$.
    
    Vậy phương trình đường thẳng $d$ (chứa $AB$) có dạng: $X + Y = c$ (với $c > 0$ do $A, B$ ở góc phần tư thứ nhất).
    $A, B$ là giao điểm của $XY=4$ và $X+Y=c \Rightarrow X(c-X)=4 \Rightarrow X^2 - cX + 4 = 0$.
    Điều kiện cắt tại 2 điểm: $\Delta = c^2 - 16 > 0 \Rightarrow c > 4$ (do $c>0$).
    Khi đó, $X_{A,B} = \frac{c \pm \sqrt{c^2-16}}{2} > 0$.
    
    **Bước 3: Sử dụng điều kiện diện tích.**
    
    Đường thẳng $d$ (pt $X+Y-c=0$) có khoảng cách đến $I(0;0)$ là:
    $d(I, d) = \frac{|0+0-c|}{\sqrt{1^2+1^2}} = \frac{c}{\sqrt{2}}$.
    
    Độ dài cạnh đáy $AB$:
    $AB = \sqrt{(X_B-X_A)^2 + (Y_B-Y_A)^2}$.
    Có $X_B-X_A = \sqrt{c^2-16}$. $Y_B-Y_A = (c-X_B)-(c-X_A) = -(X_B-X_A) = -\sqrt{c^2-16}$.
    $\Rightarrow AB^2 = (\sqrt{c^2-16})^2 + (-\sqrt{c^2-16})^2 = 2(c^2-16)$.
    $\Rightarrow AB = \sqrt{2(c^2-16)}$.
    
    Diện tích tam giác $IAB$:
    $S_{\triangle IAB} = \frac{1}{2} d(I, d) \cdot AB = \frac{1}{2} \cdot \frac{c}{\sqrt{2}} \cdot \sqrt{2(c^2-16)} = \frac{c\sqrt{c^2-16}}{2} = \frac{15}{2}$.
    $\Rightarrow c\sqrt{c^2-16} = 15 \Rightarrow c^2(c^2-16) = 225 \Rightarrow c^4 - 16c^2 - 225 = 0$.
    Giải phương trình trùng phương, ta được $c^2 = 25$ hoặc $c^2 = -9$ (loại).
    Với $c^2 = 25 \Rightarrow c = 5$ (do $c>4$).
    
    **Bước 4: Trở lại hệ tọa độ Oxy.**
    
    Phương trình đường thẳng $d$ trong hệ tọa độ $IXY$ là $X + Y = 5$.
    Trở lại hệ tọa độ $Oxy$ bằng cách thay $X = x - 1, Y = y - 2$:
    $(x - 1) + (y - 2) = 5 \Rightarrow x + y - 3 = 5 \Rightarrow x + y - 8 = 0$ hay $y = -x + 8$.
    
    Vậy phương trình đường thẳng $d$ cần tìm là **$y = -x + 8$** (hoặc **$x + y - 8 = 0$**).
    """)
    
st.markdown("---")




# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 2 (HSG 12 - Hà Tĩnh 2026) </b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Cho hàm số $y = \dfrac{x^2 - x + 2}{x - 2}$ có đồ thị $(C)$ và điểm $A(1; 3)$. Gọi $B$ là điểm cực tiểu và $\Delta$ là đường tiệm cận xiên của $(C)$. Tìm tọa độ điểm $M$ thuộc $\Delta$ sao cho tam giác $ABM$ cân tại $A$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập tọa độ điểm $M$ (ví dụ: (1;2) hoặc 1;2):", key="q4_ans_v2")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q4_check_v2"):
    # Chuẩn hóa đầu vào của người dùng để so sánh
    normalized_user_answer = user_answer.strip().replace(" ", "").replace("(", "").replace(")", "").replace("M", "").replace("m", "").replace(",", ";")
    
    # Đáp án chính xác là (5; 6)
    if normalized_user_answer == "5;6":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại cách giải (lưu ý điều kiện 3 điểm tạo thành tam giác) nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q4_solution_shown_v2' not in st.session_state:
    st.session_state['q4_solution_shown_v2'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q4_solution_v2"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q4_solution_shown_v2'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q4_solution_shown_v2'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q4_solution_shown_v2') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tìm phương trình đường tiệm cận xiên $\Delta$**
    
    Hàm số $y = \frac{x^2 - x + 2}{x - 2}$ có tập xác định $D = \mathbb{R} \setminus \{2\}$.
    
    Ta viết lại hàm số dưới dạng:
    $$y = \frac{x(x - 2) + (x - 2) + 4}{x - 2} = x + 1 + \frac{4}{x - 2}$$
    
    Khi $x \to \pm\infty$, phân thức $\frac{4}{x - 2} \to 0$. Do đó, đường tiệm cận xiên của $(C)$ là:
    $$\Delta: y = x + 1$$
    
    **Bước 2: Tìm tọa độ điểm cực tiểu $B$**
    
    Tính đạo hàm:
    $$y' = 1 - \frac{4}{(x - 2)^2} = \frac{(x - 2)^2 - 4}{(x - 2)^2} = \frac{x^2 - 4x}{(x - 2)^2}$$
    
    Cho $y' = 0 \Leftrightarrow x^2 - 4x = 0 \Leftrightarrow \left[ \begin{array}{l} x = 0 \\ x = 4 \end{array} \right.$
    
    Lập bảng biến thiên, ta thấy hàm số đạt cực tiểu tại $x = 4$.
    Giá trị cực tiểu: $y(4) = \frac{4^2 - 4 + 2}{4 - 2} = 7$.
    Vậy điểm cực tiểu của $(C)$ là $B(4; 7)$.
    
    **Bước 3: Tìm tọa độ điểm $M$**
    
    Vì điểm $M \in \Delta: y = x + 1$, gọi tọa độ $M(m; m + 1)$.
    
    Đề bài yêu cầu tam giác $ABM$ cân tại $A$, điều này tương đương với $AM = AB$ và ba điểm $A, B, M$ không thẳng hàng.
    Ta có $AM^2 = AB^2$.
    
    Với $A(1; 3)$ và $B(4; 7)$:
    *   $AB^2 = (4 - 1)^2 + (7 - 3)^2 = 3^2 + 4^2 = 25$.
    *   $AM^2 = (m - 1)^2 + (m + 1 - 3)^2 = (m - 1)^2 + (m - 2)^2 = 2m^2 - 6m + 5$.
    
    Cho $AM^2 = AB^2$, ta được phương trình:
    $$2m^2 - 6m + 5 = 25$$
    $$\Leftrightarrow 2m^2 - 6m - 20 = 0$$
    $$\Leftrightarrow m^2 - 3m - 10 = 0$$
    $$\Leftrightarrow \left[ \begin{array}{l} m = 5 \\ m = -2 \end{array} \right.$$
    
    **Kiểm tra điều kiện tạo thành tam giác:**
    Ta có $\overrightarrow{AB} = (3; 4)$.
    *   Với $m = 5 \Rightarrow M(5; 6)$. Ta có $\overrightarrow{AM} = (4; 3)$. Vì $\frac{4}{3} \neq \frac{3}{4}$, hai vectơ không cùng phương, $A, B, M$ tạo thành tam giác (Thỏa mãn).
    *   Với $m = -2 \Rightarrow M(-2; -1)$. Ta có $\overrightarrow{AM} = (-3; -4) = -1 \cdot \overrightarrow{AB}$. Suy ra ba điểm $A, B, M$ thẳng hàng, không tạo thành tam giác (Loại).
    
    Vậy tọa độ điểm $M$ cần tìm là **$M(5; 6)$**.
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 3 (HSG 12 - Hà Tĩnh 2026)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh image_d013ae.png
st.markdown(r"""
Công ty X cần vận chuyển hàng đến một địa điểm cách công ty 100 dặm. Khi xe chở hàng di chuyển với tốc độ $x$ (dặm/giờ) thì chi phí nhiên liệu (USD) trên mỗi dặm đường là $C(x) = \dfrac{1}{5}\left(\dfrac{64}{x} + \dfrac{9}{100}x\right)$. Ngoài ra, giá thuê tài xế là 16 USD mỗi giờ lái xe. Biết tốc độ không vượt quá 50 dặm/giờ. Hỏi chi phí nhỏ nhất mà công ty phải trả trên mỗi chuyến hàng là bao nhiêu USD?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập chi phí nhỏ nhất (USD) (ví dụ: 150):", key="q5_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q5_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng, chữ "usd", v.v.)
    normalized_user_answer = user_answer.strip().lower().replace(" ", "").replace("usd", "").replace("$", "")
    
    # Đáp án chính xác là 144
    if normalized_user_answer == "144":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Bạn thử tính toán lại cẩn thận hàm tổng chi phí nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q5_solution_shown' not in st.session_state:
    st.session_state['q5_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q5_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q5_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q5_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q5_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Thiết lập các biểu thức chi phí theo $x$**
    
    Gọi $x$ (dặm/giờ) là tốc độ của xe chở hàng. Theo giả thiết, điều kiện của $x$ là: $0 < x \le 50$.
    Quãng đường di chuyển là $S = 100$ dặm.
    
    *   **Thời gian di chuyển:** 
        $$t = \frac{S}{x} = \frac{100}{x} \text{ (giờ)}$$
    
    *   **Chi phí tài xế cho 1 chuyến:** 
        $$16 \cdot t = 16 \cdot \frac{100}{x} = \frac{1600}{x} \text{ (USD)}$$
    
    *   **Chi phí nhiên liệu cho 1 chuyến:** Bằng chi phí nhiên liệu trên 1 dặm nhân với quãng đường (100 dặm).
        $$100 \cdot C(x) = 100 \cdot \frac{1}{5}\left(\frac{64}{x} + \frac{9}{100}x\right) = 20\left(\frac{64}{x} + \frac{9}{100}x\right) = \frac{1280}{x} + \frac{9x}{5} \text{ (USD)}$$
    
    **Bước 2: Lập hàm tổng chi phí và tìm giá trị nhỏ nhất**
    
    Tổng chi phí công ty phải trả cho mỗi chuyến hàng là hàm số $f(x)$ với $x \in (0; 50]$:
    $$f(x) = \text{Chi phí tài xế} + \text{Chi phí nhiên liệu}$$
    $$f(x) = \frac{1600}{x} + \frac{1280}{x} + \frac{9x}{5} = \frac{2880}{x} + \frac{9x}{5}$$
    
    Để tìm giá trị nhỏ nhất của $f(x)$, ta có thể sử dụng Bất đẳng thức AM-GM (Cauchy) cho hai số dương $\frac{2880}{x}$ và $\frac{9x}{5}$:
    $$f(x) = \frac{2880}{x} + \frac{9x}{5} \ge 2\sqrt{\frac{2880}{x} \cdot \frac{9x}{5}} = 2\sqrt{\frac{25920}{5}} = 2\sqrt{5184} = 2 \cdot 72 = 144$$
    
    Dấu "=" xảy ra khi và chỉ khi:
    $$\frac{2880}{x} = \frac{9x}{5} \Leftrightarrow 9x^2 = 14400 \Leftrightarrow x^2 = 1600 \Leftrightarrow x = 40 \text{ (Thỏa mãn } 0 < x \le 50\text{)}$$
    
    *(Lưu ý: Học sinh cũng có thể tính đạo hàm $f'(x) = -\frac{2880}{x^2} + \frac{9}{5}$, giải $f'(x) = 0 \Rightarrow x = 40$ và lập bảng biến thiên để tìm Min trên khoảng $(0; 50]$ ra kết quả tương tự).*
    
    **Kết luận:** Chi phí nhỏ nhất mà công ty phải trả trên mỗi chuyến hàng là **144 USD** (khi xe chạy với tốc độ 40 dặm/giờ).
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 4 (HSG 12 - Thanh Hóa 2026)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh image_d0671d.png
st.markdown(r"""
Trong hệ trục tọa độ $Oxy$, cho đồ thị hàm số $(C): y = \dfrac{x^2 + x + 2}{x + 1}$ mô tả chuyển động của hai tàu đánh cá $A$ và $B$ (1 đơn vị trên mỗi trục tọa độ tính bằng 1 km). 
Biết quỹ đạo chuyển động của hai tàu luôn thuộc về hai nhánh khác nhau của đồ thị $(C)$. Tính khoảng cách ngắn nhất (đơn vị km) giữa hai tàu đánh cá $A$ và $B$ (kết quả làm tròn đến hàng phần trăm).
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập khoảng cách ngắn nhất (làm tròn đến 2 chữ số thập phân, ví dụ: 1.23):", key="q9_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q9_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng, đổi dấu phẩy thành dấu chấm)
    normalized_user_answer = user_answer.strip().replace(" ", "").replace(",", ".")
    
    # Đáp án chính xác là 6.22
    if normalized_user_answer == "6.22":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại cách dùng bất đẳng thức AM-GM và làm tròn số nhé!")

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
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Chuyển hệ trục tọa độ**
    
    Hàm số $y = \dfrac{x^2 + x + 2}{x + 1} = x + \dfrac{2}{x + 1}$ có tập xác định $D = \mathbb{R} \setminus \{-1\}$.
    Đồ thị $(C)$ có tiệm cận đứng $x = -1$ và tiệm cận xiên $y = x$.
    Giao điểm của hai đường tiệm cận là $I(-1; -1)$, đây cũng là tâm đối xứng của đồ thị.
    
    Thực hiện phép tịnh tiến hệ trục $Oxy$ về gốc $I(-1; -1)$ bằng công thức:
    $$\begin{cases} x = X - 1 \\ y = Y - 1 \end{cases}$$
    
    Phương trình đồ thị $(C)$ trong hệ trục $IXY$ trở thành:
    $$Y - 1 = (X - 1) + \dfrac{2}{(X - 1) + 1} \Leftrightarrow Y = X + \dfrac{2}{X}$$
    
    **Bước 2: Gọi tọa độ hai điểm $A, B$ trên hai nhánh và tính độ dài $AB$**
    
    Vì $A, B$ nằm trên hai nhánh khác nhau của đồ thị nên hoành độ của chúng trong hệ trục $IXY$ sẽ trái dấu.
    Gọi $A\left(-a; -a - \dfrac{2}{a}\right)$ với $a > 0$ (điểm thuộc nhánh trái).
    Gọi $B\left(b; b + \dfrac{2}{b}\right)$ với $b > 0$ (điểm thuộc nhánh phải).
    
    Bình phương khoảng cách giữa $A$ và $B$ là:
    $$AB^2 = (X_B - X_A)^2 + (Y_B - Y_A)^2$$
    $$AB^2 = (a + b)^2 + \left(a + b + \dfrac{2}{a} + \dfrac{2}{b}\right)^2$$
    $$AB^2 = (a + b)^2 + \left(a + b + \dfrac{2(a + b)}{ab}\right)^2 = (a + b)^2 \left[ 1 + \left(1 + \dfrac{2}{ab}\right)^2 \right]$$
    
    **Bước 3: Đánh giá tìm giá trị nhỏ nhất**
    
    Theo bất đẳng thức AM-GM, ta có: $(a + b)^2 \ge 4ab \Rightarrow ab \le \dfrac{(a + b)^2}{4} \Rightarrow \dfrac{2}{ab} \ge \dfrac{8}{(a + b)^2}$.
    
    Do đó:
    $$AB^2 \ge (a + b)^2 \left[ 1 + \left(1 + \dfrac{8}{(a + b)^2}\right)^2 \right]$$
    
    Đặt $t = (a + b)^2$ với $t > 0$, ta xét hàm số:
    $$f(t) = t \left[ 1 + \left(1 + \dfrac{8}{t}\right)^2 \right] = t \left( 1 + 1 + \dfrac{16}{t} + \dfrac{64}{t^2} \right) = 2t + \dfrac{64}{t} + 16$$
    
    Tiếp tục áp dụng bất đẳng thức AM-GM cho hai số dương $2t$ và $\dfrac{64}{t}$:
    $$2t + \dfrac{64}{t} \ge 2\sqrt{2t \cdot \dfrac{64}{t}} = 2\sqrt{128} = 16\sqrt{2}$$
    
    Suy ra: $AB^2 \ge 16\sqrt{2} + 16$.
    Giá trị nhỏ nhất của $AB$ là: $AB_{min} = \sqrt{16\sqrt{2} + 16} = 4\sqrt{\sqrt{2} + 1}$.
    
    Dấu "=" xảy ra khi và chỉ khi:
    $$\begin{cases} a = b \\ 2t = \dfrac{64}{t} \end{cases} \Leftrightarrow \begin{cases} a = b \\ t^2 = 32 \end{cases} \Leftrightarrow \begin{cases} a = b \\ (2a)^2 = 4\sqrt{2} \end{cases} \Leftrightarrow a = b = \sqrt[4]{2}$$
    (Thỏa mãn điều kiện).
    
    **Bước 4: Tính toán kết quả**
    
    Ta có: $AB_{min} = 4\sqrt{\sqrt{2} + 1} \approx 6.21509$.
    Làm tròn đến hàng phần trăm, khoảng cách ngắn nhất là **$6.22$** (km).
    """)
    
st.markdown("---")



# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 5 (HSG 12 - Thanh Hóa 2026)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh image_d07166.png
# Nội dung câu hỏi từ hình ảnh image_d07166.png
st.markdown(r"""
Một phần đường chạy của tàu lượn siêu tốc khi gắn hệ trục tọa độ $Oxy$ được mô phỏng như hình vẽ, đơn vị trên mỗi trục là mét. Biết đường chạy của nó là một phần đồ thị hàm số bậc ba $y = ax^3 + bx^2 + cx + d$ ($0 \le x \le 90$); tàu lượn siêu tốc đi qua các điểm $A(0; 30), C(50; 30), D(80; 30)$ đồng thời đạt độ cao nhỏ nhất so với mặt đất là 4m (trong khoảng từ 0 đến 50).

Độ cao lớn nhất mà tàu lượn siêu tốc đạt được là bao nhiêu mét so với mặt đất? (kết quả làm tròn đến hàng phần chục).
""")

# Hiển thị hình ảnh mô phỏng
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/hsgth.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/hsgth.PNG'. Vui lòng kiểm tra lại đường dẫn.")


# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập độ cao lớn nhất (làm tròn đến 1 chữ số thập phân, ví dụ: 45.2):", key="q10_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q10_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng, đổi phẩy thành chấm)
    normalized_user_answer = user_answer.strip().replace(" ", "").replace(",", ".")
    
    # Đáp án chính xác là 40.7
    if normalized_user_answer == "40.7":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại hàm số và cách làm tròn nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q10_solution_shown' not in st.session_state:
    st.session_state['q10_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q10_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q10_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q10_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q10_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Lập phương trình hàm số bậc ba**
    
    Gọi phương trình đường chạy là $y = f(x) = ax^3 + bx^2 + cx + d$ ($0 \le x \le 90$).
    Đồ thị hàm số đi qua 3 điểm có cùng tung độ bằng 30 là $A(0; 30), C(50; 30), D(80; 30)$. 
    Suy ra phương trình $f(x) - 30 = 0$ có 3 nghiệm là $x_1 = 0, x_2 = 50, x_3 = 80$.
    
    Do đó, hàm số có dạng:
    $$f(x) - 30 = a(x - 0)(x - 50)(x - 80)$$
    $$\Leftrightarrow f(x) = a(x^3 - 130x^2 + 4000x) + 30$$
    
    **Bước 2: Sử dụng dữ kiện điểm cực tiểu để tìm hệ số a**
    
    Đạo hàm của hàm số:
    $$f'(x) = a(3x^2 - 260x + 4000)$$
    
    Cho $f'(x) = 0 \Leftrightarrow 3x^2 - 260x + 4000 = 0 \Leftrightarrow \left[ \begin{array}{l} x = 20 \\ x = \dfrac{200}{3} \end{array} \right.$
    
    Trong khoảng $(0; 50)$, điểm cực trị là $x = 20$. 
    Vì đồ thị đạt độ cao nhỏ nhất là $4$m trong khoảng này, nên $x = 20$ chính là điểm cực tiểu của hàm số và $f(20) = 4$.
    
    Thay $x = 20$ vào phương trình hàm số ta được:
    $$a \cdot 20(20 - 50)(20 - 80) + 30 = 4$$
    $$\Leftrightarrow a \cdot 20 \cdot (-30) \cdot (-60) = -26$$
    $$\Leftrightarrow 36000a = -26 \Leftrightarrow a = -\dfrac{26}{36000} = -\dfrac{13}{18000}$$
    
    Vậy phương trình hàm số đầy đủ là: $f(x) = -\dfrac{13}{18000}(x^3 - 130x^2 + 4000x) + 30$.
    
    **Bước 3: Tìm độ cao lớn nhất của tàu lượn**
    
    Vì hệ số $a < 0$, điểm cực đại của đồ thị sẽ nằm tại nghiệm còn lại của đạo hàm, tức là tại $x = \dfrac{200}{3}$ (thuộc đoạn $[0; 90]$).
    
    Ta tính giá trị hàm số tại các điểm:
    *   $f(0) = 30$
    *   $f(90) = -\dfrac{13}{18000} \cdot 90(90 - 50)(90 - 80) + 30 = -26 + 30 = 4$
    *   Tại điểm cực đại $x = \dfrac{200}{3}$:
    $$f\left(\dfrac{200}{3}\right) = -\dfrac{13}{18000} \cdot \left(\dfrac{200}{3}\right) \cdot \left(\dfrac{200}{3} - 50\right) \cdot \left(\dfrac{200}{3} - 80\right) + 30$$
    $$f\left(\dfrac{200}{3}\right) = -\dfrac{13}{18000} \cdot \dfrac{200}{3} \cdot \dfrac{50}{3} \cdot \left(-\dfrac{40}{3}\right) + 30$$
    $$f\left(\dfrac{200}{3}\right) = \dfrac{13 \cdot 400000}{18000 \cdot 27} + 30 = \dfrac{2600}{243} + 30 = \dfrac{9890}{243} \approx 40.699$$
    
    So sánh các giá trị, độ cao lớn nhất mà tàu lượn đạt được là khoảng $40.699$m.
    Làm tròn đến hàng phần chục, kết quả là **$40.7$**.
    """)
    
st.markdown("---")



import streamlit as st

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 6 (THPT Lê Thánh Tông HCM 2026)</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi từ hình ảnh image_d0db1b.png
st.markdown(r"""
Một công ty công nghệ cung cấp gói lưu trữ dữ liệu doanh nghiệp với giá niêm yết $200.000$ đồng/tháng và đang có $400$ khách hàng. Phòng kinh doanh xác định được quy luật: Cứ giảm giá $10.000$ đồng thì sẽ có thêm $50$ khách hàng mới. 

Tuy nhiên, do hiện tượng quá tải băng thông, chi phí vận hành $C(n)$ (nghìn đồng) không cố định mà biến thiên theo hàm bậc hai của số lượng khách hàng $n$, được xác định bởi công thức: 
$$C(n) = 28n + 0,01n^2 + 15.000$$

Công ty cần chốt giá bán bao nhiêu nghìn đồng để lợi nhuận đạt mức tối đa?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập giá bán cần chốt (nghìn đồng) (ví dụ: 150):", key="q11_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q11_check"):
    # Chuẩn hóa đầu vào
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 160
    if normalized_user_answer == "160":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy thiết lập hàm doanh thu, chi phí theo số lần giảm giá và kiểm tra lại nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q11_solution_shown' not in st.session_state:
    st.session_state['q11_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q11_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q11_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q11_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q11_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Lập hàm số biểu diễn số lượng khách hàng và giá bán**
    
    Gọi $x$ là số lần giảm giá $10.000$ đồng ($x \ge 0$).
    Khi đó, giá bán mới của gói lưu trữ tính theo nghìn đồng là: 
    $$p(x) = 200 - 10x \text{ (nghìn đồng)}$$
    
    Số lượng khách hàng tương ứng sau khi giảm giá là: 
    $$n(x) = 400 + 50x \text{ (khách hàng)}$$
    
    **Bước 2: Thiết lập hàm Doanh thu và hàm Chi phí**
    
    *   **Hàm Doanh thu (nghìn đồng):**
        $$R(x) = p(x) \cdot n(x) = (200 - 10x)(400 + 50x)$$
        $$R(x) = 80000 + 10000x - 4000x - 500x^2$$
        $$R(x) = -500x^2 + 6000x + 80000$$
        
    *   **Hàm Chi phí (nghìn đồng):**
        Theo đề bài $C(n) = 28n + 0,01n^2 + 15000$. Thay $n(x) = 400 + 50x$ vào ta được:
        $$C(x) = 28(400 + 50x) + 0,01(400 + 50x)^2 + 15000$$
        $$C(x) = 11200 + 1400x + 0,01(160000 + 40000x + 2500x^2) + 15000$$
        $$C(x) = 11200 + 1400x + 1600 + 400x + 25x^2 + 15000$$
        $$C(x) = 25x^2 + 1800x + 27800$$
        
    **Bước 3: Lập hàm Lợi nhuận và tìm giá trị tối đa**
    
    Hàm lợi nhuận $P(x)$ bằng Doanh thu trừ đi Chi phí:
    $$P(x) = R(x) - C(x)$$
    $$P(x) = (-500x^2 + 6000x + 80000) - (25x^2 + 1800x + 27800)$$
    $$P(x) = -525x^2 + 4200x + 52200$$
    
    Đây là một hàm số bậc hai ẩn $x$ với hệ số $a = -525 < 0$. Đồ thị là một parabol có bề lõm hướng xuống dưới nên sẽ đạt giá trị lớn nhất tại đỉnh.
    Tọa độ đỉnh đạt được tại:
    $$x = -\dfrac{b}{2a} = -\dfrac{4200}{2 \cdot (-525)} = \dfrac{4200}{1050} = 4$$
    
    Vậy công ty cần thực hiện giảm giá $4$ lần để đạt lợi nhuận tối đa.
    Giá bán gói lưu trữ cần chốt là:
    $$p(4) = 200 - 10 \cdot 4 = 160 \text{ (nghìn đồng)}$$
    
    **Kết luận:** Công ty cần chốt giá bán **$160$** nghìn đồng.
    """)
    
st.markdown("---")



