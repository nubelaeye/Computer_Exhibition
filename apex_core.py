from urllib.parse import quote_plus
import webbrowser
import os

class ApexCore:
    
    def __init__(self, action_callback):
        self.action_callback = action_callback

    # =========================================================
    # MAIN COMMAND PARSER
    # =========================================================

    def process(self, command):
        
    # =========================================================
    # AI PORTRAIT
    # =========================================================

        if (
            "create my portrait" in command
            or "create portrait" in command
            or "ai portrait" in command
            or "animated portrait" in command
            or "artistic portrait" in command
        ):

            self.action_callback("ai_portrait")
            return

        command = command.lower().strip()

        print(f"[APEX CORE] Command: {command}")

        # -----------------------------------------------------
        # MIRROR MODES
        # -----------------------------------------------------

        if "normal" in command or "mirror mode" in command:
            self.action_callback("normal")
            return

        if "sketch" in command or "pencil" in command:
            self.action_callback("sketch")
            return

        if "cartoon" in command or "comic" in command:
            self.action_callback("cartoon")
            return

        # -----------------------------------------------------
        # PHOTO
        # -----------------------------------------------------

        if (
            "take photo" in command
            or "take a photo" in command
            or "take picture" in command
            or "take a picture" in command
            or "capture" in command
        ):
            self.action_callback("capture")
            return

        # -----------------------------------------------------
        # YOUTUBE
        # -----------------------------------------------------

        if "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            self.action_callback("youtube")
            return

        # -----------------------------------------------------
        # GOOGLE
        # -----------------------------------------------------

        if "open google" in command:
            webbrowser.open("https://www.google.com")
            self.action_callback("google")
            return

        # -----------------------------------------------------
        # MUSIC
        # -----------------------------------------------------

        if "play music" in command:

            webbrowser.open(
                "https://music.youtube.com"
            )

            self.action_callback("music")
            return
        
        # =========================================================
        # SHARE PORTRAIT
        # =========================================================

        if (
            "share" in command
            or "share my portrait" in command
            or "send my portrait" in command
        ):

            self.action_callback("share")
            return

        # -----------------------------------------------------
        # SETTINGS
        # -----------------------------------------------------

        if ("open settings" in command
            or "open system settings" in command):
            
            os.system(
                "start ms-settings:"
            )

            self.action_callback("settings")
            return
        
        # -----------------------------------------------------
        # UNKNOWN
        # -----------------------------------------------------

        self.action_callback(
            f"unknown:{command}"
        )
