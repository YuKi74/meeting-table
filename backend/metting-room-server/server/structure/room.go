package structure

import (
	"mt/logger"
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
		logger.Logger.Errorf("连接升级失败: %s", err)
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
	preparedExit := func() (bool, error) {
		err := r.Storage.Store()
		if err != nil {
			logger.Logger.Errorf("储存会议室数据失败: %s", err)
			return false, err
		}
		return len(r.Register) == 0, nil
	}

	for {
		select {
		case user := <-r.Register:
			if _, ok := r.Users[user.ID]; ok {
				r.Users[user.ID].stop()
			}
			r.Users[user.ID] = user
			logger.Logger.Infof("会议室: %d 加入新用户: %d", r.ID, user.ID)
			user.Send <- r.Storage.Bytes()
		case user := <-r.Unregister:
			delete(r.Users, user.ID)
			if len(r.Users) == 0 {
				isPrepared, err := preparedExit()
				if err != nil {
					logger.Logger.Errorf("储存会议室: %d 信息失败，会议室已关闭", r.ID)
					return
				}
				if isPrepared {
					r.Manager.Unregister <- r
					logger.Logger.Infof("会议室: %d 中没有用户，自动关闭", r.ID)
					return
				}
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
