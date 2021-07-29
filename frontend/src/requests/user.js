import request from './requests';

const login = function (email, password) {
    return request.post('user/login/', {
        email: email,
        password: password,
    });
};

const register = function (email, userName, password) {
    return request.post('user/register/', {
        email: email,
        name: userName,
        password: password,
    });
};

export { login, register };
