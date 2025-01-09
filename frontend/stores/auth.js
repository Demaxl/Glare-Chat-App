export const useAuthStore = defineStore(
    "auth",
    () => {
        /*
            State properties
        */
        const userData = ref(null);

        const { $axios } = useNuxtApp();

        async function login(username, password) {
            const response = await $axios.post(
                "/_allauth/browser/v1/auth/login",
                {
                    username,
                    password,
                }
            );

            switch (response.status) {
                case 200:
                    userData.value = response.data.data.user;

                    break;
            }

            return response;
        }

        return { login };
    },
    {
        persist: true,
    }
);
