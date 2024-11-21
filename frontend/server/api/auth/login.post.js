import useRequest from "~/composables/useRequest";

export default defineEventHandler(async (event) => {
    const { backendURL } = useRuntimeConfig();

    const { username, password } = await readBody(event);

    try {
        const response = await useRequest(backendURL).post(
            "/_allauth/browser/v1/auth/login",
            {
                username,
                password,
            }
        );

        const cookies = response.headers.getSetCookie();

        /* Attach each cookie to our incoming Request */
        for (const cookie of cookies) {
            appendResponseHeader(event, "set-cookie", cookie);
        }

        return { status: 200, error: null, data: response._data };
    } catch (error) {
        switch (error.status) {
            case 400:
                return {
                    status: 400,
                    error: "Invalid username or password",
                    data: null,
                };
                break;

            default:
                break;
        }

        return { status: 500, error: "Internal server error", data: null };
    }
});
