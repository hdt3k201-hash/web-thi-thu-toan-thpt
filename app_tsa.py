import streamlit as st
import time
from datetime import datetime, timedelta

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ Thống Thi Thử TSA Bách Khoa",
    page_icon="🦅",
    layout="wide"
)

# 2. GIAO DIỆN KHUNG VIỀN ĐỎ TRỰC QUAN (CUSTOM CSS)
st.markdown("""
<style>
    /* Header chính */
    /* Header chính - Đã thu nhỏ khung và cỡ chữ */
    .tsa-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        color: white;
        padding: 12px 15px !important; /* Giảm lề trong để khung mỏng hơn */
        border-radius: 8px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 3px 6px rgba(183, 28, 28, 0.25);
    }
    
    /* Chỉnh cỡ chữ tiêu đề lớn */
    .tsa-header h1 {
        font-size: 1.4rem !important; /* Giảm từ ~2.0rem xuống 1.4rem */
        font-weight: 700 !important;
        margin: 0 !important; /* Xóa khoảng trống thừa trên dưới */
        padding-bottom: 4px !important;
        color: white !important;
        line-height: 1.3 !important;
    }
    
    /* Chỉnh cỡ chữ chuyên đề phụ */
    .tsa-header h3 {
        font-size: 1.0rem !important; /* Giảm xuống 1.0rem vừa vặn */
        font-weight: 500 !important;
        margin: 0 !important; /* Xóa khoảng trống thừa */
        color: #ffcdd2 !important; /* Màu hồng nhạt giúp dịu mắt hơn */
    }
    
    /* Áp dụng viền đỏ trực tiếp cho các Container của Streamlit */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #d32f2f !important;
        border-radius: 10px !important;
        background-color: #fffbfb !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important;
    }
    
    /* Tiêu đề câu hỏi */
    .question-title {
        color: #b71c1c;
        font-weight: bold;
        font-size: 1.15em;
        margin-bottom: 12px;
        border-bottom: 1.5px dashed #ef9a9a;
        padding-bottom: 8px;
    }
    
    /* Nhãn loại câu hỏi */
    .tag-badge {
        background-color: #ffebee;
        color: #c62828;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85em;
        font-weight: bold;
        border: 1px solid #ef9a9a;
        margin-right: 8px;
    }
    
    /* Khung đồng hồ đếm ngược */
    .timer-container {
        background-color: #b71c1c;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. KHỞI TẠO SESSION STATE
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# 4. THANH BÊN (SIDEBAR): CHỌN ĐỀ THI & ĐỒNG HỒ ĐẾM NGƯỢC

import streamlit.components.v1 as components # Sử dụng module chuẩn để chạy JS

# 4. THANH BÊN (SIDEBAR): CHỌN ĐỀ THI & ĐỒNG HỒ ĐẾM NGƯỢC
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Logo_HUST.png/1200px-Logo_HUST.png", width=120)
st.sidebar.title("THI THỬ TSA ONLINE")

# Danh sách đề thi
selected_exam = st.sidebar.selectbox(
    "📋 Chọn Đề Thi TSA:",
    [
        "Đề TSA số 01: Chuyên đề Lượng giác & Dao động",
        "Đề TSA số 02: Hàm số & Mô hình Toán thực tế",
        "Đề TSA số 03: Xác suất & Phân tích số liệu"
    ]
)

st.sidebar.markdown("---")

# --- ĐỒNG HỒ ĐẾM NGƯỢC DÙNG COMPONENTS (CHẠY JS MƯỢT MÀ KHÔNG BỊ CHẶN) ---
EXAM_DURATION_MINUTES = 60

# 1. Tính mốc thời gian KẾT THÚC (End Time) cố định
if "end_time_tsa" not in st.session_state:
    st.session_state.end_time_tsa = time.time() + (EXAM_DURATION_MINUTES * 60)

# 2. Tính thời gian còn lại ngay tại thời điểm load trang
remaining_sec = max(0, int(st.session_state.end_time_tsa - time.time()))
init_mins, init_secs = divmod(remaining_sec, 60)
init_time_str = f"{init_mins:02d}:{init_secs:02d}"

# Chuyển đổi sang mili giây cho JS
end_timestamp_ms = int(st.session_state.end_time_tsa * 1000)

# 3. Đưa vào giao diện nhúng Component (Tạo khung iframe cách ly để JS tự do chạy)
with st.sidebar:
    components.html(f"""
    <div style="background-color: #b71c1c; color: white; padding: 12px; border-radius: 10px; text-align: center; font-family: 'Source Sans Pro', sans-serif; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin: 2px;">
        <div style="font-size: 15px; font-weight: bold; margin-bottom: 4px;">⏱️ Thời gian còn lại:</div>
        <div id="tsa-countdown" style="font-size: 26px; font-weight: bold; letter-spacing: 2px;">{init_time_str}</div>
    </div>

    <script>
    (function() {{
        const targetTime = {end_timestamp_ms};
        const timerElement = document.getElementById("tsa-countdown");

        function updateClock() {{
            if (!timerElement) return;
            
            const now = new Date().getTime();
            const remainingMs = targetTime - now;

            if (remainingMs <= 0) {{
                timerElement.innerHTML = "00:00";
                timerElement.style.color = "#ffcdd2";
                return;
            }}

            const totalSeconds = Math.floor(remainingMs / 1000);
            const m = Math.floor(totalSeconds / 60);
            const s = totalSeconds % 60;

            const formattedM = m < 10 ? "0" + m : m;
            const formattedS = s < 10 ? "0" + s : s;

            timerElement.innerHTML = formattedM + ":" + formattedS;
        }}

        // Cập nhật mỗi giây
        setInterval(updateClock, 1000);
    }})();
    </script>
    """, height=100)

# Nút Làm lại bài thi: Đặt lại mốc thời gian và trạng thái
if st.sidebar.button("🔄 Làm lại bài thi", type="secondary"):
    st.session_state.end_time_tsa = time.time() + (EXAM_DURATION_MINUTES * 60)
    st.session_state.exam_submitted = False
    st.rerun()

# 5. TIÊU ĐỀ CHÍNH BÀI THI
st.markdown("""
<div class="tsa-header">
    <h1>KỲ THI ĐÁNH GIÁ TƯ DUY (TSA) - ĐẠI HỌC BÁCH KHOA HÀ NỘI</h1>
    <h3>CHUYÊN ĐỀ: LƯỢNG GIÁC & MÔ HÌNH TOÁN HỌC</h3>
</div>
""", unsafe_allow_html=True)

# 6. GIAO DIỆN LÀM BÀI / CHẤM ĐIỂM
if not st.session_state.exam_submitted:
    with st.form("tsa_exam_form"):
        


            # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # CÂU HỎI KÉO THẢ / CHỌN PHƯƠNG ÁN CÓ KHUNG TỔNG HỢP ĐÁP ÁN
        # ---------------------------------------------------------------------
        with st.container(border=True):
           #### Câu 1: [Kéo thả phương án]
Một vòng quay Mặt Trời (Ferris wheel) có bán kính $50\text{ m}$. Tâm của vòng quay nằm ở độ cao $60\text{ m}$ so với mặt đất. Vòng quay quay đều, mất $15$ phút để hoàn thành một vòng. Giả sử tại thời điểm $t=0$ (phút), một cabin bắt đầu chuyển động từ vị trí thấp nhất của vòng quay. Độ cao của cabin so với mặt đất theo thời gian $t$ được mô hình hóa bởi hàm số:
$$h(t) = A\cos(\omega t) + B \quad (A < 0)$$

*Các phương án lựa chọn:* `-50`, `50`, `60`, `2π/15`, `15/2π`, `85`, `5`, `10`.

1. Hàm số mô phỏng độ cao có các thông số là: $A =$ `[ (1) ]`, $\omega =$ `[ (2) ]`, $B =$ `[ (3) ]`.
2. Thời điểm đầu tiên cabin đạt độ cao $85\text{ m}$ là vào phút thứ `[ (4) ]`.

---

#### Câu 2: [Trắc nghiệm 4 lựa chọn]
Cho hàm số lượng giác $y = a\sin(bx+c) + d$ có đồ thị đạt giá trị lớn nhất $y_{\max} = 4$, giá trị nhỏ nhất $y_{\min} = -2$, chu kỳ $T = \pi$. Biết $a > 0$, $b > 0$ và $c \in (-\pi; 0)$. Tính giá trị của biểu thức $P = a + b + c + d$.

* **A.** $P = 6 - \dfrac{\pi}{3}$
* **B.** $P = 4 + \dfrac{\pi}{3}$
* **C.** $P = 5 - \dfrac{\pi}{6}$
* **D.** $P = 3 + \dfrac{\pi}{2}$

---

#### Câu 3: [Trả lời ngắn]
Tính tổng tất cả các nghiệm của phương trình $\sin^2 x - \cos x = 1$ trên đoạn $[0; 2\pi]$.

---

#### Câu 4: [Đúng/Sai]
Cho phương trình lượng giác: $2\cos^2 x - (2m+1)\cos x + m = 0 \quad (1)$. Xét tính đúng/sai của các phát biểu sau:

* **a)** Phương trình (1) có thể phân tích thành nhân tử dạng $(\cos x - m)(2\cos x - 1) = 0$.
* **b)** Khi $m = 1$, phương trình có đúng 2 nghiệm phân biệt trên đoạn $[0; 2\pi]$.
* **c)** Để phương trình có đúng 3 nghiệm phân biệt trên đoạn $[0; 2\pi]$ thì $m = -1$.
* **d)** Có tồn tại giá trị thực của $m$ để phương trình đã cho hoàn toàn vô nghiệm.

---

#### Câu 5: [Trả lời ngắn]
Mực nước tại một cảng biển được mô hình hóa bởi hàm số $h(t) = 3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12$ (mét), trong đó $t$ là thời gian tính bằng giờ ($0 \le t \le 24$). Một tàu hàng yêu cầu mực nước tối thiểu là $13,5\text{ m}$ để cập cảng an toàn. Trong một ngày ($24$ giờ), tổng thời gian tàu có thể cập cảng an toàn là bao nhiêu giờ?

---

#### Câu 6: [Trả lời ngắn]
Tìm giá trị nhỏ nhất của hàm số $y = 3\sin x + 4\cos x + 5$.

---

#### Câu 7: [Đúng/Sai]
Một con lắc lò xo dao động điều hòa với phương trình li độ $x(t) = 5\cos\left(4\pi t - \dfrac{\pi}{2}\right)\text{ (cm)}$. Vận tốc của vật là $v(t) = x'(t)$. Xét tính đúng/sai của các mệnh đề sau:

* **a)** Chu kỳ dao động toàn phần của con lắc lò xo là $T = 0,5\text{ s}$.
* **b)** Tại thời điểm ban đầu $t=0$, vật chuyển động qua vị trí cân bằng theo chiều âm.
* **c)** Vận tốc đạt giá trị lớn nhất của vật trong suốt quá trình dao động là $20\pi\text{ cm/s}$.
* **d)** Thời gian ngắn nhất để vật di chuyển từ vị trí cân bằng ra đến biên dương cực đại là $0,25\text{ s}$.

---

#### Câu 8: [Trắc nghiệm 4 lựa chọn]
Có bao nhiêu giá trị nguyên của tham số $m \in [-10; 10]$ để phương trình $\tan x + \cot x = m$ có nghiệm thực?

* **A.** 18
* **B.** 21
* **C.** 17
* **D.** 19

---

#### Câu 9: [Trả lời ngắn]
Nồng độ bụi mịn PM2.5 ngoài trời tại một thành phố trong ngày được mô hình hóa bởi hàm số $C(t) = 20\sin\left(\dfrac{\pi}{12}(t-6)\right) + 40$ ($\mu\text{g/m}^3$), $0 \le t \le 24$. Khuyến cáo sức khỏe quy định không nên ra ngoài khi nồng độ vượt mức $50\mu\text{g/m}^3$. Trong một ngày, khoảng thời gian không an toàn kéo dài liên tục bao nhiêu tiếng?

---

#### Câu 10: [Kéo thả phương án]
Cho biểu thức lượng giác $P = \sin\left(x + \dfrac{\pi}{6}\right)\cos\left(x - \dfrac{\pi}{6}\right)$.
1. Rút gọn hoàn toàn biểu thức $P$, ta thu được kết quả: $P =$ `[ (1) ]`
2. Giá trị lớn nhất có thể đạt được của biểu thức $P$ là: $P_{\max} =$ `[ (2) ]`

---

#### Câu 11: [Trả lời ngắn]
Đếm số lượng các nghiệm nguyên $x$ thuộc đoạn $[1; 2026]$ thỏa mãn phương trình lượng giác: $\cos\left(\dfrac{\pi x}{3}\right) = \dfrac{1}{2}$.

---

#### Câu 12: [Đúng/Sai]
Cho phương trình lượng giác: $(2\cos x + 1)(\cos x - m) = 0$. Xét tính đúng/sai của các mệnh đề:

* **a)** Phương trình luôn có ít nhất 2 nghiệm phân biệt thuộc khoảng $(0; 2\pi)$ với mọi $m \in \mathbb{R}$.
* **b)** Khi $m = 1$, phương trình có đúng 3 nghiệm phân biệt trên đoạn $[0; 2\pi]$.
* **c)** Điều kiện cần và đủ để phương trình có đúng 4 nghiệm phân biệt trên đoạn $[-\pi; \pi]$ là $m \in (-1; 1) \setminus \left\{-\dfrac{1}{2}\right\}$.
* **d)** Giả sử $m = -\dfrac{1}{2}$, tổng tất cả các nghiệm của phương trình trên đoạn $[0; 10\pi]$ là $25\pi$.

---

#### Câu 13: [Trắc nghiệm 4 lựa chọn]
Có bao nhiêu giá trị nguyên của tham số $m \in [-10; 10]$ để phương trình $m\sin x + (m+1)\cos x = m+2$ có nghiệm thực?

* **A.** 17
* **B.** 18
* **C.** 19
* **D.** 20

---

#### Câu 14: [Kéo thả phương án]
Xét phương trình lượng giác $\sin 2x = 0$ trên đoạn $[0; 10\pi]$.
1. Số lượng các nghiệm phân biệt của phương trình trên đoạn $[0; 10\pi]$ là `[ (1) ]`.
2. Tổng của tất cả các nghiệm đó có giá trị bằng `[ (2) ]`.

---

#### Câu 15: [Trả lời ngắn]
Số giờ ánh sáng mặt trời trong ngày tại một thành phố được mô hình hóa bởi $H(t) = 12 + 3\sin\left[\dfrac{2\pi}{365}(t-80)\right]$ ($1 \le t \le 365$). Một loại cây công nghiệp chỉ sinh trưởng tốt nếu thời gian chiếu sáng $> 13,5$ giờ. Hỏi trong một năm không nhuận ($365$ ngày), có bao nhiêu ngày cây có thể sinh trưởng tốt?

---

#### Câu 16: [Trả lời ngắn]
Tìm giá trị của tham số thực $m$ để hàm số $y = \dfrac{\sin x + m\cos x + 1}{\cos x - \sin x + 2}$ có giá trị lớn nhất đúng bằng 2.

---

#### Câu 17: [Trắc nghiệm 4 lựa chọn]
Giải phương trình lượng giác $\sin x + \sin 2x + \sin 3x = 0$. Hỏi các nghiệm của phương trình này được biểu diễn bởi bao nhiêu điểm phân biệt trên đường tròn lượng giác?

* **A.** 4
* **B.** 5
* **C.** 6
* **D.** 8

---

#### Câu 18: [Đúng/Sai]
Cho phương trình $\sin^4 x + \cos^4 x = m$. Xét tính đúng/sai của các mệnh đề:

* **a)** Khi $m = 1$, phương trình có đúng 4 nghiệm phân biệt trên đoạn $[0; \pi]$.
* **b)** Điều kiện cần và đủ để phương trình có nghiệm là $m \in \left[\dfrac{1}{2}; 1\right]$.
* **c)** Khi $m = \dfrac{3}{4}$, các điểm biểu diễn tập nghiệm trên đường tròn lượng giác tạo thành đỉnh của một hình bát giác đều.
* **d)** Nếu $m = \dfrac{1}{2}$, phương trình tương đương với $\cos 4x = -1$.

---

#### Câu 19: [Trả lời ngắn]
Tính chính xác giá trị của tổng hữu hạn: $S = \sin^2 10^\circ + \sin^2 20^\circ + \sin^2 30^\circ + \dots + \sin^2 170^\circ + \sin^2 180^\circ$.

---

#### Câu 20: [Kéo thả phương án]
1. Phương trình $3\sin x + 4\cos x = m$ có nghiệm khi $m \in$ `[ ... ]`
2. Phương trình $\sin^2 x - 2\sin x + m = 0$ có nghiệm khi $m \in$ `[ ... ]`
3. Phương trình $\cos 2x - 4\cos x + m = 0$ có nghiệm khi $m \in$ `[ ... ]`

---

## III. LỜI GIẢI CHI TIẾT CÁC CÂU HỎI TỰ LUẬN & ĐIỂM NÓNG

### 🔍 Lời giải Câu 1: Mô hình Vòng quay Mặt Trời
- Độ cao tâm vòng quay là vị trí cân bằng $\Rightarrow B = 60$.
- Bán kính vòng quay ứng với biên độ $|A| = 50$. Tại $t=0$ cabin ở vị trí thấp nhất $h(0) = 10\text{m} \Rightarrow A\cos(0) + 60 = 10 \Rightarrow A = -50$.
- Chu kỳ $T = 15\text{ phút} \Rightarrow \omega = \dfrac{2\pi}{15}$.
- Phương trình độ cao: $h(t) = -50\cos\left(\dfrac{2\pi}{15}t\right) + 60$.
- Cho $h(t) = 85$:
  $$-50\cos\left(\dfrac{2\pi}{15}t\right) + 60 = 85 \Leftrightarrow \cos\left(\dfrac{2\pi}{15}t\right) = -\dfrac{1}{2} \Rightarrow \dfrac{2\pi}{15}t = \dfrac{2\pi}{3} \Rightarrow t = 5 \text{ (phút)}.$$

### 🔍 Lời giải Câu 2: Đọc đồ thị hàm số lượng giác
- Đường trung bình $d = \dfrac{y_{\max} + y_{\min}}{2} = \dfrac{4 + (-2)}{2} = 1$.
- Biên độ $a = \dfrac{y_{\max} - y_{\min}}{2} = \dfrac{4 - (-2)}{2} = 3$.
- Tần số góc $b = \dfrac{2\pi}{T} = \dfrac{2\pi}{\pi} = 2$.
- Pha ban đầu $c = -\dfrac{\pi}{3}$ thỏa mãn $c \in (-\pi; 0)$.
- Tổng $P = a + b + c + d = 3 + 2 - \dfrac{\pi}{3} + 1 = 6 - \dfrac{\pi}{3}$.
- **Chọn đáp án A.**

### 🔍 Lời giải Câu 3: Mực nước cảng biển
- Điều kiện cập cảng an toàn:
  $$3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12 \ge 13,5 \Leftrightarrow \cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) \ge \dfrac{1}{2}$$
- Giải phương trình trên $[0; 24]$ thu được 2 khoảng thời gian: $[8; 12]$ (4 tiếng) và $[20; 24]$ (4 tiếng).
- **Tổng thời gian = 8 giờ.**

### 🔍 Lời giải Câu 4: Phân tích nghiệm phương trình lượng giác
- **a) Đúng:** $2\cos^2 x - (2m+1)\cos x + m = 0 \Leftrightarrow (2\cos x - 1)(\cos x - m) = 0$.
- **b) Sai:** Khi $m = 1$, phương trình cho 4 nghiệm phân biệt trên $[0; 2\pi]$ là $x \in \left\{0; \dfrac{\pi}{3}; \dfrac{5\pi}{3}; 2\pi\right\}$.
- **c) Đúng:** $m = -1$ sinh ra đúng 1 nghiệm độc lập $x = \pi$, tổng là 3 nghiệm.
- **d) Sai:** Nhân tử $(2\cos x - 1) = 0$ luôn cho 2 nghiệm cố định với mọi $m$.

        # NÚT NỘP BÀI THI
        submit_btn = st.form_submit_button("🚀 NỘP BÀI THI TSA", type="primary", use_container_width=True)
        
        if submit_btn:
            st.session_state.exam_submitted = True
            st.rerun()

# 7. MÀN HÌNH BÁO KẾT QUẢ VÀ LỜI GIẢI CHI TIẾT
else:
    st.balloons()
    st.success("🎉 BẠN ĐÃ HOÀN THÀNH BÀI THI TSA!")
    
    # Tính điểm
    total_score = 0.0
    
    # Kiểm tra Câu 1
    c1_correct = (st.session_state.get("q1_a") == "-50" and 
                  st.session_state.get("q1_w") == r"\dfrac{2\pi}{15}" and 
                  st.session_state.get("q1_b") == "60" and 
                  st.session_state.get("q1_t") == "5")
    if c1_correct: total_score += 2.5
    
    # Kiểm tra Câu 2
    c2_correct = st.session_state.get("q2") and st.session_state.get("q2").startswith("A.")
    if c2_correct: total_score += 2.5
    
    # Kiểm tra Câu 3
    c3_correct = st.session_state.get("q3", "").strip() == "8"
    if c3_correct: total_score += 2.5
    
    # Kiểm tra Câu 4
    c4_score = 0
    if st.session_state.get("q4_1") == "Đúng": c4_score += 1
    if st.session_state.get("q4_2") == "Sai": c4_score += 1
    if st.session_state.get("q4_3") == "Đúng": c4_score += 1
    if st.session_state.get("q4_4") == "Sai": c4_score += 1
    
    if c4_score == 4: total_score += 2.5
    elif c4_score == 3: total_score += 1.5
    elif c4_score == 2: total_score += 0.75
    elif c4_score == 1: total_score += 0.25

    # Hiển thị điểm số
    st.markdown(f"""
    <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
        <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM BÀI THI: {total_score:.2f} / 10.0</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📖 LỜI GIẢI CHI TIẾT CÁC CÂU HỎI")

    # Lời giải Câu 1
    with st.expander("🔍 Lời giải Câu 1: Mô hình Vòng quay Mặt Trời"):
        st.markdown(r"""
        - Độ cao tâm vòng quay là vị trí cân bằng $\Rightarrow B = 60$.
        - Bán kính vòng quay ứng với biên độ $|A| = 50$. Tại $t=0$ cabin ở vị trí thấp nhất $h(0) = 10\text{m} \Rightarrow A\cos(0) + 60 = 10 \Rightarrow A = -50$.
        - Chu kỳ $T = 15$ phút $\Rightarrow \omega = \dfrac{2\pi}{T} = \dfrac{2\pi}{15}$.
        - Phương trình độ cao: $h(t) = -50\cos\left(\dfrac{2\pi}{15}t\right) + 60$.
        - Để đạt độ cao $85\text{m}$: $-50\cos\left(\dfrac{2\pi}{15}t\right) + 60 = 85 \Leftrightarrow \cos\left(\dfrac{2\pi}{15}t\right) = -\dfrac{1}{2} \Rightarrow \dfrac{2\pi}{15}t = \dfrac{2\pi}{3} \Rightarrow t = 5$ (phút).
        """)

    # Lời giải Câu 2
    with st.expander("🔍 Lời giải Câu 2: Đọc đồ thị hàm số lượng giác"):
        st.markdown(r"""
        - Đường trung bình $d = \dfrac{y_{\max} + y_{\min}}{2} = \dfrac{4 + (-2)}{2} = 1$.
        - Biên độ $a = \dfrac{y_{\max} - y_{\min}}{2} = \dfrac{4 - (-2)}{2} = 3$.
        - Tần số góc $b = \dfrac{2\pi}{T} = \dfrac{2\pi}{\pi} = 2$.
        - Pha ban đầu $c = -\dfrac{\pi}{3}$ thỏa mãn $c \in (-\pi; 0)$.
        - Tổng $P = a + b + c + d = 3 + 2 - \dfrac{\pi}{3} + 1 = 6 - \dfrac{\pi}{3}$.
        - **Chọn đáp án A.**
        """)

    # Lời giải Câu 3
    with st.expander("🔍 Lời giải Câu 3: Mực nước cảng biển"):
        st.markdown(r"""
        - Điều kiện tàu cập cảng an toàn: $3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12 \ge 13,5 \Leftrightarrow \cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) \ge \dfrac{1}{2}$.
        - Giải bất phương trình lượng giác thu được: $-4 + 12k \le t \le 12k$.
        - Xét $t \in [0; 24]$:
          + Với $k = 1 \Rightarrow 8 \le t \le 12$ ($4$ tiếng).
          + Với $k = 2 \Rightarrow 20 \le t \le 24$ ($4$ tiếng).
        - Tổng thời gian tàu cập cảng an toàn là $4 + 4 = 8$ giờ.
        """)

    # Lời giải Câu 4
    with st.expander("🔍 Lời giải Câu 4: Phân tích nghiệm phương trình lượng giác"):
        st.markdown(r"""
        - **a) Đúng:** $2\cos^2 x - (2m+1)\cos x + m = 0 \Leftrightarrow (2\cos x - 1)(\cos x - m) = 0$.
        - **b) Sai:** Khi $m = 1$, phương trình cho $4$ nghiệm phân biệt trên $[0; 2\pi]$ bao gồm $x \in \left\{0; \dfrac{\pi}{3}; \dfrac{5\pi}{3}; 2\pi\right\}$.
        - **c) Đúng:** Để có $3$ nghiệm phân biệt trên $[0; 2\pi]$, nhánh $\cos x = m$ phải sinh ra đúng $1$ nghiệm phân biệt độc lập $\Rightarrow m = -1$ (cho nghiệm $x = \pi$).
        - **d) Sai:** Nhân tử $(2\cos x - 1) = 0$ luôn cho $2$ nghiệm cố định $\Rightarrow$ Phương trình luôn có nghiệm với mọi $m$.
        """)
