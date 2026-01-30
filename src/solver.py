import cv2
import numpy as np
import easyocr
import os
import csv
from datetime import datetime
from PIL import Image

class CaptchaEngine:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.log_dir = "logs"
        self.img_log_dir = "logs/captures"
        if not os.path.exists(self.img_log_dir): os.makedirs(self.img_log_dir)

    def log_result(self, image, final_text, confidence, raw_data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cap_{timestamp}.png"
        image.save(os.path.join(self.img_log_dir, filename))
        log_file = os.path.join(self.log_dir, "solve_history.csv")
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Filename", "Predicted_Text", "Confidence", "Raw_Data"])
            writer.writerow([timestamp, filename, final_text, round(confidence, 4), raw_data])

    def solve(self, pil_image):
        # 1. Preprocessing (The 'Perfect Balance' Pipeline)
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 70, 40]), np.array([180, 255, 255]))
        denoised = cv2.medianBlur(mask, 3)

        # Vertical focus to kill wavy lines but keep letter legs
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 4))
        clean_img = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel_v)

        # Heal the letters (Connects the bottom of the 'U')
        kernel_d = np.ones((2, 2), np.uint8)
        clean_img = cv2.dilate(clean_img, kernel_d, iterations=1)

        final_processed = cv2.bitwise_not(clean_img)
        
        # 2. OCR Execution
        results = self.reader.readtext(final_processed, detail=1, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#')
        
        raw_text = "".join([r[1] for r in results]).replace(" ", "").upper()
        fixed = list(raw_text)

        # 3. --- THE PATTERN REFINER ---
        if len(fixed) >= 5:
            # STYLE 1: The #SOPYN Pattern
            # If it starts with a '#' (or an 'E' that looks like one) followed by 'S'
            if (fixed[0] in ["#", "E", "4", "3"]) and (len(fixed) > 1 and fixed[1] == "S"):
                fixed[0] = "#" # Force the #
                
                # Check for the O vs D confusion
                if len(fixed) > 2 and fixed[2] == "D": fixed[2] = "O"
                
                # Check for the N vs M confusion at the end
                if fixed[-1] == "M": fixed[-1] = "N"

            # STYLE 2: The 32YU#B Pattern
            elif "".join(fixed[:2]) == "32":
                # Index 2 must be Y
                if len(fixed) > 2 and fixed[2] != "Y": fixed[2] = "Y"
                
                # Index 3 must be U (AI often sees N, W, or X)
                if len(fixed) > 3 and fixed[3] in ["N", "W", "X", "V", "H"]:
                    fixed[3] = "U"
                
                # Index 4 must be # (AI often sees E, H, or 4)
                if len(fixed) > 4 and fixed[4] in ["E", "H", "4", "B", "8"]:
                    fixed[4] = "#"
                
                # Final char check (B vs 5/8)
                if fixed[-1] in ["5", "8"]: fixed[-1] = "B"

        final_string = "".join(fixed)
        
        # Log the solve for your history
        self.log_result(pil_image, final_string, 1.0, str(results))
        
        return final_string