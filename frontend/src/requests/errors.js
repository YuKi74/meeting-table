/* eslint-disable no-magic-numbers */

import { message as AMessage } from 'ant-design-vue';

const MTError = function (code, message) {
    this.code = parseInt(code);
    this.message = message;
};

const Errors = {
    UNKNOW_ERROR: new MTError(0, '未知错误'),
    NO_ERROR: new MTError(1, '无错误'),
    NEED_LOG_IN: new MTError(2, '未提供token或token已失效'),
    MISSING_PARAMETER: new MTError(3, '请求参数不完整'),
    RECORD_NOT_FOUND: new MTError(4, '查找的数据不存在'),
    ERROR_INPUT: new MTError(5, '输入数据有误'),
    FORBIDDEN: new MTError(100, '当前用户没有权限'),
    TEAM_NOT_EXIST: new MTError(101, '当前团队不存在'),
};

const ErrorMap = {};

Object.keys(Errors).forEach((key) => {
    const err = Errors[key];
    ErrorMap[err.code] = err;
});

const responseHandler = function (response) {
    if (response.data.status) {
        const err = ErrorMap[parseInt(response.data.status)];
        if (err) {
            response.data.error = err;
        } else {
            response.data.error = Errors.UNKNOW_ERROR;
        }
    }
    return response;
};

const defaultErrorHandler = function (request) {
    return function (data) {
        if (request.errors.includes(data.error)) {
            AMessage.error(data.data);
        } else {
            AMessage.error(data.error.message);
        }
    };
};

export default Errors;
export { responseHandler, defaultErrorHandler };
