import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Hệ Thống Thi TSA - Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI (Cấu hình chi tiết từng câu Phần IV)
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
        
        # Phần IV: Định nghĩa chi tiết từng câu từ 31 đến 40
        "data_p4": {
            31: {"options": ["--- Chọn ---", "15", "60" , "84",  "120"  , "220"], "slots": ["a", "b", "c"]},
            32: {"options": ["--- Chọn ---", "2", "4", "16", "32", "48"], "slots": ["a", "b", "c"]},
            33: {"options": ["--- Chọn ---", "-1", "1", "2", "3", "5"], "slots": ["a", "b", "c"]},
            34: {"options": ["--- Chọn ---", "1/5", "1/2", "2", "5", "7"], "slots": ["a", "b", "c"]},
            35: {"options": ["--- Chọn ---", "1", "3", "5", "8", "10"], "slots": ["a", "b", "c"]},
            36: {"options": ["--- Chọn ---", "-2, "0.5", "2", "4", "6"], "slots": ["a", "b", "c"]},
            37: {"options": ["--- Chọn ---", "0.5", "1", "2", "4"], "slots": ["a", "b", "c"]},
            38: {"options": ["--- Chọn ---", "2.4", "5", "6", "8", "12"], "slots": ["a", "b", "c"]},
            39: {"options": ["--- Chọn ---", "3", "4", "4000", "16000", "32000"], "slots": ["a", "b", "c"]},
            40: {"options": ["--- Chọn ---", "-2", "0", "2", "3", "9"], "slots": ["a", "b", "c"]}
        },
        "key_p4": {
            31: {"a": "15", "b": "60", "c": "84"},
            32: {"a": "4", "b": "2", "c": "8"},
            33: {"a": "3", "b": "2", "c": "-1"},
            34: {"a": "7", "b": "2", "c": "1/5"},
            35: {"a": "3", "b": "8", "c": "5"},
            36: {"a": "4", "b": "2", "c": "-2"},
            37: {"a": "4", "b": "2", "c": "0.5"},
            38: {"a": "6", "b": "8", "c": "2.4"},
            39: {"a": "4000", "b": "16000", "c": "3"},
            40: {"a": "9", "b": "2", "b": "3"}
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
    with st.form(key="exam_form"):

    # Đồng hồ đếm ngược 120 phút tự động reset khi đổi đề
    timer_code = f"""
    <div id="timer_{selected_exam_key}" style="background-color: #ff4b4b; color: white; padding: 12px; text-align: center; font-size: 26px; font-weight: bold; border-radius: 8px; margin-bottom: 15px;">
        ⏳ 120:00
    </div>
    <script>
    var time_in_minutes = 120;
    var deadline = new Date(Date.parse(new Date()) + time_in_minutes * 60 * 1000);
    function update_clock(){{
        var t = Date.parse(deadline) - Date.parse(new Date());
        var seconds = Math.floor( (t/1000) % 60 );
        var total_minutes = Math.floor(t / 1000 / 60);
        var clock = document.getElementById('timer_{selected_exam_key}');
        if(!clock) return;
        if(t <= 0){{
            clock.innerHTML = "HẾT GIỜ LÀM BÀI!";
            clock.style.backgroundColor = "black";
        }} else {{
            var m = total_minutes < 10 ? "0" + total_minutes : total_minutes;
            var s = seconds < 10 ? "0" + seconds : seconds;
            clock.innerHTML = "⏳ " + m + ":" + s;
        }}
    }}
    setInterval(update_clock, 1000);
    </script>
    """
    st.components.v1.html(timer_code, height=75)
    
    with st.form(key=f"form_{selected_exam_key}"):
    
        # PHẦN I
        st.subheader("PHẦN I (1-15)")
        p1_answers = {i: st.radio(f"Câu {i}", ["A","B","C","D"], horizontal=True, index=None) for i in range(1, 16)}
        
        # PHẦN II
        st.subheader("PHẦN II (16-20)")
        p2_answers = {}
        for i in range(16, 21):
            branches = list(current_exam["key_p2"][i].keys())
            cols = st.columns(len(branches))
            p2_answers[i] = {b: cols[idx].radio(f"Ý {b}", ["Đúng", "Sai"], index=None) for idx, b in enumerate(branches)}
        
        # PHẦN III
        st.subheader("PHẦN III (21-30)")
        p3_answers = {i: st.text_input(f"Câu {i}") for i in range(21, 31)}
        
        # PHẦN IV (31-40)
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

    # CHẤM ĐIỂM
    if submitted:
        correct_p1 = sum(1 for i in range(1, 16) if p1_answers[i] == current_exam["key_p1"][i-1])
        
        correct_p2 = 0
        total_p2 = 0
        for i in range(16, 21):
            for b, val in p2_answers[i].items():
                total_p2 += 1
                if val == current_exam["key_p2"][i][b]: correct_p2 += 1
                    
        correct_p3 = sum(1 for i in range(21, 31) if p3_answers[i].strip() == str(current_exam["key_p3"][i-21]))
        
        correct_p4 = 0
        total_p4 = 0
        for cau_id in range(31, 41):
            if cau_id in current_exam["key_p4"]:
                for slot, correct_val in current_exam["key_p4"][cau_id].items():
                    total_p4 += 1
                    if p4_answers[cau_id].get(slot) == correct_val:
                        correct_p4 += 1
        
        st.success("🎉 Kết quả bài thi:")
        st.write(f"- Phần I: {correct_p1}/15")
        st.write(f"- Phần II: {correct_p2}/{total_p2}")
        st.write(f"- Phần III: {correct_p3}/10")
        st.write(f"- Phần IV: {correct_p4}/{total_p4} vị trí")
