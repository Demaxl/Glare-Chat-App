<script setup>
onMounted(() => {
    const sessionId = useCookie("sessionid");
    const authStore = useAuthStore();

    sessionId.value = null;
    authStore.$reset();

    // Redirect to the login page
    return navigateTo("/login");
});
</script>
