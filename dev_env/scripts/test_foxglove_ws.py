#!/usr/bin/env python3
"""
Local test: check if Foxglove Bridge is listening (and optionally accept a WebSocket).
Run from the host (same machine as Docker or from another machine).
Usage:
  python3 test_foxglove_ws.py
  python3 test_foxglove_ws.py 100.125.51.31
  python3 test_foxglove_ws.py 100.125.51.31 8765
"""
import socket
import sys

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8765


def tcp_check(host: str, port: int, timeout: float = 3.0) -> bool:
    """Check if something is listening on host:port (e.g. Foxglove Bridge)."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error, OSError):
        return False


def ws_check(host: str, port: int, timeout: float = 3.0) -> bool:
    """Check WebSocket connection if websocket-client is available."""
    try:
        import websocket  # type: ignore
    except ImportError:
        return False
    url = f"ws://{host}:{port}"
    try:
        ws = websocket.create_connection(url, timeout=timeout)
        ws.close()
        return True
    except Exception:
        return False


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    print(f"Checking Foxglove Bridge at {host}:{port} ...")
    if tcp_check(host, port):
        print(f"  TCP: OK (something is listening on {host}:{port})")
        if ws_check(host, port):
            print("  WebSocket: OK (Foxglove Bridge is accepting connections)")
        else:
            try:
                import websocket
            except ImportError:
                print("  WebSocket: not tested (install with: pip install websocket-client)")
            else:
                print("  WebSocket: connection failed (port may not be Foxglove)")
    else:
        print(f"  TCP: FAIL (nothing listening on {host}:{port})")
        print("  Ensure the container is running and the main launch did not crash.")
        sys.exit(1)


if __name__ == "__main__":
    main()
