import pandas as pd
import math

def suggest_main_rebar(As_req, b, covering):
    if As_req <= 0:
        return None
        
    rebars = {"DB12": 1.13, "DB16": 2.01, "DB20": 3.14, "DB25": 4.91}
    options = []
    
    for name, area in rebars.items():
        n = math.ceil(As_req / area)
        if n < 2: n = 2 # บังคับอย่างน้อย 2 เส้นมุมคาน
        As_prov = n * area
        
        dia = int(name.replace("DB", "")) / 10
        space_needed = (2 * covering) + (2 * 0.9) + (n * dia) + ((n - 1) * max(2.5, dia))
        status = "✅ ผ่าน" if space_needed <= b else "⚠️ อาจแคบไป"
        
        options.append({
            "ขนาดเหล็ก": name,
            "จำนวนเส้น": n,
            "As ที่จัดให้ (sq.cm)": round(As_prov, 2),
            "หน้ากว้าง": status
        })
        
    return pd.DataFrame(options)