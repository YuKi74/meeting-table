package handler

import "encoding/json"

type Data struct {
	Type   string
	Target string
	Data   interface{}
}

func parseMessage(message []byte) (data *Data, err error) {
	data = &Data{}
	err = json.Unmarshal(message, data)
	return
}
