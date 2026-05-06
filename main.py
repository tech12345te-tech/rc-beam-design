import streamlit as st
from modules.flexure import design_flexure
from modules.shear import design_shear
from modules.drawing import generate_beam_diagram
from modules.rebar import suggest_main_rebar
from modules.report import generate_report_text, export_as_pdf

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="RC Beam Design Pro", layout="wide")
st.title("🏗️ โปรแกรมออกแบบคานคอนกรีตเสริมเหล็ก")

# --- ส่วนรับข้อมูล (Sidebar) ---
with st.sidebar:
    st.header("📌 ข้อมูลนำเข้า (Inputs)")
    b = st.number_input("ความกว้างคาน b (cm)", value=20.0)
    h = st.number_input("ความลึกคาน h (cm)", value=40.0)
    fc_prime = st.number_input("กำลังคอนกรีต fc' (ksc)", value=240.0)
    fy = st.number_input("กำลังเหล็กเสริม fy (ksc)", value=4000.0)
    Mu = st.number_input("โมเมนต์ดัด Mu (kg-m)", value=5000.0)
    Vu = st.number_input("แรงเฉือน Vu (kg)", value=3000.0)
    covering = 3.0

# --- ส่วนประมวลผล ---
d = h - covering  # คำนวณความลึกประสิทธิผล (d)
d_prime = covering # สมมติระยะหุ้มเหล็กรับแรงอัดเท่ากับ covering

# 1. คำนวณแรงดัด: ส่งค่า 6 ตัวเรียงตามใน flexure.py และรอรับค่ากลับมา 5 ตัว
f_type, As_req, As_prime, f_msg, f_details_dict = design_flexure(fc_prime, fy, b, d, d_prime, Mu)

# 2. คำนวณแรงเฉือน: ส่งค่า 5 ตัวเรียงตามใน shear.py และรอรับค่ากลับมา 4 ตัว
Av, s_spacing, s_msg, s_details_dict = design_shear(fc_prime, fy, b, d, Vu)

# 3. เตรียมข้อมูลสำหรับทำรายงาน (แพ็กใส่ Dictionary ให้ไฟล์ report.py ใช้งาน)
inputs_data = {
    'b': b, 'h': h, 'fc_prime': fc_prime, 'fy': fy, 
    'Mu': Mu, 'Vu': Vu
}
flex_report_data = {
    'type': f_type, 'As_req': As_req, 'As_prime': As_prime, 'msg': f_msg
}
shear_report_data = {
    'msg': s_msg
}

# --- ส่วนแสดงผล (Main UI) ---
tab_calc, tab_draw = st.tabs(["📊 ผลการคำนวณ", "✍️ แบบขยายคาน"])

with tab_calc:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 สรุปผลการออกแบบ")
        st.success(f"**การรับแรงดัด:** {f_msg}")
        st.write(f"- พื้นที่เหล็กรับแรงดึง (As): **{As_req:.2f} sq.cm**")
        if f_type == "Doubly":
            st.write(f"- พื้นที่เหล็กรับแรงอัด (A's): **{As_prime:.2f} sq.cm**")
        
        st.warning(f"**การรับแรงเฉือน:** {s_msg}")
        
        # ตารางแนะนำหน้าตัดเหล็ก
        st.markdown("---")
        st.write("💡 **ตารางแนะนำหน้าตัดเหล็ก (As):**")
        df_rebar = suggest_main_rebar(As_req, b, covering)
        if df_rebar is not None:
            st.dataframe(df_rebar, hide_index=True)

    with col2:
        st.subheader("📥 รายงานและเอกสาร")
        # แสดงตัวอย่างรายงานโดยใช้ข้อมูลที่แพ็กไว้
        report_text = generate_report_text(inputs_data, flex_report_data, shear_report_data)
        st.text_area("Preview Report", report_text, height=200)
        
        try:
            pdf_data = export_as_pdf(inputs_data, flex_report_data, shear_report_data)
            st.download_button(
                label="📥 ดาวน์โหลดรายงาน (PDF)",
                data=pdf_data,
                file_name=f"Beam_Design_{Mu}kgm.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"ไม่สามารถสร้าง PDF ได้: {e}")

with tab_draw:
    st.subheader("🖼️ แบบรายละเอียดหน้าตัดคาน")
    fig = generate_beam_diagram(b, h, As_req, As_prime)
    st.pyplot(fig)