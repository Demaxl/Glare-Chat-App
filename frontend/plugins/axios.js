import axios from "axios";

export default defineNuxtPlugin((nuxtApp) => {
    const config = useRuntimeConfig();

    const axiosInstance = axios.create({
        baseURL: config.public.backendURL,
        withCredentials: true,
        headers: {
            "X-CSRFToken": useCookie("csrftoken").value,
        },
    });

    return {
        provide: {
            axios: axiosInstance,
        },
    };
});
