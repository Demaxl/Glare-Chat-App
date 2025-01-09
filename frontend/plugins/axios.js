import axios from "axios";

export default defineNuxtPlugin((nuxtApp) => {
    const config = useRuntimeConfig();

    const axiosInstance = axios.create({
        baseURL: config.public.backendURL,
        withCredentials: true,
    });

    return {
        provide: {
            axios: axiosInstance,
        },
    };
});
