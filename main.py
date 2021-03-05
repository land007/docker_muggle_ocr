import time
# STEP 1
import muggle_ocr
import os
# STEP 2
#sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
root_dir = r"./imgs"
for i in os.listdir(root_dir):
    n = os.path.join(root_dir, i)
    with open(n, "rb") as f:
        b = f.read()
    st = time.time()
    # STEP 3
    text = sdk.predict(image_bytes=b)
    print(i, text, time.time() - st)