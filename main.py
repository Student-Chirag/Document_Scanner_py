import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract


cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
count = 0
scale = 1
font = cv2.FONT_HERSHEY_SIMPLEX

WIDTH, HEIGHT = 800, 600
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

def image_preprocessing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    return threshold

def scan_detection(image):
    global document_contour

    document_contour =  np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])
    qray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(qray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)

            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area
    cv2.drawContours(image, [document_contour], -1, (0, 255, 0), 3)
                
def center_text(image, text):
    # font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 2, 5)[0]
    text_x = (image.shape[1] - text_size[0]) // 2
    text_y = (image.shape[0] + text_size[1]) // 2
    cv2.putText(image, text, (text_x, text_y), font, 2, (255, 0, 255), 5, cv2.LINE_AA)
    



while True:
    _, frame = cap.read()
    # frame = cv2.rotate(frame, cv2) 
    frame_copy = frame.copy()
    scan_detection(frame_copy)

    # cv2.imshow("input", frame)
    cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))


    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))
    # cv2.imshow("warped", warped)
    cv2.imshow("warped", cv2.resize(warped, (int(scale * warped.shape[1]), int(scale * warped.shape[0]))))

    processed = image_preprocessing(warped)
    processed = processed[10: processed.shape[0] - 10, 10: processed.shape[1] - 10]
    cv2.imshow("processed", cv2.resize(processed, (int(scale * processed.shape[1]), int(scale * processed.shape[0]))))

    # ocr_text = pytesseract.image_to_string(warped)

    # print(ocr_text)
    pressed_key = cv2.waitKey(1) & 0xFF
    if pressed_key == 27 :
        break

    elif pressed_key == ord('s'):
        cv2.imwrite("output/scanned_" + str(count) + ".jpg", processed)

        count += 1

        center_text(frame, "Scan Saved")
        cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))
        cv2.waitKey(500)

    elif pressed_key == ord('o'):
        file = open("output/recognized_" + str(count - 1) + ".txt", "w")
        ocr_text = pytesseract.image_to_string(warped)
        file.write(ocr_text)
        file.close()

        center_text(frame, "Text Saved")
        cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))
        cv2.waitKey(500)


cv2.destroyAllWindows()




####################################################
# import cv2
# import numpy as np
# from imutils.perspective import four_point_transform
# from imutils import contours

# def capture_image():
#     cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
#     WIDTH, HEIGHT = 800, 600
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         cv2.imshow("Capture Image", frame)
#         if cv2.waitKey(1) & 0xFF == ord('c'):
#             cv2.imwrite("captured_image.jpg", frame)
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return "captured_image.jpg"

# def process_image(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)
#     edged = cv2.Canny(gray, 75, 200)

#     cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

#     for c in cnts:
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.02 * peri, True)

#         if len(approx) == 4:
#             doc_cnt = approx
#             break

#     warped = four_point_transform(image, doc_cnt.reshape(4, 2))
#     cv2.imwrite("scanned_document.jpg", warped)
#     return "scanned_document.jpg"

# def main():
#     image_path = capture_image()
#     scanned_image_path = process_image(image_path)
#     print(f"Scanned document saved as {scanned_image_path}")

# if __name__ == "__main__":
#     main()

#################### Upload file
# import cv2
# import numpy as np
# from imutils.perspective import four_point_transform
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename

# def upload_image():
#     Tk().withdraw()  # Prevents the Tkinter window from appearing
#     file_path = askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
#     return file_path

# def process_image(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)
#     edged = cv2.Canny(gray, 50, 150)  # Adjusted parameters for edge detection

#     cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]  # Increased range of contours considered

#     doc_cnt = None
#     for c in cnts:
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.02 * peri, True)

#         if len(approx) == 4:
#             doc_cnt = approx
#             break

#     if doc_cnt is None:
#         print("No document contour detected.")
#         return None

#     warped = four_point_transform(image, doc_cnt.reshape(4, 2))
#     cv2.imwrite("scanned_document.jpg", warped)
#     return "scanned_document.jpg"

# def main():
#     image_path = upload_image()
#     if image_path:
#         scanned_image_path = process_image(image_path)
#         if scanned_image_path:
#             print(f"Scanned document saved as {scanned_image_path}")
#         else:
#             print("Failed to scan the document.")
#     else:
#         print("No image selected.")

# if __name__ == "__main__":
#     main()