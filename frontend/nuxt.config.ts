// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    devtools: { enabled: true },
    modules: ["@nuxtjs/tailwindcss", "@nuxt/icon", "@vueuse/nuxt"],
    css: ["~/assets/css/fonts.css", "animate.css/animate.min.css"],
    icon: {
        customCollections: [
            {
                prefix: "icon",
                dir: "./assets/icons",
            },
        ],
    },
});