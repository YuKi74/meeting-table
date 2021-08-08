package structure

import (
	"mt/logger"
	"mt/server/handler"
	textoperation "mt/text-operation"
)

type RoomManager struct {
	Rooms      map[int64]*Room
	Register   chan *ConnectionStruct
	Unregister chan *Room
}

func (manager *RoomManager) Start() {
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

func (manager *RoomManager) addRoom(roomID int64) {
	storage, err := handler.RestoreStorage(roomID)
	if err != nil {
		logger.Logger.Errorf("恢复会议室数据失败: %s", err)
		storage = &handler.Storage{
			RoomID:     roomID,
			Data:       make([]*handler.Data, 0),
			DataMap:    make(map[string]*handler.Data),
			Operations: make(map[string][]textoperation.Operation),
		}
	}
	r := &Room{
		ID:         roomID,
		Manager:    manager,
		Users:      make(map[int64]*User),
		Register:   make(chan *User),
		Unregister: make(chan *User),
		Broadcast:  make(chan []byte),
		Storage:    storage,
	}
	manager.Rooms[roomID] = r
	go r.start()
	logger.Logger.Infof("启动新会议室: %d", roomID)
}
