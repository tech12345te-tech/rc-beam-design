import math
from modules.material import calculate_beta1

def design_flexure(fc_prime, fy, b, d, d_prime, Mu):
    """ออกแบบเหล็กเสริมรับแรงดัด (Singly / Doubly)"""
    Mu_kg_cm = Mu * 100
    phi = 0.90
    beta1 = calculate_beta1(fc_prime)
    
    rho_b = 0.85 * beta1 * (fc_prime / fy) * (6120 / (6120 + fy))
    rho_max = 0.75 * rho_b
    
    Rn_max = rho_max * fy * (1 - 0.59 * rho_max * fy / fc_prime)
    Mu_max = phi * Rn_max * b * (d ** 2)
    
    rho_min = max(14 / fy, 0.8 * math.sqrt(fc_prime) / fy)
    As_min = rho_min * b * d

    details = {
        "beta1": beta1, "rho_b": rho_b, "rho_max": rho_max, 
        "Rn_max": Rn_max, "Mu_max": Mu_max / 100, "As_min": As_min
    }

    if Mu_kg_cm <= Mu_max:
        Rn = Mu_kg_cm / (phi * b * (d ** 2))
        try:
            rho_req = (0.85 * fc_prime / fy) * (1 - math.sqrt(1 - (2 * Rn / (0.85 * fc_prime))))
        except ValueError:
            rho_req = rho_max
            
        As_req = max(rho_req * b * d, As_min)
        details.update({"type": "Singly", "Rn": Rn, "rho_req": rho_req})
        return "Singly", As_req, 0.0, "หน้าตัดรับโมเมนต์ได้ (เหล็กเสริมเดี่ยว)", details
    else:
        Mu1 = Mu_max
        Mu2 = Mu_kg_cm - Mu1
        As1 = rho_max * b * d
        
        c = rho_max * fy * d / (0.85 * beta1 * fc_prime)
        fs_prime = 6120 * (c - d_prime) / c
        
        yield_status = "Yield" if fs_prime >= fy else "Not Yield"
        if fs_prime >= fy: fs_prime = fy
            
        As2 = Mu2 / (phi * fs_prime * (d - d_prime))
        As_req = As1 + As2
        
        details.update({"type": "Doubly", "Mu1": Mu1/100, "Mu2": Mu2/100, "As1": As1, "c": c, "fs_prime": fs_prime, "yield_status": yield_status, "As2": As2})
        return "Doubly", As_req, As2, f"ต้องเสริมเหล็กคู่ (เหล็กรับแรงอัด {yield_status})", details