import socket
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3000

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
            print("Connected to server.")

            print("Available commands: ")
            print("  GET_STUDENT_COUNT")
            print("  ADD_STUDENT <id>,<name>,<major>,<email>")
            print("      e.g., ADD_STUDENT 320240092,Asma Shokr,CS,asma@mail.com")
            print("  GET_STUDENT_INFO <student_id>")
            print("      e.g., GET_STUDENT_INFO 320240092")
            print("  QUIT")
            print("-" * 30)

            while True:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue

                s.sendall(cmd.encode())

                if cmd.upper() == "QUIT":
                    print("Disconnecting...")
                    print("Server:", s.recv(4096).decode())
                    break

                resp = s.recv(4096).decode()

                try:
                    parsed = json.loads(resp)
                    print("Server:", json.dumps(parsed, indent=2))
                except:
                    print("Server:", resp)

        except ConnectionRefusedError:
            print(f"Cannot connect to {SERVER_HOST}:{SERVER_PORT}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Client exited.")

if __name__ == "__main__":
    run_client()
