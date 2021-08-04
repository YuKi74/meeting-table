import Konva from 'konva';

const Board = function (container) {
    this.stage = new Konva.Stage({
        container: container,
        width: window.innerWidth,
        height: window.innerHeight,
        draggable: true,
    });
    this.layer = new Konva.Layer();
    this.drawLayer = new Konva.Layer();
    this.dragLayer = new Konva.Layer();
    this.stage.add(this.layer, this.drawLayer, this.dragLayer);
    // transformer: 当前的变化器
    this.transformer = null;
    // shape: 当前正在绘制的图形
    this.shape = null;

    this.tool = '移动';
    this.strokeColor = 'black';
    this.fillColor = 'black';
    this.strokeWidth = 5;
    this.textColor = 'black';
    this.fontSize = 36;

    // isDrawing: 是否正在绘制中
    this.isDrawing = false;
    // isRegular: 是否绘制正图形
    this.isRegular = false;
    // isValid: 绘制的图形是否有效
    this.isValid = false;
    // xStart: 绘制起点x坐标
    this.xStart = 0;
    // yStart: 绘制起点y坐标
    this.yStart = 0;
    // x: 当前鼠标的x坐标
    this.x = 0;
    // y: 当前鼠标的y坐标
    this.y = 0;

    this.initContainer(container);
    this.initStage();
};

export default Board;
