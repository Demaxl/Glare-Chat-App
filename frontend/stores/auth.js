export const useAuthStore = defineStore(
    "auth",
    () => {
        const userData = ref(null);

        function $reset() {
            userData.value = null;
        }

        return {
            userData,
            $reset,
        };
    },
    {
        persist: {
            storage: piniaPluginPersistedstate.localStorage(),
        },
    }
);
