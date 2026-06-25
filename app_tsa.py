import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Hệ Thống Thi TSA - Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI
# =========================================================================
TSA_EXAMS_BANK = {
    "de_tsa_1": {
        "title": "Đề TSA 01: Khảo sát chất lượng Toán Tư Duy",
        "pdf_id": "1-Ywkq3yBNGIcHwOHXQ_mrpIqKvPzMOGN",  
        "giai_id": "1zqr0tGj-3dl64iI_RiPQsOkZ3fpBCLHr", 
        "key_p1": ["B", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
        "key_p2": {
            16: {"a": "Đúng", "b": "Sai"},
            17: {"a": "Đúng", "b": "Đúng", "c": "Đúng"},
            18: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            19: {"a": "Đúng", "b": "Sai", "c": "Đúng"},
            20: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["72", "16", "70", "8", "16", "5", "2.25", "2429", "1000", "3"],
        
        "data_p4": {
            31: {"options": ["--- Chọn ---", "15", "60", "84", "120", "220"], "slots": ["1", "2", "3"]},
            32: {"options": ["--- Chọn ---", "2", "4", "16", "32", "48"], "slots": ["1", "2", "3"]},
            33: {"options": ["--- Chọn ---", "-1", "1", "2", "3", "5"], "slots": ["1", "2", "3"]},
            34: {"options": ["--- Chọn ---", "1/5", "1/2", "2", "5", "7"], "slots": ["1", "2", "3"]},
            35: {"options": ["--- Chọn ---", "1", "3", "5", "8", "10"], "slots": ["1", "2", "3"]},
            36: {"options": ["--- Chọn ---", "-2", "0.5", "2", "4", "6"], "slots": ["1", "2", "3"]},
            37: {"options": ["--- Chọn ---", "0.5", "1", "2", "4"], "slots": ["1", "2", "3"]},
            38: {"options": ["--- Chọn ---", "2.4", "5", "6", "8", "12"], "slots": ["1", "2", "3"]},
            39: {"options": ["--- Chọn ---", "3", "4", "4000", "16000", "32000"], "slots": ["1", "2", "3"]},
            40: {"options": ["--- Chọn ---", "-2", "0", "2", "3", "9"], "slots": ["1", "2", "3"]}
        },
        "key_p4": {
            31: {"1": "15", "2": "60", "3": "84"},
            32: {"1": "4", "2": "2", "3": "8"},
            33: {"1": "3", "2": "2", "3": "-1"},
            34: {"1": "7", "2": "2", "3": "1/5"},
            35: {"1": "3", "2": "8", "3": "5"},
            36: {"1": "4", "2": "2", "3": "-2"},
            37: {"1": "4", "2": "2", "3": "0.5"},
            38: {"1": "6", "2": "8", "3": "2.4"},
            39: {"1": "4000", "2": "16000", "3": "3"},
            40: {"1": "9", "2": "3", "3": "0"} # Đã sửa lỗi trùng lặp khóa
        }
    }
}

# GIAO DIỆN
st.title("🎯 HỆ THỐNG THI ĐÁNH GIÁ TƯ DUY (TSA)")
selected_exam_key = st.sidebar.selectbox("Chọn đề:", options=list(TSA_EXAMS_BANK.keys()))
current_exam = TSA_EXAMS_BANK[selected_exam_key]

col1, col2 = st.columns([6, 4])
with col1:
    st.subheader("📑 Đề thi")
    st.components.v1.iframe(f"https://drive.google.com/file/d/{current_exam['pdf_id']}/preview", height=1000)

with col2:
    # Đồng hồ nằm ngoài form để không bị reset khi nộp bài
    st.components.v1.html(f"""
    <div id="timer" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px;">⏳ 120:00</div>
    <script>
    var deadline = new Date(Date.now() + 60 * 60 * 1000);
    setInterval(() => {{
        var t = deadline - Date.now();
        var m = Math.floor(t / 60000), s = Math.floor((t/1000)%60);
        document.getElementById('timer').innerHTML = "⏳ " + (m<10?"0":"") + m + ":" + (s<10?"0":"") + s;
    }}, 1000);
    </script>
    """, height=70)
    
    with st.form(key="exam_form"): # Chỉ giữ 1 form duy nhất
        st.subheader("PHẦN I (1-15)")
        p1_answers = {i: st.radio(f"Câu {i}", ["A","B","C","D"], horizontal=True, index=None, key=f"p1_{i}") for i in range(1, 16)}
        
        st.subheader("PHẦN II (16-20)")
        p2_answers = {}
        for i in range(16, 21):
            st.markdown(f"**Câu {i}:**")
            branches = list(current_exam["key_p2"][i].keys())
            cols = st.columns(len(branches))
            p2_answers[i] = {b: cols[idx].radio(f"Ý {b}", ["Đúng", "Sai"], index=None, key=f"p2_{i}_{b}") for idx, b in enumerate(branches)}
        
        st.subheader("PHẦN III (21-30)")
        p3_answers = {i: st.text_input(f"Câu {i}", key=f"p3_{i}") for i in range(21, 31)}
        
        st.subheader("PHẦN IV (31-40)")
        p4_answers = {}
        for cau_id in range(31, 41):
            data = current_exam["data_p4"].get(cau_id)
            if data:
                st.markdown(f"**Câu {cau_id}:**")
                p4_answers[cau_id] = {}
                cols = st.columns(len(data["slots"]))
                for idx, slot in enumerate(data["slots"]):
                    p4_answers[cau_id][slot] = cols[idx].selectbox(f"Ô {slot}", options=data["options"], key=f"p4_{cau_id}_{slot}")

        submitted = st.form_submit_button("NỘP BÀI", use_container_width=True)

    if submitted:
        # CHẤM ĐIỂM
        c1 = sum(1 for i in range(1, 16) if p1_answers[i] == current_exam["key_p1"][i-1])
        c2 = sum(1 for i in range(16, 21) for b, v in p2_answers[i].items() if v == current_exam["key_p2"][i][b])
        c3 = sum(1 for i in range(21, 31) if p3_answers[i].strip() == str(current_exam["key_p3"][i-21]))
        c4 = sum(1 for i in range(31, 41) for s, v in p4_answers[i].items() if v == current_exam["key_p4"][i].get(s))
        
        st.success(f"Kết quả: P1:{c1}/15 | P2:{c2} ý đúng | P3:{c3}/10 | P4:{c4} vị trí đúng!")
        st.markdown("---")
        
        # Chỉ tạo duy nhất 1 nút để xem lời giải
        if st.button("📖 Xem lời giải chi tiết (PDF)"):
            st.session_state.show_pdf = True
            
        # Nếu đã bấm nút, hiển thị file PDF
        if "show_pdf" in st.session_state and st.session_state.show_pdf:
            st.components.v1.iframe(
                f"https://drive.google.com/file/d/{current_exam['giai_id']}/preview", 
                height=800
            )










