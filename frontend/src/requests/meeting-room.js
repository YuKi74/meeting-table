import Errors from './errors';
import request from './requests';

//创建会议室
const createMeetingRoom = function (mtname) {
    return request.post('/team/room/', {
        name: mtname,
    });
};

createMeetingRoom.errors = [Errors.MISSING_PARAMETER, Errors.ERROR_INPUT];

//获取团队内所有会议室信息
const getMeetingRooms = function () {
    return request.get('/team/rooms/');
};

getMeetingRooms.errors = [Errors.TEAM_NOT_EXIST];

//获取会议室信息
const getMeetingRoomInfo = function (mtuuid) {
    return request.get('/team/room/', {
        uuid: mtuuid,
    });
};

getMeetingRoomInfo.errors = [Errors.RECORD_NOT_FOUND, Errors.FORBIDDEN];

//删除会议室
const deleteMeetingRoom = function (id) {
    return request.delete(`/team/room/${id}/`);
};

deleteMeetingRoom.errors = [
    Errors.RECORD_NOT_FOUND,
    Errors.FORBIDDEN,
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
];

export {
    createMeetingRoom,
    deleteMeetingRoom,
    getMeetingRoomInfo,
    getMeetingRooms,
};
