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
# คำนวณค่าต่างๆ ผ่าน Module
f_details = design_flexure(Mu, b, h, fc_prime, fy, covering)
s_details = design_shear(Vu, b, h, fc_prime, fy, covering)

# ดึงค่ามาใช้อย่างปลอดภัยด้วย .get() เพื่อป้องกัน KeyError
As_req = f_details.get('As_req', 0.0)
As_prime = f_details.get('As_prime', 0.0)
f_type = f_details.get('type', 'Singly')
f_msg = f_details.get('msg', 'ไม่พบข้อมูล')
s_msg = s_details.get('msg', 'ไม่พบข้อมูล')

# เตรียมข้อมูลสำหรับ Export
inputs_data = {
    'b': b, 'h': h, 'fc_prime': fc_prime, 'fy': fy, 
    'Mu': Mu, 'Vu': Vu
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
        
        # แสดงตารางแนะนำเหล็กเสริม
        st.markdown("---")
        st.write("💡 **ตารางแนะนำหน้าตัดเหล็ก (As):**")
        df_rebar = suggest_main_rebar(As_req, b)
        if df_rebar is not None:
            st.dataframe(df_rebar, hide_index=True)

    with col2:
        st.subheader("📥 รายงานและเอกสาร")
        # แสดงข้อความรายงานสรุป
        report_text = generate_report_text(inputs_data, f_details, s_details)
        st.text_area("Preview Report", report_text, height=200)
        
        # ปุ่มดาวน์โหลด PDF
        try:
            pdf_data = export_as_pdf(inputs_data, f_details, s_details)
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