import cv2
import numpy as np
import easyocr
from PIL import Image

class CaptchaEngine:
    def __init__(self):
        # Initializing the reader
        self.reader = easyocr.Reader(['en'], gpu=False)

    def solve(self, pil_image):
        # 1. --- Preprocessing (The pipeline we perfected) ---
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 145, 255, cv2.THRESH_BINARY_INV)

        nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, None, None, None, 8, cv2.CV_32S)
        clean_img = np.zeros(thresh.shape, dtype=np.uint8)
        for i in range(1, nlabels):
            if stats[i, cv2.CC_STAT_AREA] > 12 and stats[i, cv2.CC_STAT_HEIGHT] > 10: 
                clean_img[labels == i] = 255

        kernel_v = np.ones((3, 1), np.uint8)
        clean_img = cv2.dilate(clean_img, kernel_v, iterations=1)
        final_processed = cv2.bitwise_not(clean_img)

        # 2. --- OCR with Confidence ---
        # detail=1 gives us (bbox, text, confidence)
        results = self.reader.readtext(
            final_processed, 
            detail=1, 
            allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#'
        )

        final_text = ""
        low_confidence_threshold = 0.50  # 50% sure

        for (bbox, text, prob) in results:
            cleaned_chunk = text.replace(" ", "").upper()
            
            # --- Flexible Logic ---
            # If the AI is not sure about a character, we apply 'soft' rules
            if prob < low_confidence_threshold:
                # Example: If it's unsure about 'D', it's likely an 'O' in this font
                cleaned_chunk = cleaned_chunk.replace("D", "O").replace("0", "O")
                # Example: If it's unsure about 'R', check if it should be 'P'
                cleaned_chunk = cleaned_chunk.replace("R", "P")
            
            final_text += cleaned_chunk

        # Final sanity check: if the first char isn't # but the shape is small, add it
        # (This handles the case where the # is detected but not recognized as the symbol)
        if not final_text.startswith("#") and len(final_text) >= 5:
            # You can decide if you want to force the # based on game rules
            pass 

        print(f"DEBUG: Raw Detected: {final_text} (Avg Confidence: {sum([r[2] for r in results])/len(results) if results else 0:.2f})")
        return final_text