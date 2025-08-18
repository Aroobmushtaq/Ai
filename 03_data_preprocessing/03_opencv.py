import cv2
image=cv2.imread("apple.jpg")
# Resize the image to 100x100 pixels and convert it to grayscale
resizeImage=cv2.resize(image,(100,100))
grayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.rectangle(image, (0,0), (50,50), (255,0,0),2)
cv2.circle(image, (100,110), 50, (255,255,255), -1)
cv2.line(image, (150,150), (400,400), (0,255,0), 5)
edges = cv2.Canny(image, 100, 200)
cv2.imshow("Apple Image", edges)
# Save the resized and grayscale image
# cv2.imwrite("apple_gray.jpg", grayImage)
cv2.waitKey(0)==27
cv2.destroyAllWindows()


# OpenCV for image processing
# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam Feed", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

