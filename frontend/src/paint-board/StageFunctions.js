import Board from './Board';
import {
    DRAG_RATIO,
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
};

Board.prototype.scaleStage = function (deltaScale) {
    const previousScale = this.stage.scale().x;
    let currentScale;
    if (previousScale > -deltaScale) {
        currentScale = previousScale + deltaScale;
    } else {
        currentScale = MIN_SCALE;
    }
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

Board.prototype.getStagePosition = function () {
    const stagePosition = this.stage.position();
    const scale = this.stage.scale().x;
    const stageX =
        (this.stage.getPointerPosition().x - stagePosition.x) / scale;
    const stageY =
        (this.stage.getPointerPosition().y - stagePosition.y) / scale;
    return { x: stageX, y: stageY };
};
