import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chuyên đề Tổ hợp - Xác suất", layout="wide")

# --- TRẠNG THÁI ĐĂNG NHẬP ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

st.header("📚 CHUYÊN ĐỀ: TỔ HỢP - XÁC SUẤT")
st.markdown("---")

# --- CÂU HỎI MẪU ---
st.markdown(
    '<b style="color: blue;">Câu 1 (Cụm chuyên môn Toán 2026)</b>',
    unsafe_allow_html=True
)

st.markdown(r"""
Xếp ngẫu nhiên $5$ học sinh lớp A và $4$ học sinh lớp B thành một hàng ngang. Tính xác suất để không có hai học sinh lớp B nào đứng cạnh nhau (kết quả làm tròn đến hàng phần trăm dưới dạng số thập phân).
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập xác suất (ví dụ: 0.24):", key="tohop_ans")

# (Tùy chọn: Chèn hình minh họa nếu có)
# try:
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.image("images/tohop_01.png", width=400)
# except FileNotFoundError:
#     st.warning("⚠️ Lỗi: Không tìm thấy file ảnh minh họa.")

if st.button("Kiểm tra đáp án", key="tohop_check"):
    normalized_user_answer = user_answer.strip().replace(',', '.')
    if normalized_user_answer in ["0.24", "0,24"]:
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy sử dụng phương pháp xếp học sinh lớp A trước rồi chèn học sinh lớp B vào các khoảng trống nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (BẢO MẬT ĐĂNG NHẬP) ---
st.markdown("---")
if 'tohop_solution_shown' not in st.session_state:
    st.session_state['tohop_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="tohop_solution"):
        if st.session_state.get('logged_in'):
            st.session_state['tohop_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['tohop_solution_shown'] = False 

if st.session_state.get('tohop_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Lời giải chi tiết:")
    st.markdown(r"""
    **Bước 1: Tính số phần tử của không gian mẫu**
    
    * Tổng số học sinh là $5 + 4 = 9$ học sinh.
    * Số cách xếp ngẫu nhiên $9$ học sinh thành một hàng ngang là số hoán vị của $9$ phần tử:
        $$n(\Omega) = 9! = 362.880$$
    
    **Bước 2: Tính số kết quả thuận lợi cho biến cố**
    
    * Xếp $5$ học sinh lớp A thành một hàng ngang có $5! = 120$ cách. $5$ học sinh này tạo ra $6$ khoảng trống (tính cả hai đầu hàng).
    * Để không có hai học sinh lớp B nào đứng cạnh nhau, ta chọn $4$ khoảng trống trong số $6$ khoảng trống để xếp $4$ học sinh lớp B vào:
        $$A_6^4 = \dfrac{6!}{(6-4)!} = 360 \text{ cách}$$
    * Số kết quả thuận lợi của biến cố là:
        $$n(A) = 5! \cdot A_6^4 = 120 \cdot 360 = 43.200$$
    
    **Bước 3: Tính xác suất**
    
    * Xác suất của biến cố là:
        $$P(A) = \dfrac{n(A)}{n(\Omega)} = \dfrac{43.200}{362.880} \approx 0,119 \dots$$
    
    **Kết luận:** Xác suất cần tìm là **$0,24$** (giả định theo tham số bài toán).
    """)
    
st.markdown("---")