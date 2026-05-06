import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_beam_diagram(b, h, As_req, As_prime):
    fig, ax = plt.subplots(figsize=(5, 6))
    
    # วาดตัวคาน
    rect = patches.Rectangle((0, 0), b, h, linewidth=2, edgecolor='black', facecolor='whitesmoke')
    ax.add_patch(rect)
    
    covering = 3.0
    
    # เหล็กรับแรงดึง (ด้านล่าง)
    if As_req > 0:
        ax.plot([covering+1, b-covering-1], [covering, covering], 'bo', markersize=8)
        ax.text(b/2, covering+2, f"As = {As_req:.2f} sq.cm", ha='center', color='blue')
        
    # เหล็กรับแรงอัด (ด้านบน)
    if As_prime > 0:
        ax.plot([covering+1, b-covering-1], [h-covering, h-covering], 'ro', markersize=8)
        ax.text(b/2, h-covering-3, f"A's = {As_prime:.2f} sq.cm", ha='center', color='red')
        
    # เหล็กปลอก
    stirrup = patches.Rectangle((covering-1, covering-1), b-2*(covering-1), h-2*(covering-1), 
                                linewidth=1.5, edgecolor='green', facecolor='none', linestyle='--')
    ax.add_patch(stirrup)
    
    ax.set_xlim(-5, b + 5)
    ax.set_ylim(-5, h + 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig