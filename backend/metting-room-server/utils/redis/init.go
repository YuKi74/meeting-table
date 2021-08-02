package redis

import (
	"mt/config"
	"mt/logger"
	"time"

	"github.com/gomodule/redigo/redis"
)

var conn *redis.Pool

func init() {
	logger.Logger.Debug("初始化Redis...")
	redisConfig := config.Config.Redis
	conn = &redis.Pool{
		MaxIdle:     redisConfig.MaxIdle,
		MaxActive:   redisConfig.MaxActive,
		IdleTimeout: redisConfig.IdleTimeout,
		Dial: func() (redis.Conn, error) {
			c, err := redis.Dial("tcp", redisConfig.Addr, redis.DialDatabase(redisConfig.DB), redis.DialPassword(redisConfig.Password))
			if err != nil {
				return nil, err
			}
			return c, err
		},
		TestOnBorrow: func(c redis.Conn, t time.Time) error {
			_, err := c.Do("PING")
			return err
		},
	}
}
