package handler

import (
	"encoding/json"
	"mt/config"
	"mt/logger"
	"os"
	"path"
	"strconv"
	"time"
)

type Storage struct {
	RoomID int64
	Data   []*Data
}

func (storage *Storage) Start() {
	for {
		<-time.After(30 * time.Second)
		err := storage.Store()
		if err != nil {
			logger.Logger.Debugf("储存会议室数据失败: %s", err)
		}
	}
}

func (storage *Storage) Append(data *Data) {
	storage.Data = append(storage.Data, data)
}

func (storage *Storage) Store() (err error) {
	data, err := json.Marshal(storage)
	if err != nil {
		return
	}
	filename := path.Join(config.Config.Appconfig.StoragePath, strconv.FormatInt(storage.RoomID, 10))
	file, err := os.OpenFile(filename, os.O_CREATE|os.O_RDWR, 0666)
	if err != nil {
		return
	}
	_, err = file.Write(data)
	file.Close()
	return
}

func RestoreStorage(roomID int64) (storage *Storage, err error) {
	filename := path.Join(config.Config.Appconfig.StoragePath, strconv.FormatInt(roomID, 10))
	_, err = os.Stat(filename)
	if os.IsNotExist(err) {
		storage = &Storage{
			RoomID: roomID,
			Data:   make([]*Data, 0),
		}
		return
	}
	file, err := os.OpenFile(filename, os.O_RDWR, 0666)
	if err != nil {
		return
	}
	data := make([]byte, 0)
	file.Read(data)
	err = json.Unmarshal(data, storage)
	return
}
