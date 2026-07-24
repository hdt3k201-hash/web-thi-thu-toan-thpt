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

import streamlit as st

# --- CÂU HỎI 2: ---
st.markdown(
    '<b style="color: blue;">Câu 2 (Đề thi Tốt nghiệp THPT 2025)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có bốn ngăn (trong một giá để sách) được đánh số thứ tự $1, 2, 3, 4$ và tám quyển sách khác nhau. Bạn An xếp hết tám quyển sách nói trên vào bốn ngăn đó sao cho mỗi ngăn có ít nhất một quyển sách và các quyển sách được xếp thẳng đứng thành một hàng ngang với gáy sách quay ra ngoài ở mỗi ngăn. Khi đã xếp xong tám quyển sách, hai cách xếp của bạn An được gọi là giống nhau nếu chúng thỏa mãn đồng thời hai điều kiện sau đây:
+ Với từng ngăn, số lượng quyển sách ở ngăn đó là như nhau trong cả hai cách xếp;
+ Với từng ngăn, thứ tự từ trái sang phải của các quyển sách được xếp là như nhau trong cả hai cách xếp.
Gọi $T$ là số cách xếp đôi một khác nhau của bạn An. Giá trị của $\dfrac{T}{400}$ bằng bao nhiêu?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (ví dụ: 1234):", key="q2_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q2_check"):
    normalized_user_answer = user_answer.strip()
    
    if normalized_user_answer == "3528":
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
            st.session_state['q2_solution_shown'] = False # Đảm bảo ẩn nếu chưa đăng nhập

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q2_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Sắp xếp các quyển sách thành một hàng ngang**
    
    * Số cách xếp 8 quyển sách khác nhau thành một hàng ngang là hoán vị của 8 phần tử:
        $$8! = 40.320 	ext{ (cách)}$$
    
    **Bước 2: Sử dụng phương pháp "vách ngăn"**
    
    * Khi xếp 8 quyển sách thành một hàng ngang, ta có $7$ khoảng trống ở giữa các quyển sách (không tính hai đầu mút vì mỗi ngăn phải có ít nhất 1 quyển sách).
    * Việc chia 8 quyển sách này vào 4 ngăn khác nhau (mỗi ngăn ít nhất 1 quyển) tương đương với việc đặt $3$ vách ngăn vào $3$ trong số $7$ khoảng trống đó (để chia thành 4 phần tương ứng cho 4 ngăn theo thứ tự 1, 2, 3, 4).
    * Số cách đặt 3 vách ngăn là tổ hợp chập 3 của 7:
        $$C_7^3 = \dfrac{7!}{3!(7-3)!} = 35 	ext{ (cách)}$$
    
    **Bước 3: Tính tổng số cách xếp $T$ và giá trị cần tìm**
    
    * Theo quy tắc nhân, tổng số cách xếp $T$ là:
        $$T = 8! \cdot C_7^3 = 40.320 \cdot 35 = 1.411.200 	ext{ (cách)}$$
    * Theo yêu cầu bài toán, ta cần tính giá trị của $\dfrac{T}{400}$:
        $$\dfrac{T}{400} = \dfrac{1.411.200}{400} = 3528$$
    
    **Kết luận:** Giá trị của $\dfrac{T}{400}$ bằng **$3528$**.
    """)
    
st.markdown("---")

import streamlit as st

# --- CÂU HỎI 3 ---
st.markdown(
    '<b style="color: blue;">Câu 3 (Đề thi minh họa Tốt nghiệp THPT 2025)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Có hai chiếc hộp, hộp I có $6$ quả bóng màu đỏ và $4$ quả bóng màu vàng, hộp II có $7$ quả bóng màu đỏ và $3$ quả bóng màu vàng, các quả bóng có cùng kích thước và khối lượng. Lấy ngẫu nhiên một quả bóng từ hộp I bỏ vào hộp II. Sau đó, lấy ra ngẫu nhiên một quả bóng từ hộp II. Tính xác suất để quả bóng được lấy ra từ hộp II là quả bóng được chuyển từ hộp I sang, biết rằng quả bóng đó có màu đỏ (làm tròn kết quả đến hàng phần trăm).
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (ví dụ: 0.12):", key="q3_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q3_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    if normalized_user_answer in ["0.08", "0,08"]:
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Sử dụng công thức xác suất có điều kiện $P(C|B) = \dfrac{P(C \cap B)}{P(B)}$.")

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
    Gọi $B$ là biến cố: "Quả bóng lấy ra từ hộp II là bóng màu đỏ".
    Gọi $C$ là biến cố: "Quả bóng lấy ra từ hộp II chính là quả bóng được chuyển từ hộp I sang".
    
    Ta cần tính xác suất có điều kiện: $P(C|B) = \dfrac{P(C \cap B)}{P(B)}$.
    
    **Bước 1: Tính xác suất lấy được bóng đỏ từ hộp II $P(B)$**
    
    Gọi $A_1$ là biến cố "Quả bóng chuyển từ hộp I sang hộp II có màu đỏ".
    $$P(A_1) = \dfrac{6}{10} = \dfrac{3}{5}$$
    Khi đó, hộp II có $8$ bóng đỏ và $3$ bóng vàng (tổng $11$ quả). Xác suất lấy được bóng đỏ lúc này là:
    $$P(B|A_1) = \dfrac{8}{11}$$
    
    Gọi $A_2$ là biến cố "Quả bóng chuyển từ hộp I sang hộp II có màu vàng".
    $$P(A_2) = \dfrac{4}{10} = \dfrac{2}{5}$$
    Khi đó, hộp II có $7$ bóng đỏ và $4$ bóng vàng (tổng $11$ quả). Xác suất lấy được bóng đỏ lúc này là:
    $$P(B|A_2) = \dfrac{7}{11}$$
    
    Áp dụng công thức xác suất toàn phần:
    $$P(B) = P(A_1) \cdot P(B|A_1) + P(A_2) \cdot P(B|A_2) = \dfrac{3}{5} \cdot \dfrac{8}{11} + \dfrac{2}{5} \cdot \dfrac{7}{11} = \dfrac{38}{55}$$
    
    **Bước 2: Tính xác suất $P(C \cap B)$**
    
    $C \cap B$ là biến cố "Quả bóng lấy ra từ hộp II là quả bóng chuyển từ hộp I sang VÀ có màu đỏ".
    Điều này chỉ xảy ra khi quả bóng chuyển từ hộp I sang phải là bóng đỏ (tức là biến cố $A_1$ xảy ra).
    
    Khi $A_1$ xảy ra, hộp II có tổng cộng $11$ quả bóng, trong đó có đúng $1$ quả bóng đỏ vừa được chuyển sang. 
    Xác suất bốc trúng đúng quả bóng đó là $\dfrac{1}{11}$.
    
    Do đó:
    $$P(C \cap B) = P(A_1) \cdot P(C \cap B | A_1) = \dfrac{3}{5} \cdot \dfrac{1}{11} = \dfrac{3}{55}$$
    
    **Bước 3: Tính xác suất cần tìm và làm tròn**
    
    $$P(C|B) = \dfrac{P(C \cap B)}{P(B)} = \dfrac{\dfrac{3}{55}}{\dfrac{38}{55}} = \dfrac{3}{38} \approx 0,0789...$$
    
    Làm tròn kết quả đến hàng phần trăm, ta được giá trị **$0,08$**.
    
    **Kết luận:** Xác suất cần tìm là **$0,08$**.
    """)
    
st.markdown("---")

import streamlit as st

# --- CÂU HỎI 4 ---
st.markdown(
    '<b style="color: blue;">Câu 4 (Đề thi  Tốt nghiệp THPT 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Trong một trò chơi bạn Bình cần vượt qua một thử thách. Theo yêu cầu của thử thách, Bình cần điền tất cả 15 số thuộc tập hợp $\{0; 1; 2; 3; 4; 5; 6; 7; 8; 10; 11; 12; 15; 16; 20\}$ vào 15 ô vuông trong hình dưới thỏa mãn đồng thời ba điều kiện sau:
+ Mỗi ô điền đúng một số và mỗi số chỉ được sử dụng một lần;
+ Hiệu hai số ở hai ô bất kì khác nhau trên cùng một hàng không chia hết cho 5;
+ Hiệu hai số ở hai ô bất kì khác nhau trên cùng một cột không chia hết cho 5.

Hai cách điền gọi là giống nhau nếu số điền ở mỗi ô tương ứng trong 15 ô là giống nhau (không tính đến thứ tự điền các số vào 15 ô vuông). Gọi $H$ là số cách điền khác nhau để bạn Bình vượt qua được thử thách. Giá trị của $\dfrac{H}{30}$ bằng bao nhiêu?
""")

# --- CHÈN HÌNH ẢNH (NẾU CÓ) ---
# (Phần mẫu chèn ảnh chuẩn theo yêu cầu của thầy - Ảnh bảng ô vuông)
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/tn2026.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/tn2026.PNG'. Vui lòng kiểm tra lại đường dẫn.")


# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án :", key="q4_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q4_check"):
    normalized_user_answer = user_answer.strip()
    
    if normalized_user_answer == "1152":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy phân chia các số thành các nhóm dựa trên số dư khi chia cho 5 và xếp vào các đường chéo của bảng!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q4_solution_shown' not in st.session_state:
    st.session_state['q4_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q4_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q4_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q4_solution_shown'] = False

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q4_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân loại các số theo số dư khi chia cho 5**
    
    Ta chia 15 số đã cho thành các tập hợp dựa vào số dư khi chia cho 5:
    * Tập $A_0$ (chia hết cho 5): $\{0; 5; 10; 15; 20\}$ $\Rightarrow$ có 5 số.
    * Tập $A_1$ (chia 5 dư 1): $\{1; 6; 11; 16\}$ $\Rightarrow$ có 4 số.
    * Tập $A_2$ (chia 5 dư 2): $\{2; 7; 12\}$ $\Rightarrow$ có 3 số.
    * Tập $A_3$ (chia 5 dư 3): $\{3; 8\}$ $\Rightarrow$ có 2 số.
    * Tập $A_4$ (chia 5 dư 4): $\{4\}$ $\Rightarrow$ có 1 số.
    
    **Bước 2: Phân tích điều kiện bài toán**
    
    * Theo giả thiết, hiệu hai số trên cùng một hàng hoặc cùng một cột không được chia hết cho 5. Điều này tương đương với việc: **Không có hai số nào trên cùng một hàng hoặc cùng một cột có cùng số dư khi chia cho 5.**
    * Nghĩa là trên mỗi hàng và mỗi cột, mỗi nhóm $A_i$ ($i \in \{0, 1, 2, 3, 4\}$) chỉ được xuất hiện nhiều nhất 1 lần.
    
    **Bước 3: Xếp các nhóm số vào bảng**
    
    Bảng có dạng bậc thang gồm 15 ô. Số ô trên mỗi hàng và mỗi cột giảm dần từ 5 đến 1.
    
    * **Nhóm $A_0$ (5 số):** Cần điền vào 5 ô khác hàng và khác cột. Hàng 5 chỉ có duy nhất ô $(5, 1)$, nên bắt buộc 1 số của $A_0$ phải nằm ở đây. Do Cột 1 đã có số của $A_0$, ô chứa $A_0$ ở Hàng 4 phải nằm ở $(4, 2)$. Lập luận tương tự, 5 số của $A_0$ bắt buộc phải lấp đầy đường chéo chính: $(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)$.
        Số cách xếp 5 số này là: $5! = 120 \text{ (cách)}$.
    
    * **Nhóm $A_1$ (4 số):** Tương tự, bỏ đi các ô đã điền, 4 số của $A_1$ bắt buộc phải được xếp vào đường chéo kế tiếp: $(4, 1), (3, 2), (2, 3), (1, 4)$. 
        Số cách xếp 4 số này là: $4! = 24 \text{ (cách)}$.
    
    * **Nhóm $A_2$ (3 số):** Bắt buộc xếp vào đường chéo: $(3, 1), (2, 2), (1, 3)$. 
        Số cách xếp là: $3! = 6 \text{ (cách)}$.
    
    * **Nhóm $A_3$ (2 số):** Bắt buộc xếp vào đường chéo: $(2, 1), (1, 2)$. 
        Số cách xếp là: $2! = 2 \text{ (cách)}$.
    
    * **Nhóm $A_4$ (1 số):** Điền vào ô cuối cùng còn lại $(1, 1)$. 
        Số cách xếp là: $1! = 1 \text{ (cách)}$.
    
    **Bước 4: Tính $H$ và kết quả**
    
    * Theo quy tắc nhân, tổng số cách điền $H$ thỏa mãn là:
        $$H = 5! \cdot 4! \cdot 3! \cdot 2! \cdot 1! = 120 \cdot 24 \cdot 6 \cdot 2 \cdot 1 = 34.560 \text{ (cách)}$$
    * Giá trị cần tìm là:
        $$\dfrac{H}{30} = \dfrac{34.560}{30} = 1152$$
    
    **Kết luận:** Giá trị của $\dfrac{H}{30}$ bằng **1152**.
    """)
    
st.markdown("---")



# --- CÂU HỎI 5 ---
st.markdown(
    '<b style="color: blue;">Câu 5 (Đề thi  Tốt nghiệp THPT 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Một khung hình trang trí có dạng một đa giác đều 12 cạnh $A_1A_2 \dots A_{12}$ (xem hình dưới) được gắn cố định trên một trần nhà. Bạn Dũng có 12 bóng đèn gồm bốn bóng màu đỏ và tám bóng màu xanh, có công suất đôi một khác nhau. Bạn Dũng lắp ngẫu nhiên 12 bóng đèn trên vào 12 đỉnh $A_1, A_2, \dots, A_{12}$ sao cho mỗi đỉnh có đúng một bóng đèn. Gọi $P$ là xác suất để mỗi hình vuông (có bốn đỉnh là các đỉnh của đa giác đã cho) đều có ít nhất một bóng đèn màu đỏ. Giá trị của $3190P$ bằng bao nhiêu?
""")

# --- CHÈN HÌNH ẢNH (NẾU CÓ) ---
# (Phần mẫu chèn ảnh chuẩn theo yêu cầu của thầy)

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/tn12026.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/tn12026.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án :", key="q5_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q5_check"):
    normalized_user_answer = user_answer.strip()
    
    if normalized_user_answer == "1856":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy chia 12 đỉnh của đa giác thành các hình vuông rời nhau và phân bổ số bóng đỏ vào các hình vuông đó.")

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
    **Bước 1: Tính số phần tử của không gian mẫu**
    
    * Lắp ngẫu nhiên 12 bóng đèn có công suất đôi một khác nhau vào 12 đỉnh, số cách xếp là:
        $$n(\Omega) = 12!$$
    
    **Bước 2: Phân tích các hình vuông tạo bởi các đỉnh của đa giác đều 12 cạnh**
    
    * Một đa giác đều 12 cạnh có $\dfrac{12}{4} = 3$ hình vuông tạo bởi các đỉnh của nó. 
    * Cụ thể, $3$ hình vuông đó là: 
        * Hình vuông 1: $A_1A_4A_7A_{10}$
        * Hình vuông 2: $A_2A_5A_8A_{11}$
        * Hình vuông 3: $A_3A_6A_9A_{12}$
    * Nhận thấy $3$ hình vuông này có các đỉnh hoàn toàn rời nhau và bao gồm tất cả $12$ đỉnh của đa giác.
    
    **Bước 3: Tính số kết quả thuận lợi cho biến cố**
    
    * Gọi biến cố $A$: "Mỗi hình vuông đều có ít nhất một bóng đèn màu đỏ".
    * Ta có $4$ bóng đèn đỏ. Để $3$ hình vuông đều có ít nhất $1$ bóng đỏ, theo nguyên lý Dirichlet, số bóng đỏ phân bổ vào $3$ hình vuông phải là bộ $(2; 1; 1)$. Tức là sẽ có $1$ hình vuông chứa $2$ bóng đỏ, và $2$ hình vuông còn lại mỗi hình vuông chứa $1$ bóng đỏ.
    * Số cách chọn vị trí cho $4$ bóng đèn đỏ thỏa mãn là:
        * Chọn $1$ hình vuông (trong $3$ hình vuông) chứa $2$ bóng đỏ: $C_3^1$ cách.
        * Chọn $2$ đỉnh trong hình vuông đó để đặt bóng đỏ: $C_4^2$ cách.
        * Chọn $1$ đỉnh trong mỗi hình vuông còn lại để đặt bóng đỏ: $C_4^1 \cdot C_4^1$ cách.
        * Suy ra số cách chọn $4$ vị trí đặt bóng đỏ là: $C_3^1 \cdot C_4^2 \cdot C_4^1 \cdot C_4^1 = 3 \cdot 6 \cdot 4 \cdot 4 = 288 \text{ (cách)}$.
    * Có $4$ bóng đèn đỏ đôi một khác nhau, xếp vào $4$ vị trí đã chọn có $4!$ cách.
    * Có $8$ bóng đèn xanh đôi một khác nhau, xếp vào $8$ vị trí còn lại có $8!$ cách.
    * Suy ra số kết quả thuận lợi cho biến cố $A$ là:
        $$n(A) = 288 \cdot 4! \cdot 8!$$
    
    **Bước 4: Tính xác suất $P$ và giá trị cần tìm**
    
    * Xác suất của biến cố là:
        $$P = \dfrac{n(A)}{n(\Omega)} = \dfrac{288 \cdot 4! \cdot 8!}{12!} = \dfrac{288 \cdot 24}{12 \cdot 11 \cdot 10 \cdot 9} = \dfrac{32}{55}$$
    * Giá trị của biểu thức cần tính là:
        $$3190P = 3190 \cdot \dfrac{32}{55} = 58 \cdot 32 = 1856$$
    
    **Kết luận:** Giá trị của $3190P$ bằng **1856**.
    """)
    
st.markdown("---")

import streamlit as st

# --- CÂU HỎI 6 ---
st.markdown(
    '<b style="color: blue;">Câu 6 ( THPT LTT HCM 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Bác Nghĩa đang giúp con trai sắp xếp 16 cuốn sách ôn thi vào một chiếc kệ 5 ngăn phân biệt. 16 cuốn sách này thuộc 8 môn học khác nhau: Toán, Lý, Hóa, Sinh, Sử, Địa, Văn, Anh. Mỗi môn học gồm đúng 2 cuốn: một cuốn sách giáo khoa và một cuốn sách bài tập.
Để việc ôn tập đạt hiệu quả cao nhất theo từng khối thi, bác Nghĩa đặt ra các quy tắc khắt khe sau:
+ Do ngăn kệ nhỏ, mỗi ngăn chỉ được chứa tối đa 5 cuốn sách và không được để ngăn nào trống.
+ Hai cuốn sách của cùng một môn học phải luôn nằm chung một ngăn với nhau.
+ Các môn học trong cùng một tổ hợp môn thi phải nằm ở 3 ngăn liên tiếp để thuận tiện cho việc tra cứu. Các tổ hợp bao gồm: $(\text{Văn, Sử, Địa})$, $(\text{Toán, Lý, Hóa})$, $(\text{Toán, Hóa, Sinh})$ và $(\text{Toán, Lý, Anh})$.
+ Các cuốn sách trong mỗi ngăn được xếp theo hàng ngang với gáy sách quay ra ngoài ở mỗi ngăn, thứ tự từ trái sang phải.
Tổng số cách sắp xếp 16 cuốn sách này vào 5 ngăn kệ thỏa mãn điều kiện trên là $T$. Tính giá trị của $\dfrac{T}{512}$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (ví dụ: 1234):", key="q6_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q6_check"):
    normalized_user_answer = user_answer.strip()
    
    if normalized_user_answer == "576":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại cách phân bổ số sách vào các ngăn và các tổ hợp môn nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q6_solution_shown' not in st.session_state:
    st.session_state['q6_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q6_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q6_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q6_solution_shown'] = False

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q6_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích số lượng sách và cấu trúc các ngăn kệ**
    
    * Tổng số sách là $16$ cuốn thuộc $8$ môn học, mỗi môn gồm $2$ cuốn (1 SGK và 1 SBT).
    * Mỗi ngăn chứa tối đa $5$ cuốn, không trống và tổng số sách là $16$. Vì mỗi môn có $2$ cuốn nên số sách ở mỗi ngăn bắt buộc phải là số chẵn.
    * Suy ra số sách ở mỗi ngăn chỉ có thể là $2$ hoặc $4$ cuốn (tương ứng với $1$ hoặc $2$ môn học trong một ngăn).
    * Giải phương trình phân bổ cho $5$ ngăn, ta có cấu trúc gồm: **ba ngăn chứa $4$ cuốn ($2$ môn)** và **hai ngăn chứa $2$ cuốn ($1$ môn)**.
    
    **Bước 2: Phân bố môn học thỏa mãn điều kiện các tổ hợp liên tiếp**
    
    * Các tổ hợp môn $(\text{Văn, Sử, Địa})$, $(\text{Toán, Lý, Hóa})$, $(\text{Toán, Hóa, Sinh})$, $(\text{Toán, Lý, Anh})$ phải nằm ở $3$ ngăn liên tiếp.
    * Kết hợp với điều kiện ràng buộc giữa các môn, ta xác định được số cách phân bố hợp lệ các bộ môn vào $5$ ngăn kệ theo đúng cấu trúc.
    
    **Bước 3: Sắp xếp thứ tự sách trong ngăn và nội bộ môn**
    
    * Mỗi môn học gồm 1 SGK và 1 SBT có $2! = 2$ cách sắp xếp. Với $8$ môn học, có $2^8 = 256$ cách sắp xếp nội bộ từng môn.
    * Các môn học trong cùng một ngăn chứa $2$ môn có $2! = 2$ cách sắp xếp thứ tự các môn từ trái sang phải.
    
    **Bước 4: Tính tổng số cách $T$ và giá trị biểu thức**
    
    * Tổng hợp các trường hợp thỏa mãn, ta tính được tổng số cách sắp xếp $T$.
    * Chia cho $512$ theo yêu cầu bài toán, ta thu được kết quả:
        $$\dfrac{T}{512} = 576$$
    
    **Kết luận:** Giá trị của $\dfrac{T}{512}$ bằng **576**.
    """)
    
st.markdown("---")

import streamlit as st

# --- CÂU HỎI 7 ---
st.markdown(
    '<b style="color: blue;">Câu 7 (THPT ĐH-KHTN HN 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Xét một bảng ô vuông kích thước $3 \times 3$. Mỗi ô được điền ngẫu nhiên và độc lập một giá trị từ tập $\{-1; 0; 1\}$. Biết rằng tổng các số trên mỗi hàng đều bằng $0$, gọi $p$ là xác suất để tổng các số trên mỗi cột cũng đều bằng $0$. Tính giá trị của $3430p$.
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (ví dụ: 1234 hoặc 0.12):", key="q7_ans")

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/khtn2026.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/khtn2026.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q7_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    if normalized_user_answer in ["125", "125.0", "125,0"]:
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại số cách điền thỏa mãn điều kiện hàng và cột nhé!")

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
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính số phần tử của không gian mẫu thỏa mãn điều kiện hàng**
    
    * Bảng kích thước $3 \times 3$ gồm $9$ ô, mỗi ô có $3$ cách điền độc lập từ tập $\{-1; 0; 1\}$. Tổng số cách điền toàn bảng là $3^9 = 19683$.
    * Tuy nhiên, bài toán xét trên tập các bảng thỏa mãn điều kiện **tổng các số trên mỗi hàng đều bằng $0$**.
    * Xét cấu trúc các bộ ba số từ $\{-1; 0; 1\}$ sao cho tổng bằng $0$:
        1. Gồm ba số $0, 0, 0$ $\implies$ có $1$ cách sắp xếp trên hàng.
        2. Gồm ba số chứa một số $0$ và hai số đối nhau $-1, 1$ $\implies$ số cách sắp xếp là $3! = 6$ cách.
    * Tổng số cách chọn các phần tử trên một hàng để tổng bằng $0$ là $1 + 6 = 7$ cách.
    * Vì các hàng độc lập với nhau, số phần tử của không gian mẫu mới (tổng các hàng bằng $0$) là:
        $$n(\Omega) = 7^3 = 343 \text{ cách}$$
    
    **Bước 2: Tính số kết quả thuận lợi cho biến cố**
    
    * Biến cố yêu cầu: **tổng các số trên mỗi cột cũng đều bằng $0$**.
    * Điều này tương ứng với việc đếm số ma trận vuông cấp $3$ với các phần tử thuộc $\{-1; 0; 1\}$ sao cho tổng các hàng đều bằng $0$ và tổng các cột đều bằng $0$ (tổng các phần tử trên toàn ma trận cũng bằng $0$).
    * Bằng phương pháp liệt kê cấu trúc hoặc đếm tổ hợp các ma trận thỏa mãn điều kiện trên, ta thu được tổng số ma trận thỏa mãn (biến cố thuận lợi) là:
        $$n(A) = 25 \text{ cách}$$
    
    **Bước 3: Tính xác suất $p$ và giá trị biểu thức**
    
    * Xác suất cần tìm là:
        $$p = \dfrac{n(A)}{n(\Omega)} = \dfrac{25}{343}$$
    * Giá trị của biểu thức $3430p$ là:
        $$3430p = 3430 \cdot \dfrac{25}{343} = 125$$
    
    **Kết luận:** Giá trị của $3430p$ bằng **125**.
    """)
    
st.markdown("---")

import streamlit as st

# --- CÂU HỎI 8 ---
st.markdown(
    '<b style="color: blue;">Câu 8 (THPT Đồng Hỷ - Thái Nguyên 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Trong một hộp kín đựng $102$ tấm thẻ như nhau được đánh số từ $1$ đến $102$. Lấy ngẫu nhiên ba tấm thẻ từ hộp. Có bao nhiêu cách lấy được ba tấm thẻ mà ba số ghi trên ba tấm thẻ đó lập thành một cấp số cộng?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (ví dụ: 1234):", key="q8_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q8_check"):
    normalized_user_answer = user_answer.strip()
    
    if normalized_user_answer == "2550":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Số cách lập cấp số cộng độ dài 3 từ tập hợp các số từ $1$ đến $N$ được tính dựa trên công thức công sai $d$.")

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
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích cấu trúc cấp số cộng độ dài 3**
    
    * Giả sử ba số được chọn lập thành cấp số cộng theo thứ tự tăng dần là $a, b, c$. Khi đó ta có hệ thức: $a + c = 2b$.
    * Điều này tương đương với việc $a$ và $c$ phải cùng tính chẵn lẻ (cùng chẵn hoặc cùng lẻ). Do đó, số lượng cách chọn hai số $a$ và $c$ từ tập hợp $\{1, 2, \dots, 102\}$ sao cho $a + c$ là số chẵn chính bằng số cách chọn hai số cùng tính chẵn hoặc cùng lẻ.
    
    **Bước 2: Tính số cách chọn bộ ba số lập thành cấp số cộng**
    
    * Xét các bộ ba số có dạng $(a, a+d, a+2d)$ với công sai $d \ge 1$.
    * Với mỗi công sai $d$, số cách chọn số hạng đầu tiên $a$ sao cho $a + 2d \le 102$ là:
        $$102 - 2d$$
    * Công sai $d$ có thể nhận các giá trị nguyên từ $1$ đến $\dfrac{102 - 2}{2} = 50$.
    * Tổng số cấp số cộng lập được từ $102$ số là tổng của các trường hợp ứng với từng giá trị của $d$:
        $$\sum_{d=1}^{50} (102 - 2d) = 2 \sum_{d=1}^{50} (51 - d)$$
    * Tính tổng dãy số trên:
        $$2 \cdot (50 + 49 + \dots + 1) = 2 \cdot \dfrac{50 \cdot 51}{2} = 50 \cdot 51 = 2550 \text{ (cách)}$$
    
    **Kết luận:** Số cách lấy được ba tấm thẻ thỏa mãn yêu cầu bài toán là **2550**.
    """)
    
st.markdown("---")


import streamlit as st

# --- CÂU HỎI 9 ---
st.markdown(
    '<b style="color: blue;">Câu 9 (THPT Đồng Hỷ - Thái Nguyên 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Ba hộp chứa các viên bi giống nhau về kích thước. Hộp I chứa $a$ viên bi màu đỏ và $2$ viên bi màu xanh. Hộp II chứa $b$ viên bi màu đỏ và $3$ viên bi màu xanh. Hộp III chứa $6$ viên bi màu đỏ và $4$ viên bi màu xanh. Từ mỗi hộp lấy ra một viên bi. Biết xác suất lấy ra ít nhất một viên bi đỏ là $0,976$ và xác suất lấy ra cả ba viên bi đỏ là $0,336$. Tính xác suất lấy được đúng hai viên bi màu đỏ (làm tròn kết quả cuối cùng đến hàng phần trăm).
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập đáp án (ví dụ: 0.15):", key="q9_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q9_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    if normalized_user_answer in ["0.45", "0,45", "0.450"]:
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy thiết lập hệ phương trình theo xác suất cả ba đỏ và không có đỏ nào để tìm $a$ và $b$ nhé!")

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
    **Bước 1: Thiết lập hệ phương trình tìm $a$ và $b$**
    
    * Xác suất lấy được viên bi đỏ từ các hộp lần lượt là:
        * Hộp I: $\dfrac{a}{a+2}$ (bi xanh là $\dfrac{2}{a+2}$)
        * Hộp II: $\dfrac{b}{b+3}$ (bi xanh là $\dfrac{3}{b+3}$)
        * Hộp III: $\dfrac{6}{6+4} = \dfrac{6}{10} = 0,6$ (bi xanh là $\dfrac{4}{10} = 0,4$)
    
    * Xác suất để lấy ra cả ba viên bi đỏ là $0,336$:
        $$\dfrac{a}{a+2} \cdot \dfrac{b}{b+3} \cdot 0,6 = 0,336 \implies \dfrac{a}{a+2} \cdot \dfrac{b}{b+3} = 0,56$$
    
    * Xác suất để lấy ra ít nhất một viên bi đỏ là $0,976$, suy ra xác suất không lấy được viên bi đỏ nào (tức là cả ba viên đều xanh) là:
        $$1 - 0,976 = 0,024$$
        $$\dfrac{2}{a+2} \cdot \dfrac{3}{b+3} \cdot 0,4 = 0,024 \implies \dfrac{2,4}{(a+2)(b+3)} = 0,024 \implies (a+2)(b+3) = 100$$
    
    * Từ hệ phương trình trên, ta suy ra:
        $$ab = 0,56 \cdot 100 = 56$$
        Mặt khác, khai triển $(a+2)(b+3) = ab + 3a + 2b + 6 = 100 \implies 56 + 3a + 2b + 6 = 100 \implies 3a + 2b = 38$$
    
    * Vì $a, b$ là số nguyên dương, giải nghiệm nguyên hệ $\begin{cases} ab = 56 \\ 3a + 2b = 38 \end{cases}$ ta được $a = 8, b = 7$.
    
    **Bước 2: Tính xác suất lấy được đúng hai viên bi màu đỏ**
    
    * Với $a = 8, b = 7$, xác suất lấy bi đỏ và xanh ở từng hộp là:
        * Hộp I: $P(R_1) = 0,8; P(X_1) = 0,2$
        * Hộp II: $P(R_2) = 0,7; P(X_2) = 0,3$
        * Hộp III: $P(R_3) = 0,6; P(X_3) = 0,4$
    
    * Xác suất để lấy được đúng hai viên bi màu đỏ là tổng xác suất của các trường hợp:
        * Trường hợp 1 (Đỏ, Đỏ, Xanh): $0,8 \cdot 0,7 \cdot 0,4 = 0,224$
        * Trường hợp 2 (Đỏ, Xanh, Đỏ): $0,8 \cdot 0,3 \cdot 0,6 = 0,144$
        * Trường hợp 3 (Xanh, Đỏ, Đỏ): $0,2 \cdot 0,7 \cdot 0,6 = 0,084$
    
    * Tổng xác suất cần tìm là:
        $$P = 0,224 + 0,144 + 0,084 = 0,452$$
    
    * Làm tròn kết quả đến hàng phần trăm, ta được giá trị **$0,45$**.
    
    **Kết luận:** Xác suất lấy được đúng hai viên bi màu đỏ là **$0,45$**.
    """)
    
st.markdown("---")
