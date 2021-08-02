package server

import (
	"mt/logger"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,

	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var manager = roomManager{
	Rooms:      make(map[int64]*room),
	Register:   make(chan *ConnectionStruct),
	Unregister: make(chan *room),
}

func init() {
	logger.Logger.Debug("启动连接层服务...")
	go manager.start()
}
