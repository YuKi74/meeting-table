import Cookies from 'js-cookie';
import router from '../router';

const Connection = function (roomID) {
    const token = Cookies.get('token');
    if (!token) {
        router.push('/login');
        return;
    }
    const host = window.location.host;
    this.url = `ws://${host}/ws/?token=${token}&meeting_room_id=${roomID}`;

    this.messageHandlers = [];
    this.messageCache = [];
};

Connection.prototype.start = function () {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = this.getOpenHandler();
    this.ws.onmessage = this.getMessageHandler();
    this.ws.onclose = this.closeHandler;
    this.ws.onerror = this.closeHandler;
};

Connection.prototype.send = function (data) {
    this.ws.send(JSON.stringify(data));
};

export default Connection;
