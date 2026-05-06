from fpdf import FPDF

def generate_report_text(inputs, flex_data, shear_data):
    report = "=== รายงานการออกแบบคานคอนกรีตเสริมเหล็ก ===\n"
    report += f"ขนาดคาน: {inputs.get('b')} x {inputs.get('h')} ซม.\n"
    report += "-"*40 + "\n"
    report += f">>> การออกแบบรับแรงดัด: {flex_data.get('msg')}\n"
    report += f"- พื้นที่เหล็กรับแรงดึง (As): {flex_data.get('As_req', 0):.2f} sq.cm\n"
    if flex_data.get('type') == 'Doubly':
        report += f"- พื้นที่เหล็กรับแรงอัด (A's): {flex_data.get('As_prime', 0):.2f} sq.cm\n"
    report += f"\n>>> การออกแบบรับแรงเฉือน: {shear_data.get('msg')}\n"
    return report

def export_as_pdf(inputs, flex_data, shear_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "RC Beam Design Report", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Inputs:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"- Size: {inputs.get('b')} x {inputs.get('h')} cm", ln=True)
    pdf.cell(0, 7, f"- fc': {inputs.get('fc_prime')} ksc | fy: {inputs.get('fy')} ksc", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Flexural Design:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"- As Req: {flex_data.get('As_req', 0):.2f} sq.cm", ln=True)
    if flex_data.get('type') == 'Doubly':
        pdf.cell(0, 7, f"- A's Req: {flex_data.get('As_prime', 0):.2f} sq.cm", ln=True)
        
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Shear Design:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"- Stirrup spacing result is shown in UI.", ln=True)
    
    return pdf.output(dest='S')