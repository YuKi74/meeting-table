package server

import (
	"net/http"
	"time"

	"github.com/gorilla/websocket"
)

type roomManager struct {
	Rooms      map[int64]*room
	Register   chan *ConnectionStruct
	Unregister chan *room
}

type room struct {
	ID         int64
	Users      map[int64]*user
	Register   chan *user
	Unregister chan *user
	Broadcast  chan []byte
}

type user struct {
	ID      int64
	Room    *room
	Socket  *websocket.Conn
	Send    chan []byte
	Receive chan []byte
}

type ConnectionStruct struct {
	UserID  int64
	RoomID  int64
	Writer  http.ResponseWriter
	Request *http.Request
}

func (manager *roomManager) start() {
	for {
		select {
		case connectionStruct := <-manager.Register:
			if _, ok := manager.Rooms[connectionStruct.RoomID]; !ok {
				manager.addRoom(connectionStruct.RoomID)
			}
			manager.Rooms[connectionStruct.RoomID].addUser(connectionStruct.UserID, connectionStruct.Writer, connectionStruct.Request)
		case room := <-manager.Unregister:
			delete(manager.Rooms, room.ID)
		}
	}
}

func (manager *roomManager) addRoom(roomID int64) {
	r := &room{
		ID:         roomID,
		Users:      make(map[int64]*user),
		Register:   make(chan *user),
		Unregister: make(chan *user),
		Broadcast:  make(chan []byte),
	}
	manager.Rooms[roomID] = r
	go r.start()
}

func (r *room) addUser(userID int64, writer http.ResponseWriter, request *http.Request) {
	coon, err := upgrader.Upgrade(writer, request, nil)
	if err != nil {
		return
	}
	u := &user{
		ID:      userID,
		Room:    r,
		Socket:  coon,
		Send:    make(chan []byte),
		Receive: make(chan []byte),
	}
	r.Register <- u
	go u.start()
}

func (r *room) start() {
	defer func() {
		manager.Unregister <- r
	}()

	for {
		select {
		case user := <-r.Register:
			if _, ok := r.Users[user.ID]; ok {
				r.Users[user.ID].stop()
			}
			r.Users[user.ID] = user
		case user := <-r.Unregister:
			delete(r.Users, user.ID)
			if len(r.Users) == 0 {
				return
			}
		case message := <-r.Broadcast:
			r.broadcast(message)
		}
	}
}

func (r *room) broadcast(message []byte) {
	for _, user := range r.Users {
		user.Send <- message
	}
}

func (u *user) start() {
	go u.readLoop()
	go u.writeLoop()

	defer func() {
		if u.stop() {
			u.Room.Unregister <- u
		}
	}()
	for {
		select {
		case <-time.After(5 * time.Second):
			u.Socket.WriteMessage(websocket.TextMessage, []byte("TIME_OUT"))
			return
		case message, ok := <-u.Receive:
			if !ok {
				return
			}
			if string(message) == "ping" {
				u.Send <- []byte("pong")
			} else {
				u.Room.Broadcast <- message
			}
		}
	}
}

func (u *user) stop() bool {
	if u.Socket.Close() != nil {
		return false
	}
	close(u.Send)
	close(u.Receive)
	return true
}

func (u *user) readLoop() {
	for {
		_, message, err := u.Socket.ReadMessage()
		if err != nil {
			return
		}
		u.Receive <- message
	}
}

func (u *user) writeLoop() {
	for {
		message, ok := <-u.Send
		if !ok {
			u.Socket.WriteMessage(websocket.CloseMessage, []byte{})
			return
		}
		u.Socket.WriteMessage(websocket.TextMessage, message)
	}
}
