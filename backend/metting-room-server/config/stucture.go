package config

import "time"

type configStruct struct {
	AppName string
	Version string

	Log       logConfig
	Mysql     mysqlConfig
	Redis     redisConfig
	Appconfig appConfig
}

type logConfig struct {
	Path    string
	Console bool
}

type mysqlConfig struct {
	Username     string `mapstructure:"username" yaml:"username"`
	Password     string `mapstructure:"password" yaml:"password"`
	Addr         string `mapstructure:"addr" yaml:"addr"`
	Database     string `mapstructure:"database" yaml:"database"`
	Config       string `mapstructure:"config" yaml:"config"`
	MaxIdleConns int    `mapstructure:"max-idle-conns" yaml:"max-idle-conns"`
	MaxOpenConns int    `mapstructure:"max-open-conns" yaml:"max-open-conns"`
}

type redisConfig struct {
	Addr        string        `mapstructure:"addr" yaml:"addr"`
	DB          int           `mapstructure:"db" yaml:"db"`
	Password    string        `mapstructure:"password" yaml:"password"`
	MaxIdle     int           `mapstructure:"maxidle" yaml:"maxidle"`
	MaxActive   int           `mapstructure:"maxactive" yaml:"maxactive"`
	IdleTimeout time.Duration `mapstructure:"idletimeout" yaml:"idletimeout"`
}

type appConfig struct {
	Port        int    `mapstructure:"port" yaml:"port"`
	FilePath    string `mapstructure:"filepath" yaml:"filepath"`
	StoragePath string `mapstructure:"storagepath" yaml:"storagepath"`
}
