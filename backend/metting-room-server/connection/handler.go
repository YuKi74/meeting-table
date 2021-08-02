package connection

import (
	"mt/models"
	"mt/server"
	"mt/utils/mysql"
	"mt/utils/redis"
	"net/http"
	"strconv"
)

func ConnectionHandler(w http.ResponseWriter, r *http.Request) {
	token := r.Header.Get("token")
	userIDStr, err := redis.Get(token)
	if err != nil {
		return
	}
	userID, err := strconv.ParseInt(string(userIDStr), 10, 64)
	if err != nil {
		return
	}
	roomIDStr := r.URL.Query().Get("meeting_room_id")
	roomID, err := strconv.ParseInt(roomIDStr, 10, 64)
	if err != nil {
		return
	}
	user := models.User{}
	err = mysql.DB.Where("id = ?", userID).Find(&user).Error
	if err != nil {
		return
	}
	var count int64
	err = mysql.DB.Model(&models.MeetingRoom{}).Where("id = ? and team_id = ?", roomID, user.TeamID).Count(&count).Error
	if err != nil {
		return
	}
	if count == 0 {
		return
	}
	server.AddUser(userID, roomID, w, r)
}
