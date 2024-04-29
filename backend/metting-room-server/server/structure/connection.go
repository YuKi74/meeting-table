package structure

import (
	"net/http"

	"github.com/gorilla/websocket"
)

type ConnectionStruct struct {
	UserID  int64
	RoomID  int64
	Writer  http.ResponseWriter
	Request *http.Request
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,

	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}
