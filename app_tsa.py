import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Hệ Thống Thi TSA - Toán Thầy Tùng", layout="wide")

# =========================================================================
# KHO DỮ LIỆU ĐỀ THI (Cấu hình chi tiết từng câu Phần IV)
# =========================================================================
TSA_EXAMS_BANK = {
    "de_tsa_1": {
        "title": "Đề TSA 01: Khảo sát chất lượng Toán Tư Duy",
        "pdf_id": "ID_FILE_DE_TSA_1",  
        "giai_id": "ID_FILE_GIAI_TSA_1", 
        "key_p1": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C"],
        "key_p2": {
            16: {"a": "Đúng", "b": "Sai"},
            17: {"a": "Sai", "b": "Đúng", "c": "Sai"},
            18: {"a": "Đúng", "b": "Đúng", "c": "Sai", "d": "Sai"},
            19: {"a": "Sai", "b": "Sai", "c": "Đúng"},
            20: {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Đúng"},
        },
        "key_p3": ["15", "0", "-2", "3.14", "10", "5", "100", "0.5", "-1", "7"],
        
        # Phần IV: Định nghĩa chi tiết từng câu từ 31 đến 40
        "data_p4": {
            31: {"options": ["--- Chọn ---", "Đồng biến", "Nghịch biến"], "slots": ["a", "b"]},
            32: {"options": ["--- Chọn ---", "Tiệm cận đứng x=1", "Tiệm cận ngang y=2"], "slots": ["a", "b"]},
            33: {"options": ["--- Chọn ---", "D = R", "D = R \\ {1}"], "slots": ["a"]},
            34: {"options": ["--- Chọn ---", "Cực đại", "Cực tiểu", "Không có cực trị"], "slots": ["a", "b"]},
            35: {"options": ["--- Chọn ---", "Đồng biến", "Nghịch biến"], "slots": ["a", "b"]},
            36: {"options": ["--- Chọn ---", "Tiệm cận đứng x=1", "Tiệm cận ngang y=2"], "slots": ["a", "b"]},
            37: {"options": ["--- Chọn ---", "D = R", "D = R \\ {1}"], "slots": ["a"]},
            38: {"options": ["--- Chọn ---", "Cực đại", "Cực tiểu", "Không có cực trị"], "slots": ["a", "b"]},
            39: {"options": ["--- Chọn ---", "Đồng biến", "Nghịch biến"], "slots": ["a"]},
            40: {"options": ["--- Chọn ---", "Tiệm cận đứng x=1", "Tiệm cận ngang y=2"], "slots": ["a", "b"]}
        },
        "key_p4": {
            31: {"a": "Đồng biến", "b": "Nghịch biến"},
            32: {"a": "Tiệm cận đứng x=1", "b": "Tiệm cận ngang y=2"},
            33: {"a": "D = R \\ {1}"},
            34: {"a": "Cực đại", "b": "Cực tiểu"},
            35: {"a": "Đồng biến", "b": "Nghịch biến"},
            36: {"a": "Tiệm cận đứng x=1", "b": "Tiệm cận ngang y=2"},
            37: {"a": "D = R \\ {1}"},
            38: {"a": "Cực đại", "b": "Cực tiểu"},
            39: {"a": "Đồng biến"},
            40: {"a": "Tiệm cận đứng x=1", "b": "Tiệm cận ngang y=2"}
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
