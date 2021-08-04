import Konva from 'konva';
import Board from './Board';

Board.prototype.startPen = function (x, y, strokeColor, strokeWidth) {
    const pen = new Konva.Line({
        points: [x, y],
        stroke: strokeColor,
        strokeWidth: strokeWidth,
        draggable: true,
    });
    this.drawLayer.add(pen);
    return pen;
};

Board.prototype.drawLine = function (
    xStart,
    yStart,
    xEnd,
    yEnd,
    strokeColor,
    strokeWidth
) {
    const line = new Konva.Line({
        points: [xStart, yStart, xEnd, yEnd],
        stroke: strokeColor,
        strokeWidth: strokeWidth,
        draggable: true,
    });
    this.drawLayer.add(line);
    return line;
};

Board.prototype.drawRect = function (
    x,
    y,
    width,
    height,
    strokeColor,
    strokeWidth,
    fillColor
) {
    const rect = new Konva.Rect({
        x: x,
        y: y,
        width: width,
        height: height,
        stroke: strokeColor,
        strokeWidth: strokeWidth,
        fill: fillColor,
        draggable: true,
    });
    this.drawLayer.add(rect);
    return rect;
};

Board.prototype.drawEllipse = function (
    xCenter,
    yCenter,
    width,
    height,
    strokeColor,
    strokeWidth,
    fillColor
) {
    const ellipse = new Konva.Ellipse({
        x: xCenter,
        y: yCenter,
        width: width,
        height: height,
        stroke: strokeColor,
        strokeWidth: strokeWidth,
        fill: fillColor,
        draggable: true,
    });
    this.drawLayer.add(ellipse);
    return ellipse;
};

Board.prototype.drawText = function (x, y, textContent, fontSize, fontColor) {
    const text = new Konva.Text({
        x: x,
        y: y,
        text: textContent,
        fontSize: fontSize,
        fill: fontColor,
        draggable: true,
    });
    this.layer.add(text);
    return text;
};
