package logger

import (
	"mt/config"
	"os"

	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var Logger *zap.SugaredLogger

func init() {
	encoder := getEncoder()
	infoWriteSyncer := getWriteSyncer("info.log")
	debugWriteSyncer := getWriteSyncer("debug.log")
	cores := make([]zapcore.Core, 0)
	cores = append(cores, zapcore.NewCore(encoder, infoWriteSyncer, zapcore.InfoLevel))
	cores = append(cores, zapcore.NewCore(encoder, debugWriteSyncer, zapcore.DebugLevel))
	if config.Config.Log.Console {
		cores = append(cores, zapcore.NewCore(encoder, zapcore.AddSync(os.Stdout), zapcore.DebugLevel))
	}
	core := zapcore.NewTee(cores...)
	Logger = zap.New(core, zap.AddCaller()).Sugar()
}

func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	return zapcore.NewConsoleEncoder(encoderConfig)
}

func getWriteSyncer(filename string) zapcore.WriteSyncer {
	lumberJackLogger := &lumberjack.Logger{
		Filename:   config.Config.Log.Path + "/" + filename,
		MaxSize:    10,
		MaxBackups: 60,
		MaxAge:     30,
		LocalTime:  true,
		Compress:   false,
	}
	return zapcore.AddSync(lumberJackLogger)
}
