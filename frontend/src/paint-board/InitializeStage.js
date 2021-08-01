import Board from './Board';
import { WHEEL_TO_SCALE } from './config';

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
};

Board.prototype.initStage = function () {
    // TODO 完成相关绘图事件的监听
};
