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
    '<h2 style="text-align: center; color: blue;">CHUYÊN ĐỀ: NGUYÊN HÀM TÍCH PHÂN</h2>',
    unsafe_allow_html=True
)
st.markdown("---")


# --- CÂU HỎI 1: THỂ TÍCH KHỐI ĐA DIỆN VÀ KHỐI TRÒN XOAY ---
st.markdown(
    '<b style="color: blue;">Câu 1 (Đề thi Tốt Nghiệp THPT 2025)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Để đặt một vật trang trí trên mặt bàn, người ta thiết kế một chân đế như sau. Lấy một khối gỗ có dạng khối chóp cụt tứ giác đều với độ dài hai cạnh đáy lần lượt bằng $7,4\text{ cm}$ và $10,4\text{ cm}$, bề dày của khối gỗ bằng $1,5\text{ cm}$. Sau đó khoét bỏ một phần của khối gỗ sao cho phần đó có dạng vật thể $H$, ở đó $H$ nhận được bằng cách cắt khối cầu bán kính $5,5\text{ cm}$ bởi một mặt phẳng cắt mà mặt cắt là hình tròn có bán kính $3,5\text{ cm}$ (xem hình dưới).

Thể tích của khối chân đế bằng bao nhiêu centimét khối (không làm tròn kết quả các phép tính trung gian, chỉ làm tròn kết quả cuối cùng đến hàng phần mười)?
""")
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/tp_2026.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/tp_2026.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer = st.text_input("Nhập thể tích khối chân đế (làm tròn đến hàng phần mười, ví dụ: 12.3):", key="q1_ans")

# --- CHÈN HÌNH ẢNH ---


# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q1_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    # Đáp án chính xác là 94.7
    if normalized_user_answer == "94.7":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy tính thể tích khối chóp cụt ban đầu, sau đó trừ đi thể tích của phần chỏm cầu bị khoét (có thể dùng tích phân để tính thể tích chỏm cầu nhé)!")

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
    **Bước 1: Tính thể tích khối chóp cụt tứ giác đều (khối gỗ ban đầu)**
    
    * Khối chóp cụt có đáy lớn là hình vuông cạnh $a = 10,4\text{ cm}$, đáy nhỏ là hình vuông cạnh $b = 7,4\text{ cm}$ và chiều cao $h_1 = 1,5\text{ cm}$.
    * Diện tích đáy lớn: $S_1 = 10,4^2 = 108,16\text{ (cm}^2\text{)}$
    * Diện tích đáy nhỏ: $S_2 = 7,4^2 = 54,76\text{ (cm}^2\text{)}$
    * Thể tích khối gỗ ban đầu là:
        $$V_1 = \dfrac{1}{3}h_1(S_1 + \sqrt{S_1 S_2} + S_2) = \dfrac{1}{3} \cdot 1,5 \cdot (108,16 + 10,4 \cdot 7,4 + 54,76) = 119,94 \text{ (cm}^3\text{)}$$
    
    **Bước 2: Tính thể tích phần khoét đi (chỏm cầu $H$)**
    
    * Khối cầu có bán kính $R = 5,5\text{ cm}$. Mặt cắt là hình tròn có bán kính $r = 3,5\text{ cm}$.
    * Khoảng cách từ tâm khối cầu đến mặt phẳng cắt là:
        $$d = \sqrt{R^2 - r^2} = \sqrt{5,5^2 - 3,5^2} = \sqrt{18} = 3\sqrt{2} \text{ (cm)}$$
    * Thể tích chỏm cầu $H$ được tính bằng ứng dụng tích phân (như hệ trục tọa độ đã cho trên hình, quay hình phẳng giới hạn bởi đường tròn $x^2 + y^2 = 5,5^2$ quanh trục $Ox$ từ mặt cắt $x = 3\sqrt{2}$ đến $x = 5,5$):
        $$V_2 = \pi \int_{3\sqrt{2}}^{5,5} (5,5^2 - x^2) \text{d}x = \pi \left[ 30,25x - \dfrac{x^3}{3} \right]_{3\sqrt{2}}^{5,5}$$
        $$V_2 = \pi \left( \dfrac{332,75 - 218,25\sqrt{2}}{3} \right) \approx 25,236 \text{ (cm}^3\text{)}$$
    *(Lưu ý: Cũng có thể dùng công thức thể tích chỏm cầu $V_2 = \pi h_2^2 \left(R - \dfrac{h_2}{3}\right)$ với chiều cao chỏm cầu $h_2 = 5,5 - 3\sqrt{2}$)*
    
    **Bước 3: Tính thể tích khối chân đế**
    
    * Thể tích của khối chân đế là phần còn lại sau khi khoét:
        $$V = V_1 - V_2 = 119,94 - \pi \left( \dfrac{332,75 - 218,25\sqrt{2}}{3} \right) \approx 94,704 \text{ (cm}^3\text{)}$$
    * Làm tròn kết quả cuối cùng đến hàng phần mười, ta được $94,7$.
        
    **Kết luận:** Thể tích của khối chân đế xấp xỉ **$94,7\text{ cm}^3$**.
    """)

st.markdown("---")


# --- CÂU HỎI 2: ỨNG DỤNG TÍCH PHÂN TÍNH DIỆN TÍCH ---
st.markdown(
    '<b style="color: blue;">Câu 2 (Đề minh họa 2025)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Kiến trúc sư thiết kế một khu sinh hoạt cộng đồng có dạng hình chữ nhật với chiều rộng và chiều dài lần lượt là $60\text{m}$ và $80\text{m}$. Trong đó, phần được tô màu đậm là sân chơi, phần còn lại để trồng hoa. Mỗi phần trồng hoa có đường biên cong là một phần của parabol với đỉnh thuộc một trục đối xứng của hình chữ nhật và khoảng cách từ đỉnh đó đến trung điểm cạnh tương ứng của hình chữ nhật bằng $20\text{m}$ (xem hình minh họa).

Diện tích của phần sân chơi là bao nhiêu mét vuông?
""")

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Đường dẫn ảnh đã được đồng bộ
        st.image("images/mh_2026.PNG", width=400)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/mh_2026.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer = st.text_input("Nhập diện tích phần sân chơi (ví dụ: 1234):", key="q2_ans")

# --- CHÈN HÌNH ẢNH ---

# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q2_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    # Đáp án chính xác là 3200
    if normalized_user_answer == "3200":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hãy tính tổng diện tích hình chữ nhật rồi trừ đi diện tích của 2 phần parabol trồng hoa. Bạn có thể gắn trục tọa độ để dùng tích phân hoặc dùng công thức diện tích hình phẳng giới hạn bởi parabol nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q2_solution_shown' not in st.session_state:
    st.session_state['q2_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q2_solution_btn"):
        if st.session_state.get('logged_in'):
            st.session_state['q2_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q2_solution_shown'] = False 

# Hiển thị lời giải chi tiết khi đủ điều kiện
if st.session_state.get('q2_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính diện tích toàn bộ khu đất hình chữ nhật**
    
    * Hình chữ nhật có chiều rộng $60\text{ m}$ và chiều dài (cao) $80\text{ m}$.
    * Diện tích tổng thể của khu đất là:
        $$S_{\text{hcn}} = 60 \times 80 = 4800 \text{ (m}^2\text{)}$$
    
    **Bước 2: Tính diện tích phần đất trồng hoa (2 phần giới hạn bởi parabol)**
    
    * Chọn hệ trục tọa độ $Oxy$ sao cho gốc $O$ trùng với trung điểm cạnh đáy dưới của hình chữ nhật, trục $Ox$ nằm dọc theo cạnh đáy dưới, trục $Oy$ là trục đối xứng dọc của hình chữ nhật.
    * Khi đó, parabol bên dưới có đỉnh $I(0; 20)$ và đi qua 2 điểm thuộc đáy hình chữ nhật là $A(-30; 0)$ và $B(30; 0)$.
    * Phương trình parabol có dạng $y = ax^2 + c$. Vì đỉnh là $I(0; 20)$ nên $c = 20 \Rightarrow y = ax^2 + 20$.
    * Parabol đi qua $B(30; 0)$ nên:
        $$0 = a(30)^2 + 20 \Rightarrow 900a = -20 \Rightarrow a = -\dfrac{1}{45}$$
    * Vậy phương trình parabol bên dưới là: $y = -\dfrac{1}{45}x^2 + 20$.
    * Diện tích một phần trồng hoa bên dưới là diện tích hình phẳng giới hạn bởi parabol và trục hoành:
        $$S_1 = \int_{-30}^{30} \left( -\dfrac{1}{45}x^2 + 20 \right) \text{d}x = \left[ -\dfrac{x^3}{135} + 20x \right]_{-30}^{30} = 800 \text{ (m}^2\text{)}$$
        *(Mẹo nhanh: Diện tích hình phẳng giới hạn bởi parabol và dây cung vuông góc với trục đối xứng được tính nhanh bằng công thức $S = \dfrac{2}{3} \cdot \text{đáy} \cdot \text{chiều cao} = \dfrac{2}{3} \cdot 60 \cdot 20 = 800 \text{ m}^2$)*
    * Do tính đối xứng, phần trồng hoa bên trên cũng có diện tích bằng phần bên dưới. Tổng diện tích phần trồng hoa là:
        $$S_{\text{hoa}} = 2 \times 800 = 1600 \text{ (m}^2\text{)}$$
    
    **Bước 3: Tính diện tích phần sân chơi**
    
    * Phần diện tích sân chơi bằng diện tích tổng thể trừ đi diện tích trồng hoa:
        $$S_{\text{sân chơi}} = S_{\text{hcn}} - S_{\text{hoa}} = 4800 - 1600 = 3200 \text{ (m}^2\text{)}$$
        
    **Kết luận:** Diện tích của phần sân chơi là **$3200\text{ m}^2$**.
    """)

st.markdown("---")


# --- CÂU HỎI 3: ỨNG DỤNG TÍCH PHÂN TÍNH THỂ TÍCH KHỐI TRÒN XOAY ---
st.markdown(
    '<b style="color: blue;">Câu 3 (Đề thi tốt nghiệp THPT 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
**Câu 2.** Để chế tác một hạt cườm, người ta lấy một khối vật thể có dạng một khối tròn xoay được tạo thành khi quay hình phẳng giới hạn bởi trục $Ox$ và nửa trên của elip $\dfrac{x^2}{1,5^2} + \dfrac{y^2}{1^2} = 1$ (một đơn vị dài trên mỗi trục tọa độ tương ứng với một xăng-ti-mét trong thực tế) quanh trục $Ox$; sau đó khoan dọc theo trục xoay (xem hình dưới). Lỗ khoan có dạng hình trụ với bán kính 0,2 cm và có trục nằm trên trục xoay. Phần còn lại sau khi khoan là hạt cườm, có dạng một khối tròn xoay.

Thể tích của hạt cườm đó bằng bao nhiêu xăng-ti-mét khối *(không làm tròn kết quả các phép tính trung gian, chỉ làm tròn kết quả cuối cùng đến hàng phần trăm)*?
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer = st.text_input("Nhập thể tích hạt cườm (làm tròn đến hàng phần trăm, ví dụ: 12.34):", key="q3_ans")

# --- CHÈN HÌNH ẢNH ---
try:
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # Sử dụng đúng tên file ảnh bạn đã cung cấp
        st.image("images/image_d7032f.PNG", width=600)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/image_d7032f.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q3_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    # Đáp án chính xác là 5.91
    if normalized_user_answer == "5.91":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Hạt cườm là khối tròn xoay tạo bởi hình phẳng giới hạn giữa đường elip và đường thẳng y = 0,2 quay quanh trục Ox. Hãy tìm hoành độ giao điểm để xác định cận tích phân nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q3_solution_shown' not in st.session_state:
    st.session_state['q3_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q3_solution_btn"):
        if st.session_state.get('logged_in'):
            st.session_state['q3_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q3_solution_shown'] = False 

# Hiển thị lời giải chi tiết khi đủ điều kiện
if st.session_state.get('q3_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Xác định phương trình đường cong và cận tích phân**
    
    * Phương trình của elip là $\dfrac{x^2}{1,5^2} + \dfrac{y^2}{1^2} = 1$. Suy ra nửa trên của elip có phương trình:
        $$y = \sqrt{1 - \dfrac{x^2}{2,25}}$$
    * Lỗ khoan hình trụ dọc theo trục $Ox$ có bán kính $r = 0,2$ cm. Mặt cắt ngang của mép lỗ khoan là đường thẳng $y = 0,2$.
    * Tìm hoành độ giao điểm của elip và đường thẳng $y = 0,2$:
        $$\sqrt{1 - \dfrac{x^2}{2,25}} = 0,2 \Rightarrow 1 - \dfrac{x^2}{2,25} = 0,04 \Rightarrow \dfrac{x^2}{2,25} = 0,96$$
        $$\Rightarrow x^2 = 2,16 \Rightarrow x = \pm\sqrt{2,16}$$
        
    **Bước 2: Thiết lập công thức tính thể tích**
    
    * Thể tích hạt cườm ($V$) chính là thể tích khối tròn xoay được sinh ra khi quay hình phẳng giới hạn bởi đồ thị $y = \sqrt{1 - \dfrac{x^2}{2,25}}$, đường thẳng $y = 0,2$ và hai đường thẳng $x = -\sqrt{2,16}, x = \sqrt{2,16}$ xung quanh trục $Ox$.
    * Công thức tính thể tích:
        $$V = \pi \int_{-\sqrt{2,16}}^{\sqrt{2,16}} \left[ \left(\sqrt{1 - \dfrac{x^2}{2,25}}\right)^2 - 0,2^2 \right] \text{d}x$$
        $$V = \pi \int_{-\sqrt{2,16}}^{\sqrt{2,16}} \left( 1 - \dfrac{x^2}{2,25} - 0,04 \right) \text{d}x = \pi \int_{-\sqrt{2,16}}^{\sqrt{2,16}} \left( 0,96 - \dfrac{x^2}{2,25} \right) \text{d}x$$
    
    **Bước 3: Tính toán kết quả tích phân**
    
    * Do hàm số chẵn, ta có thể tính:
        $$V = 2\pi \int_{0}^{\sqrt{2,16}} \left( 0,96 - \dfrac{x^2}{2,25} \right) \text{d}x$$
        $$V = 2\pi \left[ 0,96x - \dfrac{x^3}{3 \cdot 2,25} \right]_{0}^{\sqrt{2,16}} = 2\pi \left[ 0,96x - \dfrac{x^3}{6,75} \right]_{0}^{\sqrt{2,16}}$$
    * Thay cận $x = \sqrt{2,16}$ vào (lưu ý $x^3 = 2,16\sqrt{2,16}$):
        $$V = 2\pi \left( 0,96\sqrt{2,16} - \dfrac{2,16\sqrt{2,16}}{6,75} \right)$$
        $$V = 2\pi \left( 0,96\sqrt{2,16} - 0,32\sqrt{2,16} \right) = 2\pi \left( 0,64\sqrt{2,16} \right) = 1,28\pi\sqrt{2,16}$$
    * Bấm máy tính giá trị xấp xỉ:
        $$V \approx 5,91035 \text{ (cm}^3\text{)}$$
    * Làm tròn kết quả đến hàng phần trăm theo yêu cầu đề bài, ta được 5,91.
        
    **Kết luận:** Thể tích của hạt cườm là **5,91 cm³**.
    """)

st.markdown("---")

# --- CÂU HỎI 4: ỨNG DỤNG TÍCH PHÂN TÍNH THỂ TÍCH ---
st.markdown(
    '<b style="color: blue;">Câu 4 (THPT Thường Xuân 2 - Thanh Hóa 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Ông A dự định xây “tường cong” trong sân trượt patin là một khối bê tông có chiều cao từ mặt đất lên là 3,5 m. Giao của mặt tường cong và mặt đất là đoạn thẳng $AB = 4\text{ m}$. Thiết diện của khối tường cong cắt bởi mặt phẳng vuông góc với $AB$ tại $A$ là một hình tam giác vuông cong $ACE$ với $AC = 4\text{ m}$, $CE = 3,5\text{ m}$ và cạnh cong $AE$ nằm trên một đường parabol có trục đối xứng vuông góc với mặt đất. Tại vị trí $M$ là trung điểm của $AC$ thì tường cong có độ cao 1 m (xem hình minh họa bên). 

Tính thể tích bê tông cần sử dụng để tạo nên khối tường cong đó.
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer = st.text_input("Nhập thể tích khối bê tông (ví dụ: 12.5):", key="q4_ans")

# --- CHÈN HÌNH ẢNH ---
try:
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # Sử dụng đúng tên file ảnh bạn đã cung cấp
        st.image("images/image_d7113c.PNG", width=600)
except FileNotFoundError:
    # Thông báo lỗi cập nhật đúng tên file
    st.warning("⚠️ Lỗi: Không tìm thấy file ảnh 'images/image_d7113c.PNG'. Vui lòng kiểm tra lại đường dẫn.")

# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="q4_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    # Đáp án chính xác là 20
    if normalized_user_answer == "20":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Gợi ý: Khối tường cong này thực chất là một hình lăng trụ có đáy là tam giác vuông cong ACE. Hãy gắn hệ trục tọa độ để tìm phương trình parabol và dùng tích phân tính diện tích mặt đáy nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'q4_solution_shown' not in st.session_state:
    st.session_state['q4_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q4_solution_btn"):
        if st.session_state.get('logged_in'):
            st.session_state['q4_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q4_solution_shown'] = False 

# Hiển thị lời giải chi tiết khi đủ điều kiện
if st.session_state.get('q4_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích hình học của khối tường cong**
    
    * Khối bê tông có dạng một hình lăng trụ (tổng quát) với đường sinh vuông góc với mặt đáy. 
    * Mặt đáy ở đây chính là thiết diện tam giác vuông cong $ACE$. Chiều cao (hoặc chiều dài) của khối lăng trụ này là đoạn thẳng $AB = 4\text{ m}$.
    * Thể tích khối tường cong được tính bằng công thức: $V = S_{ACE} \cdot AB$.
    
    **Bước 2: Gắn hệ trục tọa độ và tìm phương trình parabol $AE$**
    
    * Chọn hệ trục tọa độ $Oxy$ sao cho gốc tọa độ $O$ trùng với điểm $A(0; 0)$. Tia $Ox$ chứa đoạn thẳng $AC$, tia $Oy$ hướng thẳng đứng lên trên.
    * Khi đó, các điểm có tọa độ như sau:
        * $A(0; 0)$
        * Vì $AC = 4\text{ m}$ nên $C(4; 0)$.
        * $CE \perp AC$ và $CE = 3,5\text{ m}$ nên $E(4; 3,5)$.
        * $M$ là trung điểm $AC$ nên $M(2; 0)$. Tại $M$ tường cao $1\text{ m}$, tức là đồ thị đi qua điểm $N(2; 1)$.
    * Cạnh cong $AE$ nằm trên parabol có trục đối xứng vuông góc với mặt đất (tức là song song hoặc trùng với trục $Oy$), nên phương trình có dạng: $y = ax^2 + bx + c \quad (a \neq 0)$.
    * Thay tọa độ các điểm $A, N, E$ vào phương trình, ta có hệ:
        $$\begin{cases} c = 0 \\ a(2)^2 + b(2) + c = 1 \\ a(4)^2 + b(4) + c = 3,5 \end{cases} \Leftrightarrow \begin{cases} c = 0 \\ 4a + 2b = 1 \\ 16a + 4b = 3,5 \end{cases}$$
    * Giải hệ phương trình trên:
        Nhân phương trình thứ hai với $2$: $8a + 4b = 2$. Lấy phương trình thứ ba trừ đi phương trình này: 
        $16a - 8a = 3,5 - 2 \Rightarrow 8a = 1,5 \Rightarrow a = \dfrac{1,5}{8} = \dfrac{3}{16}$.
        Từ đó, $2b = 1 - 4 \cdot \dfrac{3}{16} = 1 - \dfrac{3}{4} = \dfrac{1}{4} \Rightarrow b = \dfrac{1}{8}$.
    * Vậy phương trình của parabol là: $y = \dfrac{3}{16}x^2 + \dfrac{1}{8}x$.
    
    **Bước 3: Tính diện tích tam giác vuông cong $ACE$**
    
    * Diện tích mặt cong $S_{ACE}$ chính là diện tích hình phẳng giới hạn bởi đường parabol $y = \dfrac{3}{16}x^2 + \dfrac{1}{8}x$, trục hoành $y = 0$ và hai đường thẳng $x = 0, x = 4$.
    * Áp dụng công thức tích phân:
        $$S_{ACE} = \int_{0}^{4} \left( \dfrac{3}{16}x^2 + \dfrac{1}{8}x \right) \text{d}x = \left[ \dfrac{3}{16} \cdot \dfrac{x^3}{3} + \dfrac{1}{8} \cdot \dfrac{x^2}{2} \right]_{0}^{4} = \left[ \dfrac{x^3}{16} + \dfrac{x^2}{16} \right]_{0}^{4}$$
        $$S_{ACE} = \dfrac{4^3}{16} + \dfrac{4^2}{16} - 0 = \dfrac{64}{16} + \dfrac{16}{16} = 4 + 1 = 5 \text{ (m}^2\text{)}$$
    
    **Bước 4: Tính thể tích khối bê tông**
    
    * Thể tích của khối bê tông là:
        $$V = S_{ACE} \cdot AB = 5 \cdot 4 = 20 \text{ (m}^3\text{)}$$
        
    **Kết luận:** Thể tích bê tông cần sử dụng để tạo nên khối tường cong là **20 m³**.
    """)

st.markdown("---")
