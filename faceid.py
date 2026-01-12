import cv2
import time
import os

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

FACE_TIME_REQUIRED = 2 
face_start_time = None
unlocked = False

print("📸 Նայիր տեսախցիկին...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        if face_start_time is None:
            face_start_time = time.time()

        elapsed = time.time() - face_start_time

        cv2.putText(
            frame,
            f"Scanning Face... {int(elapsed)}s",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        if elapsed >= FACE_TIME_REQUIRED:
            cv2.putText(
                frame,
                "FACE ID UNLOCKED",
                (40, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )
            unlocked = True
    else:
        face_start_time = None

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face ID Login", frame)

    if unlocked:
        time.sleep(1)
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 🔓 
if unlocked:
    print("🔓 Access granted. Opening app...")
    os.system('start chrome "https://github.com/"')