import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    # Force output to utf-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    print(f"Starting Semantic Cluster Server pointing to: {DIRECTORY}")
    
    # Enable socket re-use to avoid port-in-use errors
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/viewer.html"
            print(f"Serving at: {url}")
            print("Opening web browser...")
            webbrowser.open(url)
            print("Press Ctrl+C in this terminal window to stop the server.")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
