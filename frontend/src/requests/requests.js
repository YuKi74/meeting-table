import axios from 'axios';
import Cookies from 'js-cookie';
import router from '../router';
import Errors, { responseHandler } from './errors';

const requests = axios.create({
    baseURL: '/api/',
});

requests.interceptors.request.use(function (config) {
    const token = Cookies.get('token');
    if (token) {
        config.headers['token'] = token;
    }
    return config;
});

requests.interceptors.response.use(
    function (response) {
        return responseHandler(response).data;
    },
    function (error) {
        const response = responseHandler(error.response);
        if (response.data.error === Errors.NEED_LOG_IN) {
            router.push('/login');
        } else {
            return Promise.reject(response.data);
        }
    }
);

export default requests;
