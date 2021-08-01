import Konva from 'konva';

const Board = function (container) {
    this.stage = new Konva.Stage({
        container: container,
        width: window.innerWidth,
        height: window.innerHeight,
        draggable: true,
    });
    this.layer = new Konva.Layer();
    this.dragLayer = new Konva.Layer();
    this.stage.add(this.layer, this.dragLayer);

    this.initContainer(container);
};

export default Board;
