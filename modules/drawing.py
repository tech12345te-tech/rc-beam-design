import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_beam_diagram(inputs, As_req, As_prime, shear_details):
    b, h, covering = inputs['b'], inputs['h'], inputs['covering']
    d, d_prime = inputs['d'], inputs['d_prime']

    db = 1.6
    area_db = math.pi * (db**2) / 4
    num_tens = max(2, math.ceil(As_req / area_db))
    num_comp = max(2, math.ceil(As_prime / area_db)) if As_prime > 0 else 0

    fig, ax = plt.subplots(figsize=(6, 8))
    
    # วาดคอนกรีตและเหล็กปลอก
    ax.add_patch(patches.Rectangle((0, 0), b, h, fill=True, color='#f0f0f0', ec='black', lw=2))
    ax.add_patch(patches.Rectangle((covering, covering), b-2*covering, h-2*covering, fill=False, ec='red', ls='--', lw=2))

    # วาดเหล็กเมน
    x_start = covering + 0.9 + (db/2)
    x_end = b - x_start
    
    # เหล็กรับแรงดึง (ด้านล่าง)
    y_tens = h - d
    spacing_t = (x_end - x_start) / (num_tens - 1) if num_tens > 1 else 0
    for i in range(num_tens):
        ax.add_patch(plt.Circle((x_start + i * spacing_t, y_tens), db/2, color='blue'))

    # เหล็กรับแรงอัด (ด้านบน)
    if num_comp > 0:
        y_comp = h - d_prime
        spacing_c = (x_end - x_start) / (num_comp - 1) if num_comp > 1 else 0
        for i in range(num_comp):
            ax.add_patch(plt.Circle((x_start + i * spacing_c, y_comp), db/2, color='darkblue'))

    ax.set_xlim(-5, b + 5)
    ax.set_ylim(-10, h + 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig