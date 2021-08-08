import chat from '../components/meeting-room/chat.vue';
import mindmap from '../components/meeting-room/MindMap.vue';
import doc from '../components/meeting-room/doc.vue';

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
    const pos = board.getStagePosition({ x, y });
    if (!Object.keys(Components).includes(board.tool)) {
        return;
    }
    const component = {
        node: Components[board.tool].node,
        style: {
            x: pos.x,
            y: pos.y,
            width: Components[board.tool].width,
            height: Components[board.tool].height,
        },
        content: Components[board.tool].content,
    };
    calcStyle(component.style, board);
    return component;
};

const restoreComponent = function (data, board) {
    const name = data.Target.slice(0, data.Target.indexOf('_'));
    if (!Object.keys(Components).includes(name)) {
        return;
    }
    const component = {
        node: Components[name].node,
        style: {
            x: data.Data.x,
            y: data.Data.y,
            width: Components[name].width,
            height: Components[name].height,
        },
        content: data.Data.content,
    };
    calcStyle(component.style, board);
    return component;
};

export { calcStyle, isComponent, getComponent, restoreComponent };

const Components = {
    聊天框: {
        node: chat,
        width: '350px',
        height: '350px',
        content: [],
    },
    思维导图: {
        node: mindmap,
        width: '500px',
        height: '500px',
        content: '',
    },
    创意纸: {
        node: doc,
        width: '500px',
        height: '300px',
        content: {
            content: '',
            version: 0,
        },
    },
};
