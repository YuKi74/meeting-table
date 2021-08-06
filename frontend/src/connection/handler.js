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

Connection.prototype.packMessageHandler = function (board) {
    return function (event) {
        if (event.data === 'pong') {
            return;
        }
        if (board.messageHandler) {
            const datas = JSON.parse(event.data);
            if (datas.length === undefined) {
                board.messageHandler.call(board, datas);
            } else if (datas.length) {
                datas.forEach((data) => {
                    board.messageHandler.call(board, data);
                });
            }
        }
    };
};

Connection.prototype.closeHandler = function () {
    message.warn('与服务器的连接已断开，请刷新窗口重新连接！', 0);
};
