/** @type {import('tailwindcss').Config} */
export default {
    content: [],
    theme: {
        fontFamily: {
            sans: ["Axiforma", "sans-serif"],
        },
        extend: {
            colors: {
                "glare-black": "#141414",
                "glare-less-black": "#323232",
                "glare-gray": "#4F5665",
                "glare-white": "#FBFBFD",
                "glare-green": "#21978B",
                "glare-dark-green": "#156761",
                "glare-purple": "#7B7FEA",
                "glare-dark-purple": "#3D3F79",
                primary: "#21978B",
            },
            fontSize: {
                h1: ["72px", { lineHeight: "80px" }],
                h2: ["64px", { lineHeight: "72px" }],
                h3: ["52px", { lineHeight: "60px" }],
                h4: ["44px", { lineHeight: "52px" }],
                h5: ["36px", { lineHeight: "44px" }],
                h6: ["24px", { lineHeight: "36px" }],
                "subtitle-1": ["24px", { lineHeight: "32px" }],
                "subtitle-2": ["20px", { lineHeight: "32px" }],

                "body-1": ["16px", { lineHeight: "24px" }],
                "body-2": ["14px", { lineHeight: "24px" }],

                "button-1": ["20px", { lineHeight: "31px" }],
                "button-2": ["16px", { lineHeight: "25px" }],
                "button-3": ["14px", { lineHeight: "22px" }],

                caption: ["12px", { lineHeight: "19px" }],
                overline: ["18px", { lineHeight: "28px" }],
            },
            screens: {
                xs: "576px",
            },
        },
    },
    plugins: [],
};
