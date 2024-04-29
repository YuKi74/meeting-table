import Konva from 'konva';
import Board from './board';
import { WHEEL_TO_SCALE } from './config';
import {
    onMouseDown,
    onMouseUp,
    onMouseMove,
    onClick,
    dragStart,
    dragEnd,
    onKeyUp,
    onKeyDown,
} from './event-functions';

Board.prototype.initStage = function () {
    createStageLayers(this);
    initVariables(this);
    initStageEventListener(this);
    initContainer(this);
};

const createStageLayers = function (board) {
    board.stage = new Konva.Stage({
        container: board.container,
        width: window.screen.width,
        height: window.screen.height,
        draggable: true,
    });
    board.layer = new Konva.Layer();
    board.drawLayer = new Konva.Layer();
    board.dragLayer = new Konva.Layer();
    board.stage.add(board.layer, board.drawLayer, board.dragLayer);
    // transformer: 当前的变化器
    board.transformer = new Konva.Transformer();
    board.layer.add(board.transformer);
    board.transformer.nodes([]);
};

const initVariables = function (board) {
    // shape: 当前正在绘制的图形
    board.shape = null;
    // shapeList: 会议室中所有图形的序列
    board.shapeList = {};

    board.tool = '移动';
    board.strokeColor = 'black';
    board.fillColor = 'black';
    board.strokeWidth = 5;

    // isDrawing: 是否正在绘制中
    board.isDrawing = false;
    // isRegular: 是否绘制正图形
    board.isRegular = false;
    // isValid: mousedown-mouseup是否有效
    board.isValid = false;
    // xStart: 绘制起点x坐标
    board.xStart = 0;
    // yStart: 绘制起点y坐标
    board.yStart = 0;
    // x: 当前鼠标的x坐标
    board.x = 0;
    // y: 当前鼠标的y坐标
    board.y = 0;
};

const initStageEventListener = function (board) {
    const stage = board.stage;

    stage.on('mousedown', function (evt) {
        onMouseDown(evt, board);
    });

    window.addEventListener('mousemove', function (evt) {
        onMouseMove(evt, board);
    });

    window.addEventListener('mouseup', function () {
        onMouseUp(board);
    });

    stage.on('click', function (evt) {
        onClick(evt, board);
    });

    stage.on('dragstart', function (evt) {
        dragStart(evt, board);
    });

    stage.on('dragmove', function (evt) {
        if (evt.target === stage) {
            board.onBoardMove();
        }
    });

    stage.on('dragend', function (evt) {
        dragEnd(evt, board);
    });

    window.addEventListener('keydown', (evt) => {
        if (evt.origin) {
            return;
        }
        onKeyDown(evt, board);
    });

    window.addEventListener('keyup', (evt) => {
        if (evt.origin) {
            return;
        }
        onKeyUp(evt, board);
    });
};

const initContainer = function (board) {
    window.addEventListener('gesturestart', (e) => {
        if (e.origin) {
            return;
        }
        e.preventDefault();
        board.startScale = board.stage.scale().x;
        const deltaScale = board.startScale * e.scale - board.stage.scale().x;
        board.scaleStage(deltaScale);
    });

    window.addEventListener('gesturechange', (e) => {
        if (e.origin) {
            return;
        }
        e.preventDefault();
        const deltaScale = board.startScale * e.scale - board.stage.scale().x;
        board.scaleStage(deltaScale);
    });

    window.addEventListener('wheel', (e) => {
        if (e.origin) {
            return;
        }
        if (e.ctrlKey) {
            e.preventDefault();
            board.scaleStage(-e.deltaY / WHEEL_TO_SCALE);
        }
    });

    board.container.addEventListener('wheel', (e) => {
        e.preventDefault();
        if (e.ctrlKey) {
            board.scaleStage(-e.deltaY / WHEEL_TO_SCALE);
        } else {
            board.moveStage(e.wheelDeltaX, e.wheelDeltaY);
        }
    });
};
