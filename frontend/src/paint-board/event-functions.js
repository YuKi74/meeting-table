import Konva from 'konva';

const onMouseDown = function (evt, board) {
    board.isValid = false;
    if (evt.target === board.stage) {
        board.xStart = board.getStagePosition().x;
        board.yStart = board.getStagePosition().y;
        switch (board.tool) {
            case '画笔':
                board.isDrawing = true;
                board.startPen();
                break;
            case '直线':
                board.isDrawing = true;
                board.drawLine();
                break;
            case '矩形':
                board.isDrawing = true;
                board.drawRect();
                break;
            case '椭圆':
                board.isDrawing = true;
                board.drawEllipse();
                break;
        }
    }
};

const onMouseMove = function (evt, board) {
    board.isValid = true;
    if (!board.isDrawing) {
        return;
    }
    const clientPosition = {
        x: evt.clientX,
        y: evt.clientY,
    };
    board.x = board.getStagePosition(clientPosition).x;
    board.y = board.getStagePosition(clientPosition).y;
    switch (board.tool) {
        case '画笔':
            board.updatePen();
            break;
        case '直线':
            board.updateLine();
            break;
        case '矩形':
            board.updateRect();
            break;
        case '椭圆':
            board.updateEllipse();
            break;
    }
};

const onMouseUp = function (board) {
    board.completeDraw();
};

const onClick = function (evt, board) {
    if (evt.target !== board.stage) {
        board.transformer.nodes([evt.target]);
    } else {
        board.transformer.nodes([]);
    }
};

const dragStart = function (evt, board) {
    if (evt.target !== board.stage) {
        evt.target.moveTo(board.dragLayer);
    }
};

const dragEnd = function (evt, board) {
    if (evt.target !== board.stage) {
        evt.target.moveTo(board.layer);
        if (evt.target.globalID) {
            board.sendShapeData('move', evt.target);
        }
    }
};

const onKeyDown = function (evt, board) {
    const distance = 2;
    const transformerMove = function (xMove, yMove) {
        if (board.transformer.nodes().length) {
            board.transformer.nodes()[0].move({
                x: xMove,
                y: yMove,
            });
        }
    };

    switch (evt.key) {
        case 'Backspace':
            if (board.transformer.nodes().length) {
                board.sendShapeData('delete', board.transformer.nodes()[0]);

                board.transformer.nodes()[0].destroy();
                board.transformer.destroy();
                board.transformer = new Konva.Transformer();
                board.layer.add(board.transformer);
            }
            break;
        case 'ArrowLeft':
            transformerMove(-distance, 0);
            break;
        case 'ArrowRight':
            transformerMove(distance, 0);
            break;
        case 'ArrowUp':
            transformerMove(0, -distance);
            break;
        case 'ArrowDown':
            transformerMove(0, distance);
            break;
        case 'Shift':
            board.isRegular = true;
            if (board.isDrawing) {
                if (board.shape.className === 'Rect') {
                    board.updateRect();
                } else if (board.shape.className === 'Ellipse') {
                    board.updateEllipse();
                }
            }
            break;
    }
};

const onKeyUp = function (evt, board) {
    switch (evt.key) {
        case 'ArrowLeft':
        case 'ArrowRight':
        case 'ArrowUp':
        case 'ArrowDown':
            if (board.transformer.nodes().length) {
                board.sendShapeData('move', board.transformer.nodes()[0]);
            }
            break;
        case 'Shift':
            board.isRegular = false;
            if (board.isDrawing) {
                if (board.shape.className === 'Rect') {
                    board.updateRect();
                } else if (board.shape.className === 'Ellipse') {
                    board.updateEllipse();
                }
            }
            break;
    }
};

export {
    onMouseDown,
    onMouseMove,
    onMouseUp,
    onClick,
    dragStart,
    dragEnd,
    onKeyDown,
    onKeyUp,
};
