import socket
import threading
import json

class RemoteControl:
    """Handles remote control functionality"""
    
    def __init__(self, host='0.0.0.0', port=5002):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.running = True
    
    def handle_client(self, client_socket):
        try:
            while self.running:
                data, addr = client_socket.recv(4096)
                if not data:
                    break
                
                command = json.loads(data.decode())
                
                cmd_type = command.get('type', 'move')
                params = command.get('params', {})
                
                # Execute commands based on type
                if cmd_type == 'move':
                    self.execute_move(params)
                elif cmd_type == 'rotate':
                    self.execute_rotate(params)
        
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
    
    def execute_move(self, params):
        """Move robot forward/backward/left/right"""
        direction = params.get('direction', 'forward')
        distance = params.get('distance', 10)
        speed = params.get('speed', 50)
        
        # TODO: Implement actual motor control using LEGO's API
        print(f"Moving {direction} by {distance} units at speed {speed}")
    
    def execute_rotate(self, params):
        """Rotate robot left/right"""
        angle = params.get('angle', 90)
        direction = params.get('direction', 'left')
        
        # TODO: Implement rotation logic
        print(f"Rotating {direction} by {angle} degrees")

def start_remote_control():
    """Start the remote control server"""
    controller = RemoteControl()
    
    while controller.running:
        client_socket, addr = controller.server_socket.accept()
        thread = threading.Thread(target=controller.handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_remote_control()
