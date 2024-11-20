export default function (baseURL = "") {
    async function get(url, params = {}) {
        return await useFetch(baseURL + url);
    }

    async function post(url, data) {
        return await $fetch(baseURL + url, {
            method: "POST",
            body: data,
        });
    }

    return { get, post };
}
