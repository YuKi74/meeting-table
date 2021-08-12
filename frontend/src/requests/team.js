/* eslint-disable camelcase */
import Errors from './errors';
import request from './requests';

//创建团队
const createTeam = function (teamName, description) {
    return request.post('/team/', {
        name: teamName,
        introduction: description,
    });
};

createTeam.errors = [
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
    Errors.FORBIDDEN,
];

//向会议室上传文件
const uploadFile = function (file, uuid) {
    const data = new FormData();
    data.append('file', file);
    return request.post(`/team/file/${uuid}/`, data, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

uploadFile.errors = [
    Errors.RECORD_NOT_FOUND,
    Errors.MISSING_PARAMETER,
    Errors.FORBIDDEN,
    Errors.ERROR_INPUT,
];

//获取团队信息
const getTeaminfo = function (uuid) {
    return request.get(`/team/${uuid}/`);
};

getTeaminfo.errors = [Errors.TEAM_NOT_EXIST, Errors.ERROR_INPUT];

//编辑团队信息
const updateTeam = function (name, description) {
    return request.patch('/team/', {
        name: name,
        introduction: description,
    });
};

updateTeam.errors = [
    Errors.TEAM_NOT_EXIST,
    Errors.FORBIDDEN,
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
];

//创建者解散团队
const dissolveTeam = function () {
    return request.delete('/team/');
};

dissolveTeam.errors = [Errors.TEAM_NOT_EXIST, Errors.FORBIDDEN];

//成员退出团队
const quitTeam = function () {
    return request.post('/team/quit/');
};

quitTeam.errors = [Errors.TEAM_NOT_EXIST];

// 创建者移出团队成员
const removeMember = function (id) {
    return request.delete(`/team/member/${id}/`);
};

removeMember.errors = [
    Errors.TEAM_NOT_EXIST,
    Errors.FORBIDDEN,
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
    Errors.RECORD_NOT_FOUND,
];

//查看团队内所有成员
const getMembers = function () {
    return request.get('/team/member/');
};

getMembers.errors = [Errors.TEAM_NOT_EXIST];

//获取申请列表
const getApplyList = function () {
    return request.get('/team/join/');
};

getApplyList.errors = [Errors.FORBIDDEN, Errors.TEAM_NOT_EXIST];

//处理申请消息
const handleApplication = function (id, is) {
    return request.post('/team/member/', {
        application_id: id,
        is_admitted: is,
    });
};

handleApplication.errors = [
    Errors.TEAM_NOT_EXIST,
    Errors.FORBIDDEN,
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
    Errors.RECORD_NOT_FOUND,
];

//申请人提交加入团队申请
const submitApplication = function (applyId) {
    return request.post('/team/join/', {
        uuid: applyId,
    });
};

submitApplication.errors = [
    Errors.TEAM_NOT_EXIST,
    Errors.FORBIDDEN,
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
];

export {
    updateTeam,
    createTeam,
    getTeaminfo,
    dissolveTeam,
    quitTeam,
    getMembers,
    removeMember,
    getApplyList,
    handleApplication,
    submitApplication,
    uploadFile,
};
