def design_flexure(fc_prime, fy, b, d, d_prime, Mu):
    Mu_kg_cm = Mu * 100
    beta1 = 0.85 if fc_prime <= 280 else max(0.65, 0.85 - 0.05 * ((fc_prime - 280) / 70))
    phi = 0.90
    
    rho_min = max(14 / fy, 0.8 * (fc_prime**0.5) / fy)
    rho_b = (0.85 * beta1 * fc_prime / fy) * (6120 / (6120 + fy))
    rho_max = 0.75 * rho_b
    
    Rn = Mu_kg_cm / (phi * b * d**2)
    m = fy / (0.85 * fc_prime)
    
    try:
        rho_req = (1 / m) * (1 - (1 - 2 * m * Rn / fy)**0.5)
    except ValueError:
        rho_req = rho_max + 0.01 
        
    details = {}
    
    if rho_req <= rho_max:
        As_req = max(rho_req * b * d, rho_min * b * d)
        details.update({"type": "Singly", "Rn": Rn, "rho_req": rho_req})
        return "Singly", As_req, 0.0, "หน้าตัดรับโมเมนต์ได้ (เหล็กเสริมเดี่ยว)", details
    else:
        Mu1 = phi * rho_max * fy * b * d**2 * (1 - 0.59 * rho_max * fy / fc_prime)
        Mu2 = Mu_kg_cm - Mu1
        As1 = rho_max * b * d
        
        c = rho_max * fy * d / (0.85 * beta1 * fc_prime)
        fs_prime = 6120 * (c - d_prime) / c
        
        yield_status = "Yield" if fs_prime >= fy else "Not Yield"
        if fs_prime >= fy:
            fs_prime = fy
            
        As2 = Mu2 / (phi * fs_prime * (d - d_prime))
        As_req = As1 + As2
        
        details.update({"type": "Doubly", "Mu1": Mu1/100, "Mu2": Mu2/100, "As1": As1, "c": c, "fs_prime": fs_prime, "yield_status": yield_status})
        return "Doubly", As_req, As2, f"ต้องเสริมเหล็กคู่ (เหล็กรับแรงอัด {yield_status})", details