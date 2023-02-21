import axios from 'axios';

let loading
const service = axios.create({
    // process.env.NODE_ENV === 'development' 来判断是否开发环境
    // easy-mock服务挂了，暂时不使用了
    // baseURL: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
    timeout: 120000,

});

// 异常拦截处理器
const errorHandler = (error) => {
    layer.close(loading)

    if (error.response) {
        layer.msg(error.response.statusText, { icon : 2, time: 5000})

    } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request);

    } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
    }


    return Promise.reject(error)

}

service.interceptors.request.use(
    config => {

        loading = layer.load(0)

        return config;
    },
    errorHandler
);

service.interceptors.response.use(
    response => {
        const { data } = response

        // console.log(data);
        layer.close(loading)
        if (data.code !== 200) {
            layer.msg(data.message, { icon : 2, time: 5000})
          
            return Promise.reject(new Error(data.message || 'Error'))
        }
        return response
    },
    errorHandler
);

export default service;
