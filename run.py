from flaskr import app

if __name__ == '__main__':
    app.run(debug=True)
    #socketio.run(app, debug=True, allow_unsafe_werkzeug=True)