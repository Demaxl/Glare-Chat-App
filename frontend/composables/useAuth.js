export default function () {
    const { userData } = storeToRefs(useAuthStore());

    async function login(username, password) {
        const {
            _data: { data, status, error },
        } = await useRequest().post("/api/auth/login", {
            username,
            password,
        });

        if (status === 200) {
            // Save the user data to the store
            userData.value = data.data.user;
        }
        return { status, error, data };
    }

    async function signup(username, password) {
        const {
            _data: { data, status, errors },
        } = await useRequest().post("/api/auth/signup", {
            username,
            password,
        });

        if (status === 200) {
            // Save the user data to the store
            userData.value = data.data.user;
        }
        return { status, errors, data };
    }

    function isAuthenticated() {
        const isLoggedIn = useCookie("isLoggedIn");
        return !!isLoggedIn.value;
    }

    return { login, signup, isAuthenticated };
}
