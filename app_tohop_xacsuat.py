import streamlit as st
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
    '<h2 style="text-align: center; color: blue;">CHUYÊN ĐỀ: TỔ HỢP XÁC SUẤT</h2>',
    unsafe_allow_html=True
)
st.markdown("---")



# --- CÂU HỎI 1: TỔ HỢP XÁC SUẤT ---
st.markdown(
    '<b style="color: blue;">Câu 1 (Đề thi Tốt nghiệp THPT 2025)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Bạn Nam tham gia cuộc thi giải một mật thư. Theo quy tắc của cuộc thi, người chơi cần chọn ra sáu số từ tập $S = \{31; 32; 33; 34; 35; 36; 37; 38; 39\}$ và xếp mỗi số vào đúng một vị trí trong sáu vị trí $A, B, C, M, N, P$ như hình bên sao cho mỗi vị trí chỉ được xếp một số. Mật thư sẽ được giải nếu các bộ ba số xuất hiện ở những bộ ba vị trí $(A, M, B); (B, N, C); (C, P, A)$ tạo thành các cấp số cộng theo thứ tự đó. Bạn Nam chọn ngẫu nhiên sáu số trong tập $S$ và xếp ngẫu nhiên vào các vị trí được yêu cầu. Gọi xác suất để bạn Nam giải được mật thư ở lần chọn và xếp đó là $a$. Giá trị của $\dfrac{3}{a}$ bằng bao nhiêu?
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer = st.text_input("Nhập giá trị của 3/a (ví dụ: 1234):", key="q1_ans")

# --- CHÈN HÌNH ẢNH ---
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/image_4ed3e2.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/image_4ed3e2.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q1_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    # Đáp án chính xác là 3780
    if normalized_user_answer == "3780":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân tích tính chẵn lẻ của A, B, C và điều kiện không tạo thành cấp số cộng để loại các bộ ba trùng lặp nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q1_solution_shown' not in st.session_state:
    st.session_state['q1_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q1_solution_btn"):
        if st.session_state.get('logged_in'):
            st.session_state['q1_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q1_solution_shown'] = False 

# Hiển thị lời giải chi tiết khi đủ điều kiện
if st.session_state.get('q1_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính số phần tử của không gian mẫu**
    
    * Tập $S = \{31; 32; 33; 34; 35; 36; 37; 38; 39\}$ có $9$ phần tử.
    * Việc chọn ngẫu nhiên $6$ số từ tập $S$ và xếp vào $6$ vị trí phân biệt $A, B, C, M, N, P$ chính là một chỉnh hợp chập $6$ của $9$.
    * Số phần tử của không gian mẫu là:
        $$n(\Omega) = A_9^6 = 9 \cdot 8 \cdot 7 \cdot 6 \cdot 5 \cdot 4 = 60.480 \text{ (cách)}$$
    
    **Bước 2: Phân tích điều kiện của biến cố**
    
    Gọi biến cố $X$: "Bạn Nam giải được mật thư".
    * Theo giả thiết, các bộ ba $(A, M, B); (B, N, C); (C, P, A)$ lập thành cấp số cộng. Điều kiện này tương đương với:
        $$\begin{cases} A + B = 2M \\ B + C = 2N \\ C + A = 2P \end{cases}$$
    * Vì vế phải $2M, 2N, 2P$ là các số chẵn nên các tổng $A+B, B+C, C+A$ phải là số chẵn. Do đó, $A, B, C$ bắt buộc phải có cùng tính chẵn lẻ (cùng là số chẵn hoặc cùng là số lẻ).
    * Mặt khác, $6$ số $A, B, C, M, N, P$ là các số phân biệt nên tập hợp $3$ số $\{A, B, C\}$ không được tạo thành một cấp số cộng (Ví dụ, nếu $A, B, C$ lập thành cấp số cộng thì $A+C=2B \Rightarrow 2P = 2B \Rightarrow P = B$, trái với điều kiện các số phân biệt).
    
    **Bước 3: Đếm số kết quả thuận lợi cho biến cố $X$**
    
    * **Trường hợp 1:** $A, B, C$ cùng là số lẻ.
        * Tập các số lẻ trong $S$ là $\{31; 33; 35; 37; 39\}$ (có $5$ số).
        * Số cách chọn $3$ số lẻ là $C_5^3 = 10$ (cách).
        * Trong $10$ bộ số này, có $4$ bộ lập thành cấp số cộng là: $\{31; 33; 35\}, \{33; 35; 37\}, \{35; 37; 39\}$ (công sai 2) và $\{31; 35; 39\}$ (công sai 4).
        * Suy ra có $10 - 4 = 6$ bộ $3$ số lẻ thoả mãn không tạo thành cấp số cộng.
        * Với mỗi bộ thỏa mãn, có $3! = 6$ cách xếp vào $3$ vị trí $A, B, C$. Khi $A, B, C$ cố định, $M, N, P$ sẽ được xác định duy nhất.
        * Số kết quả trong trường hợp 1 là: $6 \times 6 = 36$ (cách).
        
    * **Trường hợp 2:** $A, B, C$ cùng là số chẵn.
        * Tập các số chẵn trong $S$ là $\{32; 34; 36; 38\}$ (có $4$ số).
        * Số cách chọn $3$ số chẵn là $C_4^3 = 4$ (cách).
        * Trong $4$ bộ số này, có $2$ bộ lập thành cấp số cộng là: $\{32; 34; 36\}, \{34; 36; 38\}$.
        * Suy ra có $4 - 2 = 2$ bộ $3$ số chẵn thoả mãn.
        * Với mỗi bộ thỏa mãn, có $3! = 6$ cách xếp vào $3$ vị trí $A, B, C$.
        * Số kết quả trong trường hợp 2 là: $2 \times 6 = 12$ (cách).
        
    * Vậy tổng số kết quả thuận lợi cho biến cố $X$ là:
        $$n(X) = 36 + 12 = 48 \text{ (cách)}$$
    
    **Bước 4: Tính xác suất và kết quả bài toán**
    
    * Xác suất để bạn Nam giải được mật thư là:
        $$a = P(X) = \dfrac{n(X)}{n(\Omega)} = \dfrac{48}{60.480} = \dfrac{1}{1260}$$
    * Giá trị cần tính là:
        $$\dfrac{3}{a} = \dfrac{3}{\dfrac{1}{1260}} = 3 \times 1260 = 3780$$
        
    **Kết luận:** Giá trị của $\dfrac{3}{a}$ bằng **$3780$**.
    """)

st.markdown("---")


