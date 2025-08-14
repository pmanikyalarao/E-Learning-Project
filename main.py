from myBlueprints import createApp,socketio

app = createApp()

if __name__=="__main__":
    socketio.run(app,debug=True)
    # app.run(debug=True,host='0.0.0.0')