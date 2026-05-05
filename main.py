import streamlit as st
from datetime import datetime

# นำเข้าฟังก์ชันจากโฟลเดอร์ modules
from modules.flexure import design_flexure
from modules.shear import design_shear
from modules.report import generate_report_text
from modules.drawing import generate_beam_diagram

st.set_page_config(page_title="โปรแกรมออกแบบคาน RC", layout="wide")
st.title("🏗️ โปรแกรมออกแบบคานคอนกรีตเสริมเหล็ก (Modular)")

st.sidebar.header("📝 กำหนดค่า (Input)")
fc_prime = st.sidebar.number_input("f'c (ksc)", value=240)
fy = st.sidebar.number_input("fy (ksc)", value=4000)
fyv = st.sidebar.number_input("fyv (ksc)", value=2400)
b = st.sidebar.number_input("b (cm)", value=20.0)
h = st.sidebar.number_input("h (cm)", value=50.0)
covering = st.sidebar.number_input("Covering (cm)", value=3.0)
Mu = st.sidebar.number_input("Mu (kg-m)", value=5000.0)
Vu = st.sidebar.number_input("Vu (kg)", value=3500.0)

# คำนวณ d เบื้องต้น
d = h - covering - 0.9 - 0.8
d_prime = covering + 0.9 + 0.8
inputs = {'fc_prime': fc_prime, 'fy': fy, 'fyv': fyv, 'b': b, 'h': h, 'd': d, 'd_prime': d_prime, 'Mu': Mu, 'Vu': Vu, 'covering': covering}

# แบ่งหน้าจอเป็น Tabs 
tab_calc, tab_report = st.tabs(["🧮 ผลการคำนวณ & หน้าตัด", "📄 รายการคำนวณ (Report)"])

with tab_calc:
    if st.button("เริ่มออกแบบ", type="primary"):
        # 1. เรียกใช้โมดูลรับแรงดัด
        f_type, As_req, As_prime, f_msg, f_details = design_flexure(fc_prime, fy, b, d, d_prime, Mu)
        # 2. เรียกใช้โมดูลรับแรงเฉือน
        Av, s_shear, s_msg, s_details = design_shear(fc_prime, fyv, b, d, Vu)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.success("**การรับแรงดัด:** " + f_msg)
            st.write(f"- As (รับดึง): **{As_req:.2f} sq.cm**")
            if f_type == "Doubly":
                st.write(f"- A's (รับอัด): **{As_prime:.2f} sq.cm**")
                
            st.warning("**การรับแรงเฉือน:** " + s_msg)
            
        with c2:
            # 3. เรียกใช้โมดูลวาดภาพ
            fig = generate_beam_diagram(inputs, As_req, As_prime, s_details)
            st.pyplot(fig)

        # เอาค่า As_req และ As_prime ยัดเข้าไปใน f_details ก่อนส่งไปทำ Report
        f_details['As_req'] = As_req
        f_details['As_prime'] = As_prime

        # เก็บค่าไว้ใช้ใน Tab Report
        st.session_state['report'] = generate_report_text(inputs, f_details, s_details)

with tab_report:
    if 'report' in st.session_state:
        st.code(st.session_state['report'], language='markdown')
        st.download_button("📥 ดาวน์โหลด .txt", st.session_state['report'], "report.txt")
    else:
        st.info("กรุณากด 'เริ่มออกแบบ' ในแท็บแรกก่อนครับ")