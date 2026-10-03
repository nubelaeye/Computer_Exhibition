import socket
import threading

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote


class ShareServer:

    def __init__(self):

        self.server = None
        self.thread = None
        self.port = None
        self.file_path = None

    # =========================================================
    # GET LOCAL IP
    # =========================================================

    def get_local_ip(self):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        try:

            # No actual data is sent.
            sock.connect(
                ("8.8.8.8", 80)
            )

            ip = sock.getsockname()[0]

        finally:

            sock.close()

        return ip

    # =========================================================
    # START SERVER
    # =========================================================

    def start(self, file_path):

        self.file_path = Path(
            file_path
        ).resolve()

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Share file not found: {self.file_path}"
            )

        folder = self.file_path.parent
        allowed_file = self.file_path.name

        # -----------------------------------------------------
        # Custom request handler
        # -----------------------------------------------------

        class Handler(SimpleHTTPRequestHandler):

            def __init__(
                self,
                *args,
                **kwargs
            ):

                super().__init__(
                    *args,
                    directory=str(folder),
                    **kwargs
                )

            def do_GET(self):

                requested = unquote(
                    self.path.split("?")[0]
                ).lstrip("/")

                # Only allow the selected image.
                if requested != allowed_file:

                    self.send_error(
                        404,
                        "File not available"
                    )
                    return

                super().do_GET()

            def log_message(
                self,
                format,
                *args
            ):

                # Keep terminal clean.
                pass

        # Port 0 = let Windows choose an available port.
        self.server = ThreadingHTTPServer(
            ("0.0.0.0", 0),
            Handler
        )

        self.port = (
            self.server.server_address[1]
        )

        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )

        self.thread.start()

        ip = self.get_local_ip()

        url = (
            f"http://{ip}:{self.port}/{allowed_file}"
        )

        print(
            f"[APEX SHARE] Server started: {url}"
        )

        return url

    # =========================================================
    # STOP SERVER
    # =========================================================

    def stop(self):

        if self.server:

            self.server.shutdown()
            self.server.server_close()

            self.server = None

            print(
                "[APEX SHARE] Server stopped."
            )
