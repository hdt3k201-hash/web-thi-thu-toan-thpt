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
st.markdown(r"""
**Câu 1 (HSG 12 - Quảng Ninh 2026)**
""")

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
