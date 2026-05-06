import streamlit as st
from modules.flexure import design_flexure
from modules.shear import design_shear
from modules.drawing import generate_beam_diagram
from modules.rebar import suggest_main_rebar
from modules.report import generate_report_text, export_as_pdf

st.set_page_config(page_title="RC Beam Design Pro", layout="wide")
st.title("🏗️ โปรแกรมออกแบบคานคอนกรีตเสริมเหล็ก")

with st.sidebar:
    st.header("📌 ข้อมูลนำเข้า (Inputs)")
    b = st.number_input("ความกว้างคาน b (cm)", value=20.0)
    h = st.number_input("ความลึกคาน h (cm)", value=40.0)
    fc_prime = st.number_input("กำลังคอนกรีต fc' (ksc)", value=240.0)
    fy = st.number_input("กำลังเหล็กเสริม fy (ksc)", value=4000.0)
    fyv = st.number_input("กำลังเหล็กปลอก fyv (ksc)", value=2400.0)
    Mu = st.number_input("โมเมนต์ดัด Mu (kg-m)", value=5000.0)
    Vu = st.number_input("แรงเฉือน Vu (kg)", value=3000.0)
    covering = 3.0

# --- ประมวลผล ---
d = h - covering
d_prime = covering

# 1. คำนวณแรงดัด (รับค่ากลับมา 5 ตัว ตามไฟล์ flexure.py)
f_type, As_req, As_prime, f_msg, f_details = design_flexure(fc_prime, fy, b, d, d_prime, Mu)

# 2. คำนวณแรงเฉือน (รับค่ากลับมา 4 ตัว ตามไฟล์ shear.py)
Av, s_spacing, s_msg, s_details = design_shear(fc_prime, fyv, b, d, Vu)

# 3. จัดเตรียมข้อมูลทำรายงาน
inputs_data = {'b': b, 'h': h, 'fc_prime': fc_prime, 'fy': fy, 'Mu': Mu, 'Vu': Vu}
flex_report_data = {'type': f_type, 'As_req': As_req, 'As_prime': As_prime, 'msg': f_msg}
shear_report_data = {'msg': s_msg}

# --- UI แสดงผล ---
tab_calc, tab_draw = st.tabs(["📊 ผลการคำนวณ", "✍️ แบบขยายคาน"])

with tab_calc:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.success(f"**การรับแรงดัด:** {f_msg}")
        st.write(f"- As (รับดึง): **{As_req:.2f} sq.cm**")
        if f_type == "Doubly":
            st.write(f"- A's (รับอัด): **{As_prime:.2f} sq.cm**")
        
        st.warning(f"**การรับแรงเฉือน:** {s_msg}")
        
        st.markdown("---")
        st.write("💡 **ตารางแนะนำเหล็กเสริมรับแรงดึง (As):**")
        df_rebar_tension = suggest_main_rebar(As_req, b, covering)
        if df_rebar_tension is not None:
            st.dataframe(df_rebar_tension, hide_index=True)

        if f_type == "Doubly" and As_prime > 0:
            st.write("💡 **ตารางแนะนำเหล็กเสริมรับแรงอัด (A's):**")
            df_rebar_comp = suggest_main_rebar(As_prime, b, covering)
            if df_rebar_comp is not None:
                st.dataframe(df_rebar_comp, hide_index=True)

    with c2:
        st.subheader("📥 รายงานและเอกสาร")
        report_text = generate_report_text(inputs_data, flex_report_data, shear_report_data)
        st.text_area("Preview Report", report_text, height=250)
        
        try:
            pdf_data = export_as_pdf(inputs_data, flex_report_data, shear_report_data)
            st.download_button(label="📥 ดาวน์โหลดรายงาน (PDF)", data=pdf_data, file_name="Beam_Report.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"ไม่สามารถสร้าง PDF ได้: {e}")

with tab_draw:
    st.subheader("🖼️ แบบรายละเอียดหน้าตัดคาน")
    fig = generate_beam_diagram(b, h, As_req, As_prime)
    st.pyplot(fig)