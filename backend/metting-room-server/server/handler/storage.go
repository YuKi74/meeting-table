package handler

import (
	"encoding/json"
	"io/ioutil"
	"mt/config"
	"mt/logger"
	textoperation "mt/text-operation"
	"os"
	"path"
	"strconv"
	"strings"
	"time"
)

type Storage struct {
	RoomID     int64
	Data       []*Data
	DataMap    map[string]*Data
	Operations map[string][]textoperation.Operation
}

func (storage *Storage) Start() {
	for {
		<-time.After(60 * time.Second)
		err := storage.Store()
		if err != nil {
			logger.Logger.Errorf("储存会议室数据失败: %s", err)
		}
	}
}

func (storage *Storage) Append(data *Data) {
	storage.Data = append(storage.Data, data)
}

func (storage *Storage) Bytes() (data []byte) {
	data, _ = json.Marshal(storage.Data)
	return
}

func (storage *Storage) Store() (err error) {
	data, err := json.Marshal(storage.Data)
	if err != nil {
		logger.Logger.Errorf("编码storage失败: %s", err)
		return
	}
	filename := path.Join(config.Config.Appconfig.StoragePath, strconv.FormatInt(storage.RoomID, 10))
	file, err := os.OpenFile(filename, os.O_CREATE|os.O_RDWR|os.O_TRUNC, 0666)
	if err != nil {
		logger.Logger.Errorf("创建文件失败: %s", err)
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
		err = nil
		storage = &Storage{
			RoomID:     roomID,
			Data:       make([]*Data, 0),
			DataMap:    make(map[string]*Data),
			Operations: make(map[string][]textoperation.Operation),
		}
		return
	}
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return
	}
	storageData := make([]*Data, 0)
	err = json.Unmarshal(data, &storageData)
	dataMap, operations := parseData(storageData)
	storage = &Storage{
		RoomID:     roomID,
		Data:       storageData,
		DataMap:    dataMap,
		Operations: operations,
	}
	return
}

func parseData(data []*Data) (dataMap map[string]*Data, operations map[string][]textoperation.Operation) {
	dataMap = make(map[string]*Data)
	operations = make(map[string][]textoperation.Operation)
	for _, value := range data {
		if value.Type == Component {
			dataMap[value.Target] = value
			if strings.HasPrefix(value.Target, TextTool) || strings.HasPrefix(value.Target, CodeTool) {
				value.Data.(map[string]interface{})["content"].(map[string]interface{})["version"] = 0
				operations[value.Target] = make([]textoperation.Operation, 0)
			}
		} else if value.Type == Paint {
			paintData := value.Data.([]interface{})
			dataMap[paintData[0].(string)] = value
		}
	}
	return
}
