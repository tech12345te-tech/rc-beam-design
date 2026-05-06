import math
import pandas as pd

def suggest_main_rebar(As_req, b, covering=3.0, stirrup_db=0.9):
    if As_req <= 0: return None
    
    rebar_db = {"DB12": 1.13, "DB16": 2.01, "DB20": 3.14, "DB25": 4.91, "DB28": 6.16}
    suggestions = []
    
    for name, area in rebar_db.items():
        num_bars = max(2, math.ceil(As_req / area))
        As_provided = num_bars * area
        db_cm = math.sqrt((area * 4) / math.pi)
        clear_spacing = max(2.5, db_cm)
        avail_width = b - (2 * covering) - (2 * stirrup_db)
        req_width = (num_bars * db_cm) + ((num_bars - 1) * clear_spacing)
        
        status = "✅ 1 ชั้น" if req_width <= avail_width else "⚠️ 2 ชั้น"
        suggestions.append({
            "เหล็ก": name, "จำนวน": num_bars, "รูปแบบ": f"{num_bars}-{name}",
            "พื้นที่ (sq.cm)": round(As_provided, 2), "การจัดเรียง": status
        })
    return pd.DataFrame(suggestions)