main module
===========

This file creates the SideNote application.

Debug mode is True.

app = create_app(debug=True)

**if __name__ == '__main__'**

    socketio.run(app, host='0.0.0.0')
