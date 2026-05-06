from fpdf import FPDF

def generate_report_text(inputs, flex, shear):
    report = "=== รายงานการออกแบบคานคอนกรีตเสริมเหล็ก ===\n"
    report += f"ขนาดคาน: {inputs.get('b')} x {inputs.get('h')} ซม.\n"
    report += "-"*40 + "\n"
    
    report += f">>> การออกแบบรับแรงดัด: {flex.get('msg', 'N/A')}\n"
    report += f"- พื้นที่เหล็กรับแรงดึงที่ต้องการ (As): {flex.get('As_req', 0):.2f} sq.cm\n"
    if flex.get('type') == 'Doubly':
        report += f"- พื้นที่เหล็กรับแรงอัดที่ต้องการ (A's): {flex.get('As_prime', 0):.2f} sq.cm\n"
    report += "\n"
    
    report += f">>> การออกแบบรับแรงเฉือน: {shear.get('msg', 'N/A')}\n"
    report += "-"*40 + "\n"
    return report

def export_as_pdf(inputs, flex, shear):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "RC Beam Design Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Design Inputs", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"- Beam Size: {inputs.get('b')} x {inputs.get('h')} cm", ln=True)
    pdf.cell(0, 7, f"- Concrete Strength (fc'): {inputs.get('fc_prime')} ksc", ln=True)
    pdf.cell(0, 7, f"- Steel Strength (fy): {inputs.get('fy')} ksc", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Flexural Results", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"- Status: {flex.get('msg')}", ln=True)
    pdf.cell(0, 7, f"- As Required: {flex.get('As_req', 0):.2f} sq.cm", ln=True)
    if flex.get('type') == 'Doubly':
        pdf.cell(0, 7, f"- A's Required: {flex.get('As_prime', 0):.2f} sq.cm", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Shear Results", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 7, f"- Status: {shear.get('msg')}", ln=True)
    
    return pdf.output(dest='S')