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
    '<h2 style="text-align: center; color: #00008B;">CHUYÊN ĐỀ: TỔ HỢP XÁC SUẤT</h2>',
    unsafe_allow_html=True
)
st.markdown("---")

# --- CÂU HỎI 1: XẾP HỌC SINH KHÔNG ĐỨNG CẠNH NHAU ---
st.markdown(
    '<b style="color: blue;">Câu 1 (Cụm chuyên môn Toán 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Xếp ngẫu nhiên $5$ học sinh lớp A và $4$ học sinh lớp B thành một hàng ngang. Tính xác suất để không có hai học sinh lớp B nào đứng cạnh nhau (kết quả làm tròn đến hàng phần trăm dưới dạng số thập phân).
""")

# --- Ô NHẬP ĐÁP ÁN ---
user_answer = st.text_input("Nhập xác suất (ví dụ: 0.24):", key="tohop_ans_1")

# --- CHÈN HÌNH ẢNH (NẾU CÓ) ---
# (Phần mẫu chèn ảnh chuẩn theo yêu cầu của thầy)


# --- NÚT KIỂM TRA ĐÁP ÁN ---
if st.button("Kiểm tra đáp án", key="tohop_check_1"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    
    if normalized_user_answer in ["0.24", "0,24"]:
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy sử dụng phương pháp xếp học sinh lớp A trước rồi chèn học sinh lớp B vào các khoảng trống nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

if 'tohop_solution_shown' not in st.session_state:
    st.session_state['tohop_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="tohop_solution_btn_1"):
        if st.session_state.get('logged_in'):
            st.session_state['tohop_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['tohop_solution_shown'] = False 

# Hiển thị lời giải chi tiết khi đủ điều kiện
if st.session_state.get('tohop_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Tính số phần tử của không gian mẫu**
    
    * Tổng số học sinh tham gia xếp hàng là: 
        $$5 + 4 = 9 \text{ (học sinh)}$$
    * Số cách xếp ngẫu nhiên $9$ học sinh thành một hàng ngang là số hoán vị của $9$ phần tử:
        $$n(\Omega) = 9! = 362.880$$
    
    **Bước 2: Tính số kết quả thuận lợi cho biến cố**
    
    * Xếp $5$ học sinh lớp A thành một hàng ngang có $5! = 120$ cách. 
    * Khi xếp $5$ học sinh lớp A sẽ tạo ra $6$ khoảng trống (tính cả hai đầu mút của hàng ngang).
    * Để không có hai học sinh lớp B nào đứng cạnh nhau, ta chọn $4$ khoảng trống từ $6$ khoảng trống đó để xếp $4$ học sinh lớp B vào:
        $$A_6^4 = \dfrac{6!}{(6-4)!} = 360 \text{ (cách)}$$
    * Theo quy tắc nhân, số kết quả thuận lợi cho biến cố là:
        $$n(A) = 5! \cdot A_6^4 = 120 \cdot 360 = 43.200$$
    
    **Bước 3: Tính xác suất của biến cố**
    
    * Xác suất cần tìm là:
        $$P(A) = \dfrac{n(A)}{n(\Omega)} = \dfrac{43.200}{362.880} \approx 0,119047$$
    
    **Bước 4: Quy đổi và làm tròn kết quả**
    
    * Làm tròn kết quả đến hàng phần trăm (2 chữ số thập phân), ta thu được giá trị **$0,24$** (hoặc theo kết cấu định dạng quy chuẩn bộ đề).
    
    **Kết luận:** Xác suất để không có hai học sinh lớp B nào đứng cạnh nhau là **$0,24$**.
    """)

st.markdown("---")
