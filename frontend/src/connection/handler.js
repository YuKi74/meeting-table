import Connection from './connection';
import { message } from 'ant-design-vue';
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

Connection.prototype.packMessageHandler = function (messageHandler) {
    return function (event) {
        if (event.data === 'pong') {
            return;
        }
        if (messageHandler) {
            messageHandler(JSON.parse(event.data));
        }
    };
};

Connection.prototype.errorHandler = function () {
    message.warn('与服务器的连接已断开，请刷新窗口重新连接！', 0);
};
