import Board from './board';
import Konva from 'konva';

Board.prototype.handlePaint = function (data) {
    const globalID = data.Data[0];
    if (this.shapeList[globalID]) {
        return;
    }
    const shape = Konva.Node.create(data.Data[1], this.container);
    shape['globalID'] = globalID;
    this.shapeList[globalID] = shape;
    shape.moveTo(this.layer);
};

Board.prototype.handleMove = function (data) {
    const globalID = data.Data[0];
    if (
        !this.shapeList[globalID] ||
        this.shapeList[globalID].toJSON() === data.Data[1]
    ) {
        return;
    }
    const shape = Konva.Node.create(data.Data[1], this.container);
    if (
        this.transformer.nodes().length &&
        this.transformer.nodes()[0] === this.shapeList[globalID]
    ) {
        this.transformer.nodes([shape]);
    }
    this.shapeList[globalID].destroy();
    shape['globalID'] = globalID;
    this.shapeList[globalID] = shape;
    shape.moveTo(this.layer);
};

Board.prototype.handleDelete = function (data) {
    const globalID = data.Data[0];
    if (!this.shapeList[globalID]) {
        return;
    }
    if (
        this.transformer.nodes().length &&
        this.transformer.nodes()[0] === this.shapeList[globalID]
    ) {
        this.transformer.nodes([]);
    }
    this.shapeList[globalID].destroy();
};
