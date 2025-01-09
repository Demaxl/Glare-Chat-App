export default defineNuxtRouteMiddleware(async (to, from) => {
    // If the user is on the login or logout page, do not check authentication
    if (
        to.path === "/login" ||
        to.path === "/logout" ||
        to.path === "/signup"
    ) {
        return;
    }
    // If the user is not authenticated, redirect to the login page
    if (!(await useAuthStore().isAuthenticated())) {
        return navigateTo("/login");
    }
});
