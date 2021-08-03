package server

import (
	"mt/server/structure"
	"net/http"
)

func AddUser(userID, roomID int64, w http.ResponseWriter, r *http.Request) {
	connectionStruct := &structure.ConnectionStruct{
		UserID:  userID,
		RoomID:  roomID,
		Writer:  w,
		Request: r,
	}
	manager.Register <- connectionStruct
}
