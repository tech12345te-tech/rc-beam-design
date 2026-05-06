import math

def design_shear(fc_prime, fyv, b, d, Vu):
    phi_v = 0.85
    Vc = 0.53 * math.sqrt(fc_prime) * b * d
    Vu_req = Vu / phi_v
    
    area_rb9 = math.pi * (0.9 ** 2) / 4
    Av = 2 * area_rb9
    
    details = {"Vc": Vc, "Vu_req": Vu_req, "Av": Av}
    
    if Vu_req <= Vc / 2:
        details.update({"Vs": 0, "s_final": 999, "status": "No stirrups required theoretically"})
        return 0, 0, "ไม่ต้องเสริมเหล็กปลอกตามทฤษฎี", details
        
    Vs = Vu_req - Vc
    Vs_max = 2.1 * math.sqrt(fc_prime) * b * d
    details.update({"Vs": Vs, "Vs_max": Vs_max})
    
    if Vs > Vs_max:
        return -1, 0, "❌ แรงเฉือนสูงเกินไป ต้องขยายหน้าตัดคาน!", details
        
    s_req1 = Av * fyv * d / Vs if Vs > 0 else 999
    s_max1 = d / 2 if Vs <= 1.06 * math.sqrt(fc_prime) * b * d else d / 4
    
    s_final = min(s_req1, s_max1, 60)
    s_final = math.floor(s_final / 5) * 5 # ปัดลงทีละ 5 ซม.
    
    details.update({"s_final": s_final})
    return Av, s_final, f"ใช้เหล็กปลอก RB9 @ {s_final:.0f} cm", details