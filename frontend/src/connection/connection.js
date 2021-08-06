import Cookies from 'js-cookie';
import router from '../router';

const Connection = function (roomID, board) {
    const token = Cookies.get('token');
    if (!token) {
        router.push('/login');
        return;
    }
    const host = window.location.host;
    const url = `ws://${host}/ws/?token=${token}&meeting_room_id=${roomID}`;
    this.ws = new WebSocket(url);
    this.ws.onopen = this.getOpenHandler();
    this.ws.onmessage = this.packMessageHandler(board);
    this.ws.onclose = this.closeHandler;
    this.ws.onerror = this.closeHandler;
    board.connection = this;
};

Connection.prototype.send = function (data) {
    this.ws.send(JSON.stringify(data));
};

export default Connection;
