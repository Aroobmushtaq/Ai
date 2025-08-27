# import cv2
# image=cv2.imread("apple.jpg")
# # Resize the image to 100x100 pixels and convert it to grayscale
# resizeImage=cv2.resize(image,(100,100))
# grayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.rectangle(image, (0,0), (50,50), (255,0,0),2)
# cv2.circle(image, (100,110), 50, (255,255,255), -1)
# cv2.line(image, (150,150), (400,400), (0,255,0), 5)
# edges = cv2.Canny(image, 100, 200)
# cv2.imshow("Apple Image", edges)
# # Save the resized and grayscale image
# # cv2.imwrite("apple_gray.jpg", grayImage)
# cv2.waitKey(0)==27
# cv2.destroyAllWindows()


# # OpenCV for image processing
# # Open webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     cv2.imshow("Webcam Feed", frame)
    
#     # Press 'q' to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import numpy as np

# Webcam
cap = cv2.VideoCapture(0)

# Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Blank canvas
canvas = None

# Brush settings
brush_color = (255, 0, 0)  # Blue
brush_size = 8

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Detect hands
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, c = frame.shape
            x = int(handLms.landmark[8].x * w)  # Index fingertip (landmark 8)
            y = int(handLms.landmark[8].y * h)

            # Draw circle at fingertip
            cv2.circle(frame, (x, y), 10, brush_color, -1)

            # Paint on canvas
            cv2.circle(canvas, (x, y), brush_size, brush_color, -1)

            # Draw hand skeleton (optional)
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    # Combine camera feed + canvas
    combined = cv2.addWeighted(frame, 1, canvas, 0.7, 0)

    cv2.imshow("Air Paint 🎨", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("c"):   # Clear screen
        canvas = None
    elif key == ord("r"): # Red color
        brush_color = (0, 0, 255)
    elif key == ord("g"): # Green color
        brush_color = (0, 255, 0)
    elif key == ord("b"): # Blue color
        brush_color = (255, 0, 0)
    elif key == ord("e"): # Eraser
        brush_color = (0, 0, 0)
    elif key == 27:       # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
