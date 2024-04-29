import Connection from './connection';
import { message as AMessage } from 'ant-design-vue';
import { HEART_BEAT_DURATION } from './config';

Connection.prototype.getOpenHandler = function () {
    const ws = this.ws;
    const heartBeat = function () {
        setTimeout(() => {
            ws.send('ping');
            heartBeat();
        }, HEART_BEAT_DURATION);
    };
    return heartBeat;
};

Connection.prototype.getMessageHandler = function () {
    const messageCache = this.messageCache;
    const messageHandlers = this.messageHandlers;
    const handleData = function (data) {
        messageHandlers.forEach((messageHandler) => {
            if (messageHandler.rule(data)) {
                messageHandler.handler.call(messageHandler.caller, data);
            }
        });
        messageCache.unshift(data);
    };
    return function (event) {
        if (event.data === 'pong') {
            return;
        }
        const datas = JSON.parse(event.data);
        if (datas.length === undefined) {
            handleData(datas);
        } else if (datas.length) {
            datas.forEach((data) => {
                handleData(data);
            });
        }
    };
};

Connection.prototype.addMessageHandler = function (rule, handler, caller) {
    const messageHandler = {
        rule: rule,
        handler: handler,
        caller: caller,
    };
    this.messageHandlers.push(messageHandler);
    for (let i = this.messageCache.length - 1; i >= 0; i--) {
        const message = this.messageCache[i];
        if (messageHandler.rule(message)) {
            this.messageCache = this.messageCache
                .slice(0, i)
                .concat(this.messageCache.slice(i + 1));
            messageHandler.handler.call(messageHandler.caller, message);
        }
    }
};

Connection.prototype.closeHandler = function () {
    AMessage.warn('与服务器的连接已断开，请刷新窗口重新连接！', 0);
};
