import os
from flask import session, json, request
from flask_socketio import emit, join_room, leave_room
from app import routes, socketio, app
	
clients = []
datas = {}
rooms = {}
	
def getKeys(dict): 
    return list(dict.keys())
	
def getValues(dict): 
    return list(dict.values())
	
def checkDatas():
    currentRoom = session.get('room')
    if not currentRoom in datas.keys(): 
        datas[currentRoom] = {}
        datas[currentRoom]['d'] = []
		
    if not datas[currentRoom]['d'] is None:
        if len(datas[currentRoom]['d']) > 3000:
            del datas[currentRoom]['d'][0:500]
            
def clearDatas(currentRoom):
    datas[currentRoom] = {}
    datas[currentRoom]['d'] = []
    
@socketio.on('joined', namespace='/')
def joined(data):
    global rooms
    currentRoom = session.get('room')
    clients.append(request.namespace + str(currentRoom))
    #getRooms()
    
    join_room(currentRoom)
    rooms[currentRoom] = str(sum(1 for i in clients if i == request.namespace + currentRoom))
	
    #updateRooms()
    #emit('count', {
    #    'count': getValues(rooms),
	#	'rooms': getKeys(rooms)
    #}, broadcast=True)
    print('clients: '+str(rooms))
    print('--------------------------------------------------------------------------')
    
@socketio.on('disconnect', namespace='/')
def disconnect():
    global rooms
    currentRoom = session.get('room')
    clients.remove(request.namespace + str(currentRoom))
	
    rooms[currentRoom] = str(sum(1 for i in clients if i == request.namespace + currentRoom))

    leave_room(currentRoom)
    #updateRooms()
    emit('count', {
        'count': getValues(rooms),
		'rooms': getKeys(rooms)
    }, broadcast=True)
    print('clients: '+str(rooms))
	
@socketio.on('drawing', namespace='/')
def drawing(data):
    currentRoom = session.get('room')
    checkDatas()
    datas[currentRoom]['d'].append(data)
    emit('drawing', data, room=currentRoom)
	
@socketio.on('fill', namespace='/')
def fill(data):
    currentRoom = session.get('room')
    checkDatas()
    datas[currentRoom]['d'].append(data['color'])
    emit('fill', {
        'color': data['color']
    }, room=currentRoom)	
    
@socketio.on('img', namespace='/')
def loadImg(data):
    currentRoom = session.get('room')
    clearDatas(currentRoom)
    datas[currentRoom]['i'] = data
    emit('img', data, room=currentRoom)

@socketio.on('new', namespace='/')
def new(data):
    currentRoom = session.get('room')
    clearDatas(currentRoom)
    emit('new', {}, room=currentRoom)	
    
@socketio.on('save', namespace='/')
def save(newdata):
    currentRoom = session.get('room')
    
    id = newdata['id'] if newdata['id'] is not None else ''
    title = newdata['title'] if newdata['title'] is not None else ''
    tags = newdata['tags'] if newdata['tags'] is not None else ''
    thumbnail = newdata['DataURL'] if newdata['DataURL'] is not None else ''
    data = datas[currentRoom].copy() if datas[currentRoom] is not None else ''
    
    if id is not '':
        saveData = routes.saveCanvasById(id, title, tags, thumbnail, data)
    else:
        saveData = routes.saveCanvas(title, tags, thumbnail, data)
        
    emit('saved', saveData, room=currentRoom)
    print('Canvas Saved')

def revokeAccess():
    currentRoom = session.get('room')
    socketio.emit('accessRevoked', {}, room=currentRoom)	
    
@app.route('/img', methods=['GET'])
def img():
    currentRoom = session.get('room')
    return datas