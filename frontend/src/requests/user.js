import request from './requests';

const login = function (email, password) {
    return request.post('user/login/', {
        email: email,
        password: password,
    });
};

const register = function (email, user_name, password) {
    return request.post('user/register/', {
        email: email,
        name: user_name,
        password: password,
    });
};

export { login, register };
