/* eslint-disable no-magic-numbers */

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

export default Errors;
export { responseHandler };
