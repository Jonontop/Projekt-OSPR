from flask import render_template
from flask_socketio import SocketIO, emit
from flaskr import app
import subprocess
import threading

## NEEDS TO BE FIXED - ADDED, JON FIXED MY ČRT

socketio = SocketIO(app)

# Global variable to hold the subprocess
mc_process = None

@socketio.on('connect')
def handle_connect():
    emit('terminal_output', {'data': 'Connected to Minecraft Server Terminal\n'})

@socketio.on('disconnect')
def handle_disconnect():
    global mc_process
    if mc_process:
        mc_process.terminate()
        mc_process = None
    emit('terminal_output', {'data': 'Disconnected from Minecraft Server Terminal\n'})

@socketio.on('terminal_input')
def handle_terminal_input(data):
    global mc_process
    if not mc_process:
        # Start the Minecraft server process
        mc_process = subprocess.Popen(
            ['java', '-jar', 'minecraft_server.jar', 'nogui'],  # Replace with your server command
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        # Start a thread to read the output from the server
        threading.Thread(target=read_output, args=(mc_process,), daemon=True).start()

    # Send the input to the Minecraft server process
    mc_process.stdin.write(data['data'] + '\n')
    mc_process.stdin.flush()

def read_output(process):
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            socketio.emit('terminal_output', {'data': output})
    process.stdout.close()

if __name__ == '__main__':
    socketio.run(app, debug=True)