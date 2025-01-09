export const useAuthStore = defineStore(
    "auth",
    () => {
        const { $axios } = useNuxtApp();
        /*
            State properties
        */
        const userData = ref(null);

        async function isAuthenticated() {
            try {
                const response = await $axios.get(
                    "/_allauth/browser/v1/auth/session"
                );
                // If the request succeeds, update the user data
                userData.value = response.data.data.user;
                return true;
            } catch (error) {
                userData.value = null;
                return false;
            }
        }

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

        return { login, isAuthenticated, userData };
    },
    {
        persist: {
            storage: piniaPluginPersistedstate.localStorage(),
        },
    }
);
