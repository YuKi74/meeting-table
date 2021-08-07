import chat from '../components/meeting-room/chat.vue';

const calcStyle = function (style, board, deltaX = 0, deltaY = 0) {
    const pos = board.stage.position();
    const scale = board.stage.scale().x;
    style.x += deltaX / scale;
    style.y += deltaY / scale;
    const left = style.x * scale + pos.x;
    const top = style.y * scale + pos.y;
    style.left = left + 'px';
    style.top = top + 'px';
    style.transform = `scale(${scale}, ${scale})`;
    return style;
};

const isComponent = function (name) {
    return (
        name === '聊天框' ||
        name === '创意纸' ||
        name === '代码块' ||
        name === '思维导图' ||
        name === '文件' ||
        name === '从其他会议室导入文件'
    );
};

const getComponent = function (board, x, y) {
    let node, width, height, content;
    const pos = board.getStagePosition({ x, y });
    switch (board.tool) {
        case '聊天框':
            node = chat;
            width = '350px';
            height = '500px';
            content = '';
            break;
        default:
            return;
    }
    const component = {
        node,
        style: { x: pos.x, y: pos.y, width, height, content },
    };
    calcStyle(component.style, board);
    return component;
};

const restoreComponent = function (data, board) {
    let node, width, height;
    const name = data.Target.slice(0, data.Target.indexOf('_'));
    switch (name) {
        case '聊天框':
            node = chat;
            width = '350px';
            height = '500px';
            break;
    }
    const component = {
        node,
        style: {
            x: data.Data.x,
            y: data.Data.y,
            width,
            height,
            content: data.Data.content,
        },
    };
    calcStyle(component.style, board);
    return component;
};

export { calcStyle, isComponent, getComponent, restoreComponent };
