package config

import (
	"fmt"
	"os"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

const configFile = "config.yaml"

var Config *configStruct = &configStruct{}

func init() {
	v := viper.New()

	if len(os.Args) > 1 {
		v.SetConfigFile(os.Args[1])
	} else {
		v.SetConfigFile(configFile)
	}

	err := v.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("加载配置文件失败: %s ", err))
	}

	v.WatchConfig()

	v.OnConfigChange(func(in fsnotify.Event) {
		fmt.Println("配置文件改动...")
		if err := v.Unmarshal(&Config); err != nil {
			fmt.Printf("配置读取错误: %s\n", err)
		}
	})

	if err := v.Unmarshal(&Config); err != nil {
		fmt.Printf("配置读取错误: %s\n", err)
	}
}
