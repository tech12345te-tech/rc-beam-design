import math

def design_shear(fc_prime, fyv, b, d, Vu):
    """ออกแบบเหล็กเสริมรับแรงเฉือน (เหล็กปลอก)"""
    phi_v = 0.85
    Vc = 0.53 * math.sqrt(fc_prime) * b * d
    Vu_req = Vu / phi_v
    
    area_rb9 = math.pi * (0.9 ** 2) / 4
    Av = 2 * area_rb9
    
    details = {"Vc": Vc, "Vu_req": Vu_req, "Av": Av}

    if Vu_req <= Vc / 2:
        details.update({"Vs": 0, "s_final": 999, "status": "No stirrups required theoretically"})
        return 0, 0, "ไม่ต้องการเหล็กปลอกตามทฤษฎี", details
    
    Vs = Vu_req - Vc
    Vs_max = 2.1 * math.sqrt(fc_prime) * b * d
    details.update({"Vs": Vs, "Vs_max": Vs_max})
    
    if Vs > Vs_max:
        return -1, 0, "❌ แรงเฉือนสูงเกินไป ต้องขยายหน้าตัดคาน!", details
    
    s_req = (Av * fyv * d) / Vs if Vs > 0 else 999
    
    if Vs > 1.06 * math.sqrt(fc_prime) * b * d:
        s_max_code = min(d / 4, 30.0)
    else:
        s_max_code = min(d / 2, 60.0)
        
    s_min_code = (Av * fyv) / (3.5 * b)
    s_max = min(s_max_code, s_min_code)
    s_final = min(s_req, s_max)
    s_practise = max(math.floor(s_final / 5) * 5, 5)
    
    details.update({"s_req": s_req, "s_max": s_max, "s_practise": s_practise})
    return Av, s_practise, f"ใช้เหล็กปลอก RB9 @ {s_practise} ซม.", details