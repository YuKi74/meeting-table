import Board from './board';

Board.prototype.registerMessageHandler = function (connection) {
    connection.addMessageHandler(
        (data) => {
            return ['paint', 'move', 'delete'].includes(data.Type);
        },
        this.messageHandler,
        this
    );
    this.connection = connection;
};

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
