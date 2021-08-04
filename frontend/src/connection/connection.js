import Cookies from 'js-cookie';
import router from '../router';

const Connection = function (roomID, messageHandler) {
    const token = Cookies.get('token');
    if (!token) {
        router.push('/login');
        return;
    }
    const host = window.location.host;
    const url = `ws://${host}/ws/?token=${token}&meeting_room_id=${roomID}`;
    this.ws = new WebSocket(url);
    this.ws.onopen = this.getOpenHandler();
    this.ws.onmessage = this.packMessageHandler(messageHandler);
    this.ws.onerror = this.errorHandler;
};

export default Connection;
