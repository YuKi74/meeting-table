import Konva from 'konva';
import Board from './board';

Board.prototype.startPen = function () {
    const pen = new Konva.Line({
        points: [this.xStart, this.yStart],
        stroke: this.strokeColor,
        strokeWidth: this.strokeWidth,
        draggable: true,
    });
    this.drawLayer.add(pen);
    this.shape = pen;
};

Board.prototype.drawLine = function () {
    const line = new Konva.Line({
        points: [this.xStart, this.yStart, this.xStart, this.yStart],
        stroke: this.strokeColor,
        strokeWidth: this.strokeWidth,
        draggable: true,
    });
    this.drawLayer.add(line);
    this.shape = line;
};

Board.prototype.drawRect = function () {
    const rect = new Konva.Rect({
        x: this.xStart,
        y: this.yStart,
        width: 0,
        height: 0,
        stroke: this.strokeColor,
        strokeWidth: this.strokeWidth,
        fill: this.fillColor,
        draggable: true,
    });
    this.drawLayer.add(rect);
    this.shape = rect;
};

Board.prototype.drawEllipse = function () {
    const ellipse = new Konva.Ellipse({
        x: this.xStart,
        y: this.yStart,
        width: 0,
        height: 0,
        stroke: this.strokeColor,
        strokeWidth: this.strokeWidth,
        fill: this.fillColor,
        draggable: true,
    });
    this.drawLayer.add(ellipse);
    this.shape = ellipse;
};

Board.prototype.updatePen = function () {
    this.shape.attrs.points.push(this.x, this.y);
    this.shape.draw();
};

Board.prototype.updateLine = function () {
    this.shape.setAttrs({
        duration: 0,
        points: [
            this.shape.attrs.points[0],
            this.shape.attrs.points[1],
            this.x,
            this.y,
        ],
    });
};

Board.prototype.updateRect = function () {
    if (this.isRegular) {
        let side = Math.max(
            Math.abs(this.x - this.xStart),
            Math.abs(this.y - this.yStart)
        );
        this.shape.setAttrs({
            x: this.xStart < this.x ? this.xStart : this.xStart - side,
            y: this.yStart < this.y ? this.yStart : this.yStart - side,
            width: side,
            height: side,
        });
    } else {
        this.shape.setAttrs({
            x: Math.min(this.x, this.xStart),
            y: Math.min(this.y, this.yStart),
            width: Math.abs(this.x - this.xStart),
            height: Math.abs(this.y - this.yStart),
        });
    }
};

Board.prototype.updateEllipse = function () {
    if (this.isRegular) {
        let diameter = Math.max(
            Math.abs(this.x - this.xStart),
            Math.abs(this.y - this.yStart)
        );
        this.shape.setAttrs({
            x:
                this.xStart < this.x
                    ? (2 * this.xStart + diameter) / 2
                    : (2 * this.xStart - diameter) / 2,
            y:
                this.yStart < this.y
                    ? (2 * this.yStart + diameter) / 2
                    : (2 * this.yStart - diameter) / 2,
            width: diameter,
            height: diameter,
        });
    } else {
        this.shape.setAttrs({
            x: (this.x + this.xStart) / 2,
            y: (this.y + this.yStart) / 2,
            width: Math.abs(this.x - this.xStart),
            height: Math.abs(this.y - this.yStart),
        });
    }
};

Board.prototype.completeDraw = function () {
    const defer = function (that) {
        that.isDrawing = false;
        that.xStart = 0;
        that.yStart = 0;
        that.shape = null;
    };
    if (!this.isValid) {
        if (this.shape) {
            this.shape.destroy();
        }
        defer(this);
        return;
    }
    if (this.isDrawing) {
        this.shape.moveTo(this.layer);
        this.shape['globalID'] = this.userID + '_' + new Date().getTime();
        this.sendShapeData('paint', this.shape);
        this.shapeList[this.shape['globalID']] = this.shape;
        this.transformer.nodes([this.shape]);
    } else if (this.transformer.nodes().length) {
        this.sendShapeData('move', this.transformer.nodes()[0]);
    }
    defer(this);
};

Board.prototype.sendShapeData = function (type, shape) {
    const data = {
        Type: type,
        Target: 'board',
        Data: [shape.globalID, shape.toJSON()],
    };
    this.connection.send(data);
};
