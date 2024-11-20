export default function () {
    const { userData } = storeToRefs(useAuthStore());

    async function login(username, password) {
        const response = await useRequest().post("/api/auth/login", {
            username,
            password,
        });

        if (response.status === 200) {
            // Save the user data to the store
            userData.value = response.data.user;
        }
        return response;
    }

    return { login };
}
