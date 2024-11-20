export default function () {
    async function login(username, password) {
        return await useRequest().post("/api/auth/login", {
            username,
            password,
        });
    }

    return { login };
}
