/* eslint-disable camelcase */
import Errors from './errors';
import request from './requests';

//创建会议室
const createMeetingRoom = function (mtname) {
    return request.post('/team/room/', {
        name: mtname,
    });
};

createMeetingRoom.errors = [Errors.MISSING_PARAMETER, Errors.ERROR_INPUT];
//获取视频通话token
const getVideoToken = function (uuid) {
    return request.get(`/team/video_token/${uuid}/`);
};

getVideoToken.errors = [
    Errors.TEAM_NOT_EXIST,
    Errors.RECORD_NOT_FOUND,
    Errors.FORBIDDEN,
];
//获取团队内所有会议室信息
const getMeetingRooms = function () {
    return request.get('/team/rooms/');
};

getMeetingRooms.errors = [Errors.TEAM_NOT_EXIST];

//获取会议室信息
const getMeetingRoomInfo = function (uuid) {
    return request.get(`/team/room/${uuid}/`);
};

getMeetingRoomInfo.errors = [Errors.RECORD_NOT_FOUND, Errors.FORBIDDEN];

//获取会议室文件
const getMeetingRoomFile = function (uuid) {
    return request.get(`/team/file/${uuid}/`);
};

getMeetingRoomFile.errors = [Errors.RECORD_NOT_FOUND];

//从某个会议室转移文件到另一个会议室
const importOtherMeetingRoomFile = function (roomId, recordId) {
    return request.post('/team/file/', {
        record_id: recordId,
        room_id: roomId,
    });
};

importOtherMeetingRoomFile.errors = [
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
    Errors.RECORD_NOT_FOUND,
    Errors.FORBIDDEN,
];

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
    getMeetingRoomFile,
    importOtherMeetingRoomFile,
    getVideoToken,
};
