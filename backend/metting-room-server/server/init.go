package server

import (
	"mt/logger"
	"mt/server/structure"
)

var manager = structure.RoomManager{
	Rooms:      make(map[int64]*structure.Room),
	Register:   make(chan *structure.ConnectionStruct),
	Unregister: make(chan *structure.Room),
}

func init() {
	logger.Logger.Debug("启动连接层服务...")
	go manager.Start()
}
