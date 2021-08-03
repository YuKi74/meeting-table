package structure

import (
	"mt/server/handler"
	"net/http"
)

type Room struct {
	ID         int64
	Manager    *RoomManager
	Users      map[int64]*User
	Register   chan *User
	Unregister chan *User
	Broadcast  chan []byte
	Storage    *handler.Storage
}

func (r *Room) addUser(userID int64, writer http.ResponseWriter, request *http.Request) {
	coon, err := upgrader.Upgrade(writer, request, nil)
	if err != nil {
		return
	}
	u := &User{
		ID:      userID,
		Room:    r,
		Socket:  coon,
		Send:    make(chan []byte),
		Receive: make(chan []byte),
	}
	r.Register <- u
	go u.start()
}

func (r *Room) start() {
	defer func() {
		r.Manager.Unregister <- r
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

func (r *Room) broadcast(message []byte) {
	for _, user := range r.Users {
		user.Send <- message
	}
}
