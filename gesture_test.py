import cv2
import mediapipe as mp


# ============================================================
# MediaPipe setup
# ============================================================

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = "models/gesture_recognizer.task"


# ============================================================
# Gesture recognizer
# ============================================================

options = GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

recognizer = GestureRecognizer.create_from_options(
    options
)


# ============================================================
# Camera
# ============================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Could not open the camera.")


timestamp_ms = 0


# ============================================================
# Main loop
# ============================================================

while True:

    success, frame = camera.read()

    if not success:
        print("Could not read camera frame.")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # OpenCV BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms += 33

    # Recognize gestures
    result = recognizer.recognize_for_video(
        mp_image,
        timestamp_ms
    )

    # --------------------------------------------------------
    # Display detected gesture
    # --------------------------------------------------------

    gesture_text = "No gesture"

    if result.gestures:

        top_gesture = result.gestures[0][0]

        if top_gesture.category_name != "None":

            gesture_text = (
                f"{top_gesture.category_name} "
                f"({top_gesture.score:.2f})"
            )

    cv2.putText(
        frame,
        f"Gesture: {gesture_text}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 150),
        2
    )

    # Show the camera
    cv2.imshow(
        "APEX AI - Gesture Test",
        frame
    )

    # ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ============================================================
# Cleanup
# ============================================================


recognizer.close()
camera.release()
cv2.destroyAllWindows()
