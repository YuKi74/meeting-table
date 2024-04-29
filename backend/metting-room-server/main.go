package main

import (
	"fmt"
	"mt/config"
	"mt/connection"
	"mt/logger"
	"net/http"
)

func main() {
	http.HandleFunc("/", connection.ConnectionHandler)
	address := fmt.Sprintf("127.0.0.1:%d", config.Config.Appconfig.Port)
	logger.Logger.Debugf("%s : %s 应用启动，绑定: %s...", config.Config.AppName, config.Config.Version, address)
	http.ListenAndServe(address, nil)
}
