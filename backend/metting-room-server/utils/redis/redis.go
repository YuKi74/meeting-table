package redis

import (
	"encoding/json"

	"github.com/gomodule/redigo/redis"
)

func Set(key string, data interface{}, time int) error {
	c := conn.Get()
	defer c.Close()

	value, err := json.Marshal(data)
	if err != nil {
		return err
	}

	_, err = c.Do("SET", key, value)
	if err != nil {
		return err
	}

	_, err = c.Do("EXPIRE", key, time)
	if err != nil {
		return err
	}

	return nil
}

func Exists(key string) (bool, error) {
	c := conn.Get()
	defer c.Close()

	return redis.Bool(c.Do("EXISTS", key))
}

func Get(key string) ([]byte, error) {
	c := conn.Get()
	defer c.Close()

	value, err := redis.Bytes(c.Do("GET", key))
	if err != nil {
		return nil, err
	}

	return value, nil
}

func Delete(key string) (bool, error) {
	c := conn.Get()
	defer c.Close()

	return redis.Bool(c.Do("DEL", key))
}
