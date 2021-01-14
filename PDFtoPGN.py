import cv2
import psutil
import tempfile
import pytesseract
import numpy as np
from tqdm import tqdm
from pdf2image import convert_from_path


def preprocess(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    #img = cv2.erode(img, np.ones((5, 5), np.uint8), iterations=5)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img


if __name__ == '__main__':
    book = ''
    print(pytesseract.get_languages(config=''))
    custom_config = r' -l eng'
    with tempfile.TemporaryDirectory() as path:
        pages = convert_from_path("test.pdf", dpi=500, output_folder=path,
                                  thread_count=psutil.cpu_count(), fmt="png")
        for page in tqdm(pages):
            page = preprocess(page)

            try:
                book += pytesseract.image_to_string(page, timeout=0,  config=custom_config)
                print(pytesseract.image_to_string(page, timeout=0,  config=custom_config))
                print()
            except RuntimeError as timeout_error:
                pass
        with open("Output.txt", "w") as text_file:
            text_file.write(book)
