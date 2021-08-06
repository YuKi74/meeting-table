import Board from './board';

Board.prototype.messageHandler = function (data) {
    switch (data.Type) {
        case 'paint':
            this.handlePaint(data);
            break;
        case 'move':
            this.handleMove(data);
            break;
        case 'delete':
            this.handleDelete(data);
            break;
    }
};
