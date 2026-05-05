from datetime import datetime

def generate_report_text(inputs, flex, shear):
    """สร้างรายการคำนวณแบบ Text"""
    report = f"=========================================================\n"
    report += f"                 รายการคำนวณออกแบบคาน ค.ส.ล.                 \n"
    report += f"=========================================================\n"
    report += f"วันที่คำนวณ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report += f"[1. ข้อมูลนำเข้า]\n"
    report += f"- f'c = {inputs['fc_prime']} ksc | fy = {inputs['fy']} ksc\n"
    report += f"- b = {inputs['b']} cm | h = {inputs['h']} cm | d = {inputs['d']:.2f} cm\n"
    report += f"- Mu = {inputs['Mu']} kg-m | Vu = {inputs['Vu']} kg\n\n"
    
    report += f"[2. ออกแบบรับแรงดัด]\n"
    report += f"- As_min = {flex['As_min']:.2f} sq.cm\n"
    report += f"- Mu_max = {flex['Mu_max']:.2f} kg-m\n"
    
    if flex['type'] == 'Singly':
        report += f"** ออกแบบเป็นเหล็กเสริมเดี่ยว **\n"
    else:
        report += f"** ต้องออกแบบเป็นเหล็กเสริมคู่ **\n"
        
    report += f">>> ต้องการเหล็กรับแรงดึง (As) = {flex['As_req']:.2f} sq.cm\n"
    if flex['type'] == 'Doubly':
        report += f">>> ต้องการเหล็กรับแรงอัด (A's) = {flex['As_prime']:.2f} sq.cm\n\n"
    
    report += f"[3. ออกแบบรับแรงเฉือน]\n"
    if shear.get('s_practise'):
        report += f">>> ใช้เหล็กปลอก RB9 ระยะเรียง (s) = {shear['s_practise']} ซม.\n"
    else:
        report += f">>> หน้าตัดรับแรงเฉือนได้โดยไม่ต้องเสริมเหล็กปลอกตามทฤษฎี\n"
        
    return report