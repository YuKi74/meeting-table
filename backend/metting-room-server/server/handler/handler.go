package handler

import (
	"encoding/json"
	"mt/logger"
	textoperation "mt/text-operation"
	"strings"
)

func Handle(message []byte, broadcast chan []byte, storage *Storage) {
	data, err := parseMessage(message)
	if err != nil {
		logger.Logger.Debugf("解析传入数据失败: %s, 原始数据为: %s", err, string(message))
		return
	}
	var returnData []byte = nil
	if isPaintData(data) {
		returnData = handlePaintData(data, storage)
	} else if isComponentData(data) {
		returnData = handleComponentData(data, storage)
	} else if isTextData(data) {
		returnData = handleTextData(data, storage)
	} else if isIMData(data) {
		returnData = handleIMData(data, storage)
	}
	if returnData == nil {
		broadcast <- message
	} else {
		broadcast <- returnData
	}
}

func isPaintData(data *Data) bool {
	return data.Type == Paint || data.Type == Move || data.Type == Delete
}

func handlePaintData(data *Data, storage *Storage) []byte {
	paintData := data.Data.([]interface{})
	paintID := paintData[0].(string)
	switch data.Type {
	case Paint:
		storage.DataMap[paintID] = data
		storage.Append(data)
	case Move:
		storage.DataMap[paintID].Data.([]interface{})[1] = paintData[1]
	case Delete:
		delete(storage.DataMap, paintID)
		storage.Data = deletePaint(storage.Data, paintID)
	}
	return nil
}

func isComponentData(data *Data) bool {
	return data.Type == Component || data.Type == ComponentMove || data.Type == ComponentDelete
}

func handleComponentData(data *Data, storage *Storage) []byte {
	switch data.Type {
	case Component:
		storage.DataMap[data.Target] = data
		storage.Append(data)
		if strings.HasPrefix(data.Target, TextTool) || strings.HasPrefix(data.Target, CodeTool) {
			storage.Operations[data.Target] = make([]textoperation.Operation, 0)
		}
	case ComponentMove:
		storage.DataMap[data.Target].Data.(map[string]interface{})["x"] = data.Data.(map[string]interface{})["x"]
		storage.DataMap[data.Target].Data.(map[string]interface{})["y"] = data.Data.(map[string]interface{})["y"]
	case ComponentDelete:
		delete(storage.DataMap, data.Target)
		delete(storage.Operations, data.Target)
		storage.Data = deleteComponent(storage.Data, data.Target)
	}
	return nil
}

func isTextData(data *Data) bool {
	return data.Type == Text || data.Type == Code
}

func handleTextData(data *Data, storage *Storage) (message []byte) {
	message = []byte("pong")
	textData := data.Data.(map[string]interface{})
	operationMap := textData["operation"].(map[string]interface{})
	operation1 := textoperation.Operation{
		BaseLength:   int(operationMap["BaseLength"].(float64)),
		TargetLength: int(operationMap["TargetLength"].(float64)),
		Ops:          operationMap["Ops"].([]interface{}),
	}
	version := int(textData["version"].(float64))
	for _, operation2 := range storage.Operations[data.Target][version:] {
		operation1Prime, _, err := textoperation.Transform(operation1, operation2)
		if err != nil {
			logger.Logger.Error(err)
			return
		}
		operation1 = operation1Prime
	}
	storage.Operations[data.Target] = append(storage.Operations[data.Target], operation1)
	content := storage.DataMap[data.Target].Data.(map[string]interface{})["content"].(map[string]interface{})["content"].(string)
	content = operation1.Apply(content)
	storage.DataMap[data.Target].Data.(map[string]interface{})["content"] = map[string]interface{}{
		"content": content,
		"version": len(storage.Operations[data.Target]),
	}
	returnData := Data{
		Type:   data.Type,
		Target: data.Target,
		Data:   operation1,
	}
	message, err := json.Marshal(&returnData)
	if err != nil {
		logger.Logger.Errorf("解析Operation返回数据失败: %s", err)
	}
	return
}

func isIMData(data *Data) bool {
	return data.Type == IM
}

func handleIMData(data *Data, storage *Storage) []byte {
	oldMessages := storage.DataMap[data.Target].Data.(map[string]interface{})["content"].([]interface{})
	newMessages := append(oldMessages, data.Data)
	if len(newMessages) > 10 {
		newMessages = newMessages[1:]
	}
	storage.DataMap[data.Target].Data.(map[string]interface{})["content"] = newMessages

	return nil
}

func deletePaint(data []*Data, paintID string) []*Data {
	for k, v := range data {
		if v.Type == Paint {
			paintData := v.Data.([]interface{})
			if paintID == paintData[0].(string) {
				newData := append(data[:k], data[k+1:]...)
				return newData
			}
		}
	}
	return data
}

func deleteComponent(data []*Data, componentID string) []*Data {
	for k, v := range data {
		if v.Target == componentID {
			newData := append(data[:k], data[k+1:]...)
			return newData
		}
	}
	return data
}
