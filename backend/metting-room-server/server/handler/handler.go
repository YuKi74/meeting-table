package handler

import "mt/logger"

func Handle(message []byte, broadcast chan []byte, storage *Storage) {
	data, err := parseMessage(message)
	if err != nil {
		logger.Logger.Debugf("解析传入数据失败: %s, 原始数据为: %s", err, string(message))
		return
	}
	if data.Type != IM {
		storage.Append(data)
	}
	broadcast <- message
}
