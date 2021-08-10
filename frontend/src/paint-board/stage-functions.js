import Board from './board';
import {
    DRAG_RATIO,
    MAX_SCALE,
    MESSAGE_DURATION,
    MIN_SCALE,
    ORIGIN_SCALE,
} from './config';
import { message } from 'ant-design-vue';

Board.prototype.moveStage = function (deltaX, deltaY, dragRatio) {
    let stagePosition = this.stage.position();
    if (dragRatio === undefined) {
        dragRatio = DRAG_RATIO;
    }
    stagePosition.x += deltaX * dragRatio;
    stagePosition.y += deltaY * dragRatio;
    this.stage.position(stagePosition);
    this.onBoardMove();
};

Board.prototype.scaleStage = function (deltaScale) {
    const previousScale = this.stage.scale().x;
    let currentScale = previousScale + deltaScale;
    currentScale = currentScale > MIN_SCALE ? currentScale : MIN_SCALE;
    currentScale = currentScale < MAX_SCALE ? currentScale : MAX_SCALE;
    this.stage.scale({
        x: currentScale,
        y: currentScale,
    });
    const mousePosition = this.stage.getPointerPosition();
    const stagePosition = this.stage.position();
    this.moveStage(
        -(mousePosition.x - stagePosition.x) *
            ((currentScale - previousScale) / previousScale),
        -(mousePosition.y - stagePosition.y) *
            ((currentScale - previousScale) / previousScale),
        ORIGIN_SCALE
    );
    const hundred = 100;
    message.open({
        content: '' + parseInt(currentScale * hundred) + '%',
        duration: MESSAGE_DURATION,
        key: 'scale_key',
    });
};

Board.prototype.getStagePosition = function (pos) {
    if (!pos) {
        pos = this.stage.getPointerPosition();
    }
    const scale = this.stage.scale().x;
    const stageX = (pos.x - this.stage.position().x) / scale;
    const stageY = (pos.y - this.stage.position().y) / scale;
    return { x: stageX, y: stageY };
};

Board.prototype.blur = function () {
    this.transformer.nodes([]);
};
