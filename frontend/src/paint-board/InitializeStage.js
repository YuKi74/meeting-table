import Konva from 'konva';
import Board from './Board';
import { WHEEL_TO_SCALE, DEFAULT_WIDTH, DEFAULT_HEIGHT } from './config';

Board.prototype.initContainer = function (container) {
    container.addEventListener('gesturestart', (e) => {
        e.preventDefault();
        this.startScale = this.stage.scale().x;
        const deltaScale = this.startScale * e.scale - this.stage.scale().x;
        this.scaleStage(deltaScale);
    });
    container.addEventListener('gesturechange', (e) => {
        e.preventDefault();
        const deltaScale = this.startScale * e.scale - this.stage.scale().x;
        this.scaleStage(deltaScale);
    });
    container.addEventListener('wheel', (e) => {
        e.preventDefault();
        if (e.ctrlKey) {
            this.scaleStage(-e.deltaY / WHEEL_TO_SCALE);
        } else {
            this.moveStage(e.wheelDeltaX, e.wheelDeltaY);
        }
    });
    window.addEventListener('keydown', (evt) => {
        switch (evt.key) {
            case 'Backspace':
                if (this.transformer._nodes && this.transformer._nodes.length) {
                    this.transformer._nodes[0].destroy();
                    this.transformer.destroy();
                    this.transformer = new Konva.Transformer();
                    this.layer.add(this.transformer);
                }
                break;
            case 'ArrowLeft':
                if (this.transformer._nodes && this.transformer._nodes.length) {
                    this.transformer._nodes[0].move({
                        x: -2,
                        y: 0,
                    });
                }
                break;
            case 'ArrowRight':
                if (this.transformer._nodes && this.transformer._nodes.length) {
                    this.transformer._nodes[0].move({
                        x: 2,
                        y: 0,
                    });
                }
                break;
            case 'ArrowUp':
                if (this.transformer._nodes && this.transformer._nodes.length) {
                    this.transformer._nodes[0].move({
                        x: 0,
                        y: -2,
                    });
                }
                break;
            case 'ArrowDown':
                if (this.transformer._nodes && this.transformer._nodes.length) {
                    this.transformer._nodes[0].move({
                        x: 0,
                        y: 2,
                    });
                }
                break;
            case 'Shift':
                if (this.isDrawing) {
                    this.isRegular = true;
                    if (this.shape.className === 'Rect') {
                        let side = Math.max(
                            Math.abs(this.x - this.xStart),
                            Math.abs(this.y - this.yStart)
                        );
                        this.shape.setAttrs({
                            x:
                                this.xStart < this.x
                                    ? this.xStart
                                    : this.xStart - side,
                            y:
                                this.yStart < this.y
                                    ? this.yStart
                                    : this.yStart - side,
                            width: side,
                            height: side,
                        });
                    } else if (this.shape.className === 'Ellipse') {
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
                    }
                }
                break;
        }
    });
    window.addEventListener('keyup', (evt) => {
        switch (evt.key) {
            case 'Backspace':
                // TODO 绘图持久化
                break;
            case 'ArrowLeft':
                // TODO 绘图持久化
                break;
            case 'ArrowRight':
                // TODO 绘图持久化
                break;
            case 'ArrowUp':
                // TODO 绘图持久化
                break;
            case 'ArrowDown':
                // TODO 绘图持久化
                break;
            case 'Shift':
                if (this.isDrawing) {
                    this.isRegular = false;
                    if (this.shape.className === 'Rect') {
                        this.shape.setAttrs({
                            x: Math.min(this.x, this.xStart),
                            y: Math.min(this.y, this.yStart),
                            width: Math.abs(this.x - this.xStart),
                            height: Math.abs(this.y - this.yStart),
                        });
                    } else if (this.shape.className === 'Ellipse') {
                        this.shape.setAttrs({
                            x: (this.x + this.xStart) / 2,
                            y: (this.y + this.yStart) / 2,
                            width: Math.abs(this.x - this.xStart),
                            height: Math.abs(this.y - this.yStart),
                        });
                    }
                }
                break;
        }
    });
};

Board.prototype.initStage = function () {
    const that = this;
    const stage = this.stage;

    this.transformer = new Konva.Transformer();
    this.layer.add(this.transformer);

    stage.on('mousedown', function (evt) {
        if (evt.target === stage) {
            that.xStart = that.getStagePosition().x;
            that.yStart = that.getStagePosition().y;
            switch (that.tool) {
                case '画笔':
                    that.isDrawing = true;
                    that.isValid = false;
                    that.shape = that.startPen(
                        that.xStart,
                        that.yStart,
                        that.strokeColor,
                        that.strokeWidth
                    );
                    break;
                case '直线':
                    that.isDrawing = true;
                    that.isValid = false;
                    that.shape = that.drawLine(
                        that.xStart,
                        that.yStart,
                        that.xStart,
                        that.yStart,
                        that.strokeColor,
                        that.strokeWidth
                    );
                    break;
                case '矩形':
                    that.isDrawing = true;
                    that.isValid = false;
                    that.shape = that.drawRect(
                        that.xStart,
                        that.yStart,
                        DEFAULT_WIDTH,
                        DEFAULT_HEIGHT,
                        that.strokeColor,
                        that.strokeWidth,
                        that.fillColor
                    );
                    break;
                case '椭圆':
                    that.isDrawing = true;
                    that.isValid = false;
                    that.shape = that.drawEllipse(
                        that.xStart,
                        that.yStart,
                        DEFAULT_WIDTH,
                        DEFAULT_HEIGHT,
                        that.strokeColor,
                        that.strokeWidth,
                        that.fillColor
                    );
                    break;
            }
        }
    });

    stage.on('mousemove', function () {
        if (that.isDrawing) {
            that.x = that.getStagePosition().x;
            that.y = that.getStagePosition().y;
            switch (that.tool) {
                case '画笔':
                    that.isValid = true;
                    that.shape.attrs.points.push(that.x, that.y);
                    that.shape.draw();
                    break;
                case '直线':
                    that.isValid = true;
                    that.shape.setAttrs({
                        duration: 0,
                        points: [
                            that.shape.attrs.points[0],
                            that.shape.attrs.points[1],
                            that.x,
                            that.y,
                        ],
                    });
                    break;
                case '矩形':
                    that.isValid = true;
                    if (that.isRegular) {
                        let side = Math.max(
                            Math.abs(that.x - that.xStart),
                            Math.abs(that.y - that.yStart)
                        );
                        that.shape.setAttrs({
                            x:
                                that.xStart < that.x
                                    ? that.xStart
                                    : that.xStart - side,
                            y:
                                that.yStart < that.y
                                    ? that.yStart
                                    : that.yStart - side,
                            width: side,
                            height: side,
                        });
                    } else {
                        that.shape.setAttrs({
                            x: Math.min(that.x, that.xStart),
                            y: Math.min(that.y, that.yStart),
                            width: Math.abs(that.x - that.xStart),
                            height: Math.abs(that.y - that.yStart),
                        });
                    }
                    break;
                case '椭圆':
                    that.isValid = true;
                    if (that.isRegular) {
                        let diameter = Math.max(
                            Math.abs(that.x - that.xStart),
                            Math.abs(that.y - that.yStart)
                        );
                        that.shape.setAttrs({
                            x:
                                that.xStart < that.x
                                    ? (2 * that.xStart + diameter) / 2
                                    : (2 * that.xStart - diameter) / 2,
                            y:
                                that.yStart < that.y
                                    ? (2 * that.yStart + diameter) / 2
                                    : (2 * that.yStart - diameter) / 2,
                            width: diameter,
                            height: diameter,
                        });
                    } else {
                        that.shape.setAttrs({
                            x: (that.x + that.xStart) / 2,
                            y: (that.y + that.yStart) / 2,
                            width: Math.abs(that.x - that.xStart),
                            height: Math.abs(that.y - that.yStart),
                        });
                    }
                    break;
            }
        }
    });

    stage.on('mouseup', function () {
        if (that.isDrawing) {
            if (that.isValid) {
                that.shape.moveTo(that.layer);
                // TODO 绘图持久化
                that.transformer.attachTo(that.shape);
            } else {
                that.shape.destroy();
            }
            that.isDrawing = false;
            that.isRegular = false;
            that.isValid = false;
            that.xStart = 0;
            that.yStart = 0;
            that.shape = null;
        }
    });

    stage.on('click', function (evt) {
        if (evt.target !== stage) {
            that.transformer.attachTo(evt.target);
        } else {
            that.transformer.destroy();
            that.transformer = new Konva.Transformer();
            that.layer.add(that.transformer);
        }
    });

    stage.on('dragstart', function (evt) {
        if (evt.target !== stage) {
            evt.target.moveTo(that.dragLayer);
        }
    });

    stage.on('dragend', function (evt) {
        if (evt.target !== stage) {
            evt.target.moveTo(that.layer);
            // TODO 绘图持久化
        }
    });
};
