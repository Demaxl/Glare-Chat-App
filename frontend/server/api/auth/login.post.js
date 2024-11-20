import useRequest from "~/composables/useRequest";

export default defineEventHandler(async (event) => {
    const { backendURL } = useRuntimeConfig();

    const { username, password } = await readBody(event);

    return useRequest(backendURL).post("/_allauth/browser/v1/auth/login", {
        username,
        password,
    });
});
