import axios from 'axios';
import configs from "../configs";

const axiosConfigs = {
    baseURL: configs.apiUrl
}

const getAxiosClient = () => {
    const token = localStorage.getItem("token");
    if (!token || token === 'undefined') return axios.create(axiosConfigs);
    return axios.create({
        ...axiosConfigs,
        headers: {
            Authorization: `Bearer ${JSON.parse(token)}`
        }
    })
}
export default getAxiosClient;