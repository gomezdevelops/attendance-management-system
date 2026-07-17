import cv2
import pickle
from datetime import datetime
from database.db import get_connection
import dlib
import numpy as np

# Load models once
detector = dlib.get_frontal_face_detector()

shape_predictor = dlib.shape_predictor(
    "models/shape_predictor_68_face_landmarks.dat"
)

face_rec_model = dlib.face_recognition_model_v1(
    "models/dlib_face_recognition_resnet_model_v1.dat"
)


def recognize_and_mark_attendance(subject_id):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    hour = now.hour


    cursor.execute("SELECT student_id FROM students")

    all_students = cursor.fetchall()

    for student in all_students:

        student_id = student[0]

        cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id = ?
        AND subject_id = ?
        AND date = ?
        AND hour = ?
        """, (
            student_id,
            subject_id,
            date,
            hour
        ))

        existing = cursor.fetchone()

        if not existing:

            cursor.execute("""
            INSERT INTO attendance
            (student_id, subject_id, date, hour, status)
            VALUES (?, ?, ?, ?, ?)
            """, (
                student_id,
                subject_id,
                date,
                hour,
                "Absent"
            ))

    conn.commit()

    print("All students initially marked as Absent")


    cursor.execute(
        "SELECT student_id, encoding_data FROM face_encodings"
    )

    records = cursor.fetchall()

    known_encodings = []
    student_ids = []

    for student_id, encoding_blob in records:
        try:
            encoding = pickle.loads(encoding_blob)
            known_encodings.append(encoding)
            student_ids.append(student_id)
        except:
            continue

    if len(known_encodings) == 0:
        print("No face encodings found in database")
        return

    video_capture = cv2.VideoCapture(1,cv2.CAP_DSHOW)

    print("Press 'q' to stop attendance")

    marked_students = set()

    while True:

        try:

            ret, frame = video_capture.read()

            if not ret:
                continue

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            rgb_frame = np.ascontiguousarray(
                rgb_frame,
                dtype=np.uint8
            )

            faces = detector(rgb_frame)

            for face_rect in faces:

                try:

                    shape = shape_predictor(
                        rgb_frame,
                        face_rect
                    )

                    face_descriptor = face_rec_model.compute_face_descriptor(
                        rgb_frame,
                        shape,
                        0,
                        0.25
                    )

                    face_encoding = np.array(
                        face_descriptor
                    )

                except Exception as e:

                    print("Encoding error:", e)
                    continue

                matches = []

                for known_encoding in known_encodings:

                    distance = np.linalg.norm(
                        known_encoding - face_encoding
                    )

                    if distance < 0.6:
                        matches.append(True)
                    else:
                        matches.append(False)

                if True in matches:

                    index = matches.index(True)

                    student_id = student_ids[index]

                    if student_id not in marked_students:

                        cursor.execute("""
                        UPDATE attendance
                        SET status = ?
                        WHERE student_id = ?
                        AND subject_id = ?
                        AND date = ?
                        AND hour = ?
                        """, (
                            "Present",
                            student_id,
                            subject_id,
                            date,
                            hour
                        ))

                        conn.commit()

                        print(
                            f"Attendance marked for {student_id}"
                        )

                        marked_students.add(
                            student_id
                        )

            cv2.imshow(
                "Attendance",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                print("Attendance stopped")

                break

        except Exception as e:

            print("Runtime error:", e)

            continue

    video_capture.release()

    cv2.destroyAllWindows()

    conn.close()