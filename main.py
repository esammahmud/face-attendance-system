import cv2
import face_recognition
import datetime
import pandas as pd
df = pd.DataFrame(columns=["Name", "Date", "Time"])
df.to_excel("attendance.xlsx", index=False)

your_face_encoding = face_recognition.load_image_file("esam mahmud.jpg")
your_face_encoding = face_recognition.face_encodings(your_face_encoding)[0]

try:
    df = pd.read_excel("attendance.xlsx")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Name", "Date", "Time"])

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        continue

    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) > 0:
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([your_face_encoding], face_encoding)

            if match[0]:
                now = datetime.datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                df = df.append({"Name": "Your Name", "Date": now.date(), "Time": now.time()}, ignore_index=True)
                df.to_excel("attendance.xlsx", index=False)

    cv2.imshow("Face Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
