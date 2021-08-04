package connection

import (
	"mt/logger"
	"mt/models"
	"mt/server"
	"mt/utils/mysql"
	"mt/utils/redis"
	"net/http"
	"strconv"
	"time"
)

func ConnectionHandler(w http.ResponseWriter, r *http.Request) {
	token := r.URL.Query().Get("token")
	userIDStr, err := redis.Get(token)
	if err != nil {
		logger.Logger.Errorf("从Redis获取token失败: %s", err)
		return
	}
	userID, err := strconv.ParseInt(string(userIDStr), 10, 64)
	if err != nil {
		logger.Logger.Errorf("解析用户ID失败: %s", err)
		return
	}
	roomIDStr := r.URL.Query().Get("meeting_room_id")
	roomID, err := strconv.ParseInt(roomIDStr, 10, 64)
	if err != nil {
		logger.Logger.Debugf("解析会议室ID失败: %s", err)
		return
	}
	user := models.User{}
	err = mysql.DB.Where("id = ?", userID).Find(&user).Error
	if err != nil {
		logger.Logger.Errorf("数据库错误: %s", err)
		return
	}
	var count int64
	err = mysql.DB.Model(&models.MeetingRoom{}).Where("id = ? and team_id = ?", roomID, user.TeamID).Count(&count).Error
	if err != nil {
		logger.Logger.Errorf("数据库错误: %s", err)
		return
	}
	if count == 0 {
		logger.Logger.Debug("用户不属于本团队或会议室ID错误")
		return
	}
	server.AddUser(userID, roomID, w, r)
	<-time.After(3 * time.Second)
}
