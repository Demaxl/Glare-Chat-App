// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    devtools: { enabled: true },
    modules: ["@nuxtjs/tailwindcss", "nuxt-icons"],
    css: ["~/assets/css/fonts.css", "animate.css/animate.min.css"],
});
