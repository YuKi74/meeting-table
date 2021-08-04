package structure

import (
	"mt/logger"
	"mt/server/handler"
	"time"

	"github.com/gorilla/websocket"
)

type User struct {
	ID      int64
	Room    *Room
	Socket  *websocket.Conn
	Send    chan []byte
	Receive chan []byte
}

func (u *User) start() {
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
				handler.Handle(message, u.Room.Broadcast, u.Room.Storage)
			}
		}
	}
}

func (u *User) stop() bool {
	logger.Logger.Infof("用户: %d 断开连接", u.ID)
	if u.Socket.Close() != nil {
		return false
	}
	close(u.Send)
	close(u.Receive)
	return true
}

func (u *User) readLoop() {
	for {
		_, message, err := u.Socket.ReadMessage()
		if err != nil {
			return
		}
		u.Receive <- message
	}
}

func (u *User) writeLoop() {
	for {
		message, ok := <-u.Send
		if !ok {
			u.Socket.WriteMessage(websocket.CloseMessage, []byte{})
			return
		}
		u.Socket.WriteMessage(websocket.TextMessage, message)
	}
}
