import cv2
import tkinter as tk
import speech_recognition as sr
import mediapipe as mp
import qrcode 


from share_server import ShareServer
from portrait_engine import PortraitEngine


from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime
from threading import Thread
from queue import Queue, Empty

from apex_core import ApexCore


class ApexAI:
    
    def share_portrait(self):

        if not self.last_ai_path:

            self.status.config(
            text="APEX AI • NO PORTRAIT TO SHARE"
            )

            return

        ai_path = Path(
            self.last_ai_path
        )

        if not ai_path.exists():

            self.status.config(
                text="APEX AI • PORTRAIT NOT FOUND"
            )

            return

        try:

            # Stop any previous sharing server.
            if self.share_server:

                self.share_server.stop()

            # Start a new server.
            self.share_server = ShareServer()

            url = self.share_server.start(
                ai_path
            )

            print(
                f"[APEX SHARE] {url}"
            )

        # -----------------------------------------------------
        # Generate QR
        # -----------------------------------------------------

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4
            )

            qr.add_data(url)
            qr.make(fit=True)

            qr_image = qr.make_image(
                fill_color="black",
                back_color="white"
            )

            qr_path = (
                self.output_dir /
                "APEX_SHARE_QR.png"
            )

            qr_image.save(qr_path)  

            # Show QR window.
            self.show_share_qr(
                qr_path,
                url
            )

        except Exception as error:

            print(
                f"[APEX SHARE ERROR] {error}"
            )

            self.status.config(
                text="APEX AI • SHARE FAILED"
            )
            
    def show_share_qr(self,qr_path,url):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "APEX AI • Share Portrait"
        )

        window.geometry(
            "500x650"
        )

        window.configure(
            bg="#101820"
        )

    # ---------------------------------------------------------
    # Heading
    # ---------------------------------------------------------

        tk.Label(
            window,
            text="YOUR PORTRAIT IS READY!",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#101820"
        ).pack(
            pady=20
        )

        tk.Label(
            window,
            text="Scan this QR code with your phone",
            font=("Arial", 12),
            fg="#8fd3ff",
            bg="#101820"
        ).pack(
            pady=5
        )

    # ---------------------------------------------------------
    # QR image
    # ---------------------------------------------------------

        qr_image = Image.open(
            qr_path
        )

        qr_image.thumbnail(
            (350, 350),
            Image.Resampling.LANCZOS
        )

        qr_photo = ImageTk.PhotoImage(
            qr_image
        )

        qr_label = tk.Label(
            window,
            image=qr_photo,
            bg="white"
        )

        qr_label.pack(
            pady=20
        )

        qr_label.image = qr_photo

    # ---------------------------------------------------------
    # URL
    # ---------------------------------------------------------

        tk.Label(
            window,
            text=url,
            font=("Arial", 8),
            fg="white",
            bg="#101820",
            wraplength=420
        ).pack(
            pady=5
        )

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

        tk.Button(
            window,
            text="CLOSE",
            command=window.destroy,
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#1c2b36",
            fg="white",
            relief="flat"
        ).pack(
            pady=15
        )

        self.status.config(
            text="APEX AI • READY TO SHARE"
        )
        
        tk.Button(
            window,
            text="SHARE",
            command=self.share_portrait,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#1c2b36",
            fg="white",
            relief="flat"
        ).pack(
            side="left",
            padx=10
        )
    
    
    def show_processing_screen(self):

        self.camera_label.config(
            image=""
        )

        self.camera_label.image = None

        self.status.config(
            text="APEX AI • CREATING YOUR PORTRAIT..."
        )

        self.camera_label.config(
            text="🧠\n\nAPEX AI IS CREATING\nYOUR PORTRAIT...",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#101820",
            justify="center"
        )
    
    
    def start_ai_portrait(self):

        if self.portrait_engine is None:

            self.status.config(
                text="APEX AI • PORTRAIT ENGINE UNAVAILABLE"
            )

            return

        self.status.config(
            text="APEX AI • CAPTURING..."
        )

        success, frame = self.camera.read()

        if not success:

            self.status.config(
                text="APEX AI • CAPTURE FAILED"
            )

            return

        frame = cv2.flip(frame, 1)

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        input_path = (
            self.output_dir /
            f"APEX_ORIGINAL_{timestamp}.jpg"
        )

        output_path = (
            self.output_dir /
            f"APEX_AI_{timestamp}.png"
        )

        cv2.imwrite(
            str(input_path),
            frame
        )

        self.last_original_path = input_path
        self.last_ai_path = output_path

        # Stop the normal mirror display while AI is processing.
        self.result_mode = True

        self.show_processing_screen()

        thread = Thread(
            target=self.generate_ai_portrait,
            args=(input_path, output_path),
            daemon=True
        )

        thread.start()
    
    def generate_ai_portrait(
        self,
        input_path,
        output_path
    ):  
        try:

            result_path = (
                self.portrait_engine.generate(
                    input_path,
                    output_path
                )
            )

            # Return to Tkinter's main thread.
            self.root.after(
                0,
                lambda: self.show_ai_result(result_path)
            )

        except Exception as error:
            print(
                f"[APEX AI ERROR] {error}"
            )

            self.root.after(
                0,
                lambda: self.status.config(
                    text="APEX AI • GENERATION FAILED"
                )
            )
    
    def show_ai_result(self, result_path):

        result_path = Path(result_path)

        if not result_path.exists():

            self.result_mode = False

            self.status.config(
                text="APEX AI • RESULT NOT FOUND"
            )

            return

        self.show_result_screen(
            self.last_original_path,
            result_path
        )
    
    def show_result_screen(
        self,
        original_path,
        ai_path
    ):

        # Clear camera display
        self.camera_label.config(
            image="",
            text=""
        )

        self.camera_label.image = None

        # ---------------------------------------------------------
        # Result container
        # ---------------------------------------------------------

        result_frame = tk.Frame(
            self.root,
            bg="#101820"
        )

        result_frame.place(
            relx=0.5,
            rely=0.48,
            anchor="center",
            relwidth=0.92,
            relheight=0.72
        )

        self.result_frame = result_frame

        # ---------------------------------------------------------
        # Headings
        # ---------------------------------------------------------

        original_title = tk.Label(
            result_frame,
            text="ORIGINAL",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#101820"
        )

        original_title.grid(
            row=0,
            column=0,
            pady=10
        )

        ai_title = tk.Label(
            result_frame,
            text="APEX AI PORTRAIT",
            font=("Arial", 15, "bold"),
            fg="#65ff9a",
            bg="#101820"
        )

        ai_title.grid(
            row=0,
            column=1,
            pady=10
        )

        # ---------------------------------------------------------
        # Original image
        # ---------------------------------------------------------

        original_image = Image.open(
            original_path
        )

        original_image.thumbnail(
            (450, 450),
            Image.Resampling.LANCZOS
        )

        original_photo = ImageTk.PhotoImage(
            original_image
        )

        original_label = tk.Label(
            result_frame,
            image=original_photo,
            bg="black"
        )

        original_label.grid(
            row=1,
            column=0,
            padx=20
        )

        original_label.image = original_photo

        # ---------------------------------------------------------
        # AI image
        # ---------------------------------------------------------

        ai_image = Image.open(
            ai_path
        )

        ai_image.thumbnail(
            (450, 450),
            Image.Resampling.LANCZOS
        )

        ai_photo = ImageTk.PhotoImage(
            ai_image
        )

        ai_label = tk.Label(
            result_frame,
            image=ai_photo,
            bg="black"
        )

        ai_label.grid(
            row=1,
            column=1,
            padx=20
        )

        ai_label.image = ai_photo

    # ---------------------------------------------------------
    # Buttons
    # ---------------------------------------------------------

        button_frame = tk.Frame(
            result_frame,
            bg="#101820"
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=25
        )

        tk.Button(
            button_frame,
            text="RETAKE",
            command=self.retake_portrait,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#1c2b36",
            fg="white",
            relief="flat"
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            button_frame,
            text="SHARE",
            command=self.share_portrait,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#1c2b36",
            fg="white",
            relief="flat"
        ).pack(
            side="left",
            padx=10
        )

        self.status.config(
            text="APEX AI • PORTRAIT READY!"
        )
    
    def retake_portrait(self):

        if hasattr(self, "result_frame"):
            self.result_frame.destroy()

        self.result_mode = False
        self.status.config(text="APEX AI • LIVE")

        self.update_camera()

    def __init__(self, root):
        
        
        self.portrait_engine = None
        
        try:
            self.portrait_engine = PortraitEngine()
            print("[APEX] AI Portrait Engine ready.")
        except Exception as error:
            print(f"[APEX] Portrait engine unavailable: {error}")
            
        self.share_server = None

        self.root = root
        
        

        self.root.title(
            "APEX AI - Interactive Smart Mirror"
        )

        self.root.geometry(
            "1200x800"
        )

        self.root.configure(
            bg="#101820"
        )

        self.running = True

        # =====================================================
        # CAMERA
        # =====================================================

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            raise RuntimeError(
                "Could not access the camera."
            )

        # =====================================================
        # MODE
        # =====================================================

        self.mode = "normal"
        self.result_mode = False
        self.last_original_path = None
        self.last_ai_path = None

        # =====================================================
        # FACE DETECTION
        # =====================================================

        cascade_path = (
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        self.face_detector = (
            cv2.CascadeClassifier(cascade_path)
        )

        # =====================================================
        # OUTPUT
        # =====================================================

        self.output_dir = Path("output")

        self.output_dir.mkdir(
            exist_ok=True
        )

        # =====================================================
        # VOICE
        # =====================================================

        self.recognizer = sr.Recognizer()

        self.voice_queue = Queue()

        self.listening = False

        # =====================================================
        # GESTURE RECOGNIZER
        # =====================================================

        self.gesture_recognizer = None

        self.gesture_timestamp = 0

        self.frame_counter = 0

        self.last_gesture = None

        self.last_gesture_time = 0

        self.setup_gesture_recognizer()

        # =====================================================
        # APEX CORE
        # =====================================================

        self.apex_core = ApexCore(
            self.execute_action
        )

        # =====================================================
        # UI
        # =====================================================

        self.create_ui()

        # =====================================================
        # START SYSTEM
        # =====================================================

        self.update_camera()

        self.process_voice_queue()

    # =========================================================
    # GESTURE SETUP
    # =========================================================

    def setup_gesture_recognizer(self):

        model_path = (
            Path(__file__).parent /
            "models" /
            "gesture_recognizer.task"
        )

        if not model_path.exists():

            print(
                "[APEX] Gesture model not found."
            )

            return

        BaseOptions = mp.tasks.BaseOptions

        GestureRecognizer = (
            mp.tasks.vision.GestureRecognizer
        )

        GestureRecognizerOptions = (
            mp.tasks.vision.GestureRecognizerOptions
        )

        VisionRunningMode = (
            mp.tasks.vision.RunningMode
        )

        options = GestureRecognizerOptions(

            base_options=BaseOptions(
                model_asset_path=str(model_path)
            ),

            running_mode=VisionRunningMode.VIDEO,

            num_hands=1,

            min_hand_detection_confidence=0.5,

            min_hand_presence_confidence=0.5,

            min_tracking_confidence=0.5
        )

        self.gesture_recognizer = (
            GestureRecognizer.create_from_options(
                options
            )
        )

        print(
            "[APEX] Gesture engine ready."
        )

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="APEX AI",
            font=("Arial", 30, "bold"),
            fg="white",
            bg="#101820"
        )

        title.pack(
            pady=10
        )

        subtitle = tk.Label(
            self.root,
            text="INTERACTIVE SMART MIRROR",
            font=("Arial", 12),
            fg="#8fd3ff",
            bg="#101820"
        )

        subtitle.pack()

        self.camera_label = tk.Label(
            self.root,
            bg="black"
        )

        self.camera_label.pack(
            padx=20,
            pady=15,
            expand=True
        )

        self.status = tk.Label(
            self.root,
            text="APEX AI • LIVE",
            font=("Arial", 13, "bold"),
            fg="#65ff9a",
            bg="#101820"
        )

        self.status.pack(
            pady=5
        )

        controls = tk.Frame(
            self.root,
            bg="#101820"
        )

        controls.pack(
            pady=15
        )

        self.create_button(
            controls,
            "NORMAL",
            lambda: self.apex_core.process(
                "normal"
            )
        )

        self.create_button(
            controls,
            "SKETCH",
            lambda: self.apex_core.process(
                "sketch"
            )
        )

        self.create_button(
            controls,
            "CARTOON",
            lambda: self.apex_core.process(
                "cartoon"
            )
        )

        self.create_button(
            controls,
            "CAPTURE",
            lambda: self.apex_core.process(
                "capture"
            )
        )

        self.voice_button = self.create_button(
            controls,
            "VOICE",
            self.start_voice
        )

        self.create_button(
            controls,
            "EXIT",
            self.close
        )

    def create_button(
        self,
        parent,
        text,
        command
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=12,
            height=2,
            font=("Arial", 10, "bold"),
            bg="#1c2b36",
            fg="white",
            relief="flat",
            cursor="hand2"
        )

        button.pack(
            side="left",
            padx=6
        )

        return button

    # =========================================================
    # EXECUTE APEX ACTION
    # =========================================================

    def execute_action(self, action):
        
        

        print(
            f"[APEX ACTION] {action}"
        )

        # -----------------------------------------------------
        # NORMAL
        # -----------------------------------------------------

        if action == "normal":

            self.mode = "normal"

            self.status.config(
                text="APEX AI • NORMAL MIRROR"
            )
            


        # -----------------------------------------------------
        # SKETCH
        # -----------------------------------------------------

        elif action == "sketch":

            self.mode = "sketch"

            self.status.config(
                text="APEX AI • SKETCH MODE"
            )

        # -----------------------------------------------------
        # CARTOON
        # -----------------------------------------------------

        elif action == "cartoon":

            self.mode = "cartoon"

            self.status.config(
                text="APEX AI • CARTOON MODE"
            )

        # -----------------------------------------------------
        # CAPTURE
        # -----------------------------------------------------

        elif action == "capture":

            self.capture_image()
            
        elif action == "ai_portrait":

            self.start_ai_portrait()
            
        elif action == "share":
            self.share_portrait()

        # -----------------------------------------------------
        # YOUTUBE
        # -----------------------------------------------------

        elif action == "youtube":

            self.status.config(
                text="APEX AI • YOUTUBE OPENED"
            )

        # -----------------------------------------------------
        # GOOGLE
        # -----------------------------------------------------

        elif action == "google":

            self.status.config(
                text="APEX AI • GOOGLE OPENED"
            )

        # -----------------------------------------------------
        # MUSIC
        # -----------------------------------------------------

        elif action == "music":

            self.status.config(
                text="APEX AI • MUSIC"
            )

        # -----------------------------------------------------
        # SETTINGS
        # -----------------------------------------------------

        elif action == "settings":

            self.status.config(
                text="APEX AI • SETTINGS OPENED"
            )

        # -----------------------------------------------------
        # UNKNOWN
        # -----------------------------------------------------

        elif action.startswith("unknown:"):

            command = action[
                len("unknown:"):
            ]

            self.status.config(
                text=f"HEARD: {command}"
            )
        
    # =========================================================
    # IMAGE EFFECTS
    # =========================================================

    def apply_effect(self, frame):

        if self.mode == "normal":

            return frame

        if self.mode == "sketch":

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            inverted = cv2.bitwise_not(
                gray
            )

            blurred = cv2.GaussianBlur(
                inverted,
                (21, 21),
                0
            )

            sketch = cv2.divide(
                gray,
                255 - blurred,
                scale=256
            )

            return cv2.cvtColor(
                sketch,
                cv2.COLOR_GRAY2BGR
            )

        if self.mode == "cartoon":

            smooth = cv2.bilateralFilter(
                frame,
                9,
                75,
                75
            )

            gray = cv2.cvtColor(
                smooth,
                cv2.COLOR_BGR2GRAY
            )

            edges = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9,
                2
            )

            edges = cv2.cvtColor(
                edges,
                cv2.COLOR_GRAY2BGR
            )

            return cv2.bitwise_and(
                smooth,
                edges
            )

        return frame

    # =========================================================
    # GESTURE PROCESSING
    # =========================================================

    def process_gesture(self, frame):

        if self.gesture_recognizer is None:
            return None

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        self.gesture_timestamp += 33

        result = (
            self.gesture_recognizer
            .recognize_for_video(
                mp_image,
                self.gesture_timestamp
            )
        )

        if not result.gestures:
            return None

        gesture = result.gestures[0][0]

        if gesture.category_name == "None":
            return None

        return gesture.category_name

    # =========================================================
    # GESTURE → COMMAND
    # =========================================================

    def handle_gesture(self, gesture):

        import time

        current_time = time.time()

        # Prevent repeated commands
        # from one held gesture.

        if (
            gesture == self.last_gesture
            and current_time - self.last_gesture_time < 1.5
        ):

            return

        self.last_gesture = gesture

        self.last_gesture_time = current_time

        print(
            f"[APEX GESTURE] {gesture}"
        )

        # -----------------------------------------------------
        # GESTURE MAP
        # -----------------------------------------------------

        if gesture == "Thumb_Up":

            self.apex_core.process(
            "ai portrait"
        )

        elif gesture == "Victory":

            self.apex_core.process(
                "sketch"
            )

        elif gesture == "Closed_Fist":

            self.apex_core.process(
                "cartoon"
            )

        elif gesture == "Open_Palm":

            self.apex_core.process(
                "normal"
            )

    # =========================================================
    # CAMERA
    # =========================================================

    def update_camera(self):
        
        if self.result_mode:
            return

        if not self.running:
            return

        success, frame = self.camera.read()

        if not success:

            self.status.config(
                text="CAMERA ERROR"
            )

            self.root.after(
                100,
                self.update_camera
            )

            return

        frame = cv2.flip(
            frame,
            1
        )

        # -----------------------------------------------------
        # FACE DETECTION
        # -----------------------------------------------------

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 150),
                2
            )

            cv2.putText(
                frame,
                "FACE DETECTED",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 150),
                2
            )

        # -----------------------------------------------------
        # GESTURE
        # -----------------------------------------------------

        self.frame_counter += 1

        # Process every 3rd frame to reduce load
        if self.frame_counter % 3 == 0:

            gesture = self.process_gesture(
                frame
            )

            if gesture:

                cv2.putText(
                    frame,
                    f"Gesture: {gesture}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )

                self.handle_gesture(
                    gesture
                )

        # -----------------------------------------------------
        # VISUAL EFFECT
        # -----------------------------------------------------

        processed = self.apply_effect(
            frame
        )

        rgb = cv2.cvtColor(
            processed,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(
            rgb
        )

        image.thumbnail(
            (1100, 600),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(
            image
        )

        self.camera_label.config(
            image=photo
        )

        self.camera_label.image = photo

        self.root.after(
            15,
            self.update_camera
        )

    # =========================================================
    # CAPTURE
    # =========================================================

    def capture_image(self):

        success, frame = self.camera.read()

        if not success:

            self.status.config(
                text="CAPTURE FAILED"
            )

            return

        frame = cv2.flip(
            frame,
            1
        )

        processed = self.apply_effect(
            frame
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            self.output_dir /
            f"APEX_{timestamp}.jpg"
        )

        cv2.imwrite(
            str(filename),
            processed
        )

        self.status.config(
            text="APEX AI • PHOTO SAVED"
        )

        print(
            f"[APEX] Saved: {filename}"
        )

    # =========================================================
    # VOICE
    # =========================================================

    def start_voice(self):

        if self.listening:
            return

        self.listening = True

        self.voice_button.config(
            state=tk.DISABLED
        )

        self.status.config(
            text="APEX AI • LISTENING..."
        )

        thread = Thread(
            target=self.listen_for_command,
            daemon=True
        )

        thread.start()

    def listen_for_command(self):

        try:

            with sr.Microphone() as source:

                print(
                    "\n🎤 APEX listening..."
                )

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=6
                )

            text = (
                self.recognizer
                .recognize_google(audio)
                .lower()
            )

            print(
                f"[APEX VOICE] {text}"
            )

            self.voice_queue.put(
                text
            )

        except sr.WaitTimeoutError:

            self.voice_queue.put(
                "__timeout__"
            )

        except sr.UnknownValueError:

            self.voice_queue.put(
                "__unknown__"
            )

        except sr.RequestError:

            self.voice_queue.put(
                "__network_error__"
            )

        except Exception as error:

            print(
                f"[APEX VOICE ERROR] {error}"
            )

            self.voice_queue.put(
                "__error__"
            )

    # =========================================================
    # VOICE QUEUE
    # =========================================================

    def process_voice_queue(self):

        if not self.running:
            return

        try:

            command = (
                self.voice_queue
                .get_nowait()
            )

            self.listening = False

            self.voice_button.config(
                state=tk.NORMAL
            )

            if command == "__timeout__":

                self.status.config(
                    text="APEX • NO SPEECH"
                )

            elif command == "__unknown__":

                self.status.config(
                    text="APEX • COULDN'T UNDERSTAND"
                )

            elif command == "__network_error__":

                self.status.config(
                    text="APEX • NETWORK ERROR"
                )

            elif command == "__error__":

                self.status.config(
                    text="APEX • VOICE ERROR"
                )

            else:

                self.apex_core.process(
                    command
                )

        except Empty:
            pass

        self.root.after(
            100,
            self.process_voice_queue
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.running = False

        if self.share_server:

            self.share_server.stop()

        if self.camera.isOpened():
            self.camera.release()

        if self.gesture_recognizer:
            self.gesture_recognizer.close()

        self.root.destroy()


# =============================================================
# START APEX
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ApexAI(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close
    )

    root.mainloop()
