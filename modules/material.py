def calculate_beta1(fc_prime):
    """คำนวณค่าสัมประสิทธิ์ beta1 ของคอนกรีต"""
    if fc_prime <= 280:
        return 0.85
    else:
        beta1 = 0.85 - 0.05 * ((fc_prime - 280) / 70)
        return max(0.65, beta1)