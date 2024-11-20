export const useAuthStore = defineStore(
    "auth",
    () => {
        const userData = ref(null);

        return {
            userData,
        };
    },
    {
        persist: {
            storage: piniaPluginPersistedstate.localStorage(),
        },
    }
);
