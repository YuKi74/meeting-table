package mysql

import (
	"fmt"
	"mt/config"
	"mt/logger"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
)

var DB *gorm.DB

func init() {
	logger.Logger.Debug("初始化数据库...")
	mysqlConfig := config.Config.Mysql
	dsn := fmt.Sprintf("%s:%s@(%s)/%s?%s", mysqlConfig.Username, mysqlConfig.Password, mysqlConfig.Addr, mysqlConfig.Database, mysqlConfig.Config)
	db, err := gorm.Open("mysql", dsn)
	if err != nil {
		logger.Logger.Error("数据库初始化失败")
		panic("数据库初始化失败...")
	}
	DB = db
	sqlDB := db.DB()
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(10)
}
