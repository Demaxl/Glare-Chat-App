<script setup>
definePageMeta({
    middleware() {
        const sessionId = useCookie("sessionid");
        sessionId.value = null;
    },
});

onMounted(() => {
    const isLoggedIn = useCookie("isLoggedIn");
    const authStore = useAuthStore();

    isLoggedIn.value = null;
    authStore.$reset();

    // Redirect to the login page
    return navigateTo("/login");
});
</script>
