import cv2
image=cv2.imread("apple.jpg")
cv2.imshow("Apple Image", image)
cv2.waitKey(0)==27
cv2.destroyAllWindows()