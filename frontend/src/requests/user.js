import Errors from './errors';
import request from './requests';

const login = function (email, password) {
    return request.post('user/login/', {
        email: email,
        password: password,
    });
};

login.errors = [
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
    Errors.RECORD_NOT_FOUND,
];

const register = function (email, userName, password) {
    return request.post('user/register/', {
        email: email,
        name: userName,
        password: password,
    });
};

register.errors = [Errors.MISSING_PARAMETER, Errors.ERROR_INPUT];

const updateUser = function (userName, password) {
    return request.patch('user/', {
        name: userName,
        password: password,
    });
};

updateUser.errors = [
    Errors.MISSING_PARAMETER,
    Errors.ERROR_INPUT,
    Errors.FORBIDDEN,
];

const getUserinfo = function () {
    return request.get('user/');
};

getUserinfo.errors = [];

export { login, register, updateUser, getUserinfo };
