import Konva from 'konva';
import Board from './Board';

Board.prototype.drawRect = function (x, y, width, height, color) {
    const rect = new Konva.Rect({
        x: x,
        y: y,
        width: width,
        height: height,
        fill: color,
        draggable: true,
    });
    this.layer.add(rect);
    return rect;
};
