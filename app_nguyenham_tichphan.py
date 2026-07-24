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
