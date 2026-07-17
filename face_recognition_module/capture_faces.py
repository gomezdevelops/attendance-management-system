import cv2
import pickle
import dlib
import numpy as np
from database.db import get_connection


def capture_face(student_id):

    print("DEBUG: About to capture face for", student_id)

    video_capture = cv2.VideoCapture(1,cv2.CAP_DSHOW)

    print("Press 'c' to capture face")
    print("Press 'q' to quit")

    # Load models ONCE (important)
    detector = dlib.get_frontal_face_detector()

    shape_predictor = dlib.shape_predictor(
        "models/shape_predictor_68_face_landmarks.dat"
    )

    face_rec_model = dlib.face_recognition_model_v1(
        "models/dlib_face_recognition_resnet_model_v1.dat"
    )

    while True:

        ret, frame = video_capture.read()

        if not ret:
            continue

        cv2.imshow("Capture Face", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):

            print("DEBUG: 'c' key pressed")

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            rgb_frame = np.ascontiguousarray(rgb_frame, dtype=np.uint8)

            try:

                faces = detector(rgb_frame)

                print("DEBUG: faces detected =", len(faces))

                if len(faces) == 0:
                    print("DEBUG: No face detected")
                    continue

                # Take first face
                face_rect = faces[0]

                # Get landmarks
                shape = shape_predictor(
                    rgb_frame,
                    face_rect
                )

                # Generate encoding
                face_descriptor = face_rec_model.compute_face_descriptor(
                    rgb_frame,
                    shape,
                    0
                )

                face_encoding = np.array(face_descriptor)

                print("DEBUG: face_encoding generated")

            except Exception as e:

                print("DEBUG: Encoding error:", e)
                continue

            # Serialize encoding
            encoding_data = pickle.dumps(face_encoding)

            print("DEBUG: encoding serialized")

            conn = get_connection()
            cursor = conn.cursor()

            try:

                cursor.execute("""
                INSERT INTO face_encodings
                (student_id, encoding_data)
                VALUES (?, ?)
                """, (
                    student_id,
                    encoding_data
                ))

                conn.commit()

                print("DEBUG: database insert committed")

            except Exception as e:

                print("DEBUG: database insert failed:", e)

            conn.close()

            print("Face captured and saved successfully")

            break

        if key == ord("q"):

            print("Capture cancelled")
            break

    video_capture.release()
    cv2.destroyAllWindows()