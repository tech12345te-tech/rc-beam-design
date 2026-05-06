import math
import pandas as pd

def suggest_main_rebar(As_req, b, covering=3.0, stirrup_db=0.9):
    """
    ฟังก์ชันแนะนำการจัดเหล็กเสริมหลัก (ใช้ได้ทั้งรับแรงดึงและแรงอัด)
    """
    # ถ้าไม่ต้องใช้เหล็ก (As = 0) ให้ส่งค่าว่างกลับไป
    if As_req <= 0:
        return None
        
    # ฐานข้อมูลหน้าตัดเหล็กข้ออ้อย (ตร.ซม.)
    rebar_db = {
        "DB12": 1.13,
        "DB16": 2.01,
        "DB20": 3.14,
        "DB25": 4.91,
        "DB28": 6.16
    }
    
    suggestions = []
    
    for name, area in rebar_db.items():
        # คำนวณจำนวนเส้น (ปัดขึ้นเสมอ) และบังคับว่าคานต้องมีมุมซ้ายขวาอย่างน้อย 2 เส้น
        num_bars = math.ceil(As_req / area)
        if num_bars < 2:
            num_bars = 2
            
        As_provided = num_bars * area
        
        # คำนวณว่าใส่ 1 ชั้นพอไหม?
        db_cm = math.sqrt((area * 4) / math.pi) # ขนาดเส้นผ่านศูนย์กลางจริง (ซม.)
        clear_spacing = max(2.5, db_cm) # ระยะห่างช่องว่างอย่างน้อย 2.5 ซม. หรือเท่ากับ db
        
        # พื้นที่ความกว้างคานที่ใส่เหล็กได้ (หักระยะหุ้มและเหล็กปลอก 2 ฝั่ง)
        avail_width = b - (2 * covering) - (2 * stirrup_db)
        
        # ความกว้างที่ต้องใช้ทั้งหมด
        req_width = (num_bars * db_cm) + ((num_bars - 1) * clear_spacing)
        
        # เช็กสถานะ
        layer_status = "✅ 1 ชั้น" if req_width <= avail_width else "⚠️ 2 ชั้น"
        
        suggestions.append({
            "เหล็ก": name,
            "จำนวน": num_bars,
            "รูปแบบ": f"{num_bars} - {name}",
            "จัดให้ (sq.cm)": round(As_provided, 2),
            "การจัดเรียง": layer_status
        })
        
    return pd.DataFrame(suggestions)