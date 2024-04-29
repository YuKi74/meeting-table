const Board = function (container, userID, onBoardMove) {
    this.container = container;
    this.userID = userID;
    this.onBoardMove = onBoardMove;
    this.initStage();
};

export default Board;
