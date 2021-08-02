package server

import "net/http"

func AddUser(userID, roomID int64, w http.ResponseWriter, r *http.Request) {
	connectionStruct := &ConnectionStruct{
		UserID:  userID,
		RoomID:  roomID,
		Writer:  w,
		Request: r,
	}
	manager.Register <- connectionStruct
}
