import os
import sys
from PIL import Image

# Add the project root to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.solver import CaptchaEngine

def run_debug_test():
    print("🔍 Initializing Captcha Engine for Testing...")
    solver = CaptchaEngine()
    
    img_dir = "img/"
    if not os.path.exists(img_dir):
        print(f"❌ Error: {img_dir} folder not found. Capture some images first!")
        return

    images = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg'))]
    
    if not images:
        print("📂 No images found in the img/ folder.")
        return

    print(f"✅ Found {len(images)} images. Starting OCR Analysis...\n")
    print(f"{'File Name':<25} | {'Detected Text':<15}")
    print("-" * 45)

    for img_name in images:
        path = os.path.join(img_dir, img_name)
        img = Image.open(path)
        
        # Solve using our production logic
        result = solver.solve(img)
        
        print(f"{img_name:<25} | {str(result):<15}")

if __name__ == "__main__":
    run_debug_test()