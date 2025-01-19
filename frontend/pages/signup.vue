<template>
    <div class="flex justify-center items-center min-h-screen">
        <div
            class="mx-auto text-center bg-[#FAFAFA] tracking-wide p-8 rounded-2xl shadow-[0_0_20px_rgba(0,0,0,0.1)] w-[500px] max-w-xl"
        >
            <Icon size="40px" name="icon:logo" class="block mx-auto mb-10" />
            <p class="font-bold text-subtitle-1 mb-3">Create an account</p>

            <p class="text-body-2 text-glare-gray tracking-normal">
                Already have an account?
                <nuxt-link
                    to="/login"
                    class="font-semibold text-black hover:underline"
                    >Log in</nuxt-link
                >
            </p>

            <Form
                @submit="onSubmit"
                :validation-schema="schema"
                :initial-values="initialValues"
                class="mt-8"
                v-slot="{ isSubmitting, meta }"
            >
                <div class="pr-6 mb-4 relative">
                    <Icon
                        size="20px"
                        name="uil:envelope"
                        class="block absolute top-3 left-4"
                    />

                    <Field
                        name="username"
                        class="mx-auto text-button-2 block w-full border rounded-lg py-2 pl-14 pr-9"
                        type="text"
                        aria-label="username"
                        placeholder="Username"
                        rules="required|alpha_dash|min:3|max:10"
                    />
                    <ErrorMessage
                        name="username"
                        class="text-red-500 text-start block text-sm mt-2"
                    />
                </div>
                <div class="pr-6 mb-4 relative">
                    <Icon
                        size="20px"
                        name="uil:padlock"
                        class="block absolute top-3 left-4"
                    />

                    <Field
                        class="mx-auto text-button-2 block w-full border rounded-lg py-2 pl-14 pr-9"
                        type="password"
                        aria-label="password"
                        name="password"
                        placeholder="Password"
                    />

                    <ErrorMessage
                        name="password"
                        class="text-red-500 text-start block text-sm mt-2"
                    />
                </div>
                <div class="pr-6 mb-6 relative">
                    <Icon
                        size="20px"
                        name="uil:padlock"
                        class="block absolute top-3 left-4"
                    />

                    <Field
                        class="mx-auto text-button-2 block w-full border rounded-lg py-2 pl-14 pr-9"
                        type="password"
                        aria-label="Confirm password"
                        name="password2"
                        placeholder="Confirm Password"
                    />

                    <ErrorMessage
                        name="password2"
                        class="text-red-500 text-start block text-sm mt-2"
                    />
                </div>

                <input
                    type="submit"
                    :disabled="
                        !meta.dirty ||
                        !(meta.touched && meta.valid) ||
                        isSubmitting
                    "
                    value="Sign up"
                    class="block disabled:cursor-not-allowed disabled:bg-glare-gray cursor-pointer hover:bg-glare-dark-green transition-colors tracking-wide text-button-2 w-full mx-auto rounded-lg p-2 bg-glare-green text-white"
                />

                <div class="flex items-center gap-4 w-full my-4">
                    <div class="h-px flex-1 bg-glare-black"></div>
                    <span class="text-sm text-gray-500 uppercase font-medium"
                        >or</span
                    >
                    <div class="h-px flex-1 bg-glare-black"></div>
                </div>

                <input
                    type="submit"
                    value="Continue with Google"
                    class="block cursor-pointer border-glare-black transition-colors tracking-wide text-button-2 w-full mx-auto rounded-lg p-2 border"
                />
            </Form>
        </div>
    </div>
</template>

<script setup>
import { object, string, ref } from "yup";

const initialValues = {
    username: "",
    password: "",
    password2: "",
};

const schema = object({
    username: string()
        .required("Username is required")
        .matches(
            /^[a-zA-Z0-9_-]+$/,
            "Username can only contain letters, numbers, dashes, and underscores"
        )
        .min(3, "Username must be at least 3 characters")
        .max(10, "Username cannot be more than 10 characters"),
    password: string()
        .required()
        .min(8, "Password must be at least 8 characters")
        .matches(/.*[^0-9].*/, "Password cannot be entirely numeric"),
    password2: string()
        .oneOf([ref("password"), null], "Passwords must match")
        .required("Confirm password is required"),
});

async function onSubmit({ username, password }, { setFieldError }) {
    const response = await useAuthStore().signup(username, password);

    switch (response.status) {
        case 200:
            navigateTo("/");
            break;
        case 400:
            for (const error of response.data.errors) {
                setFieldError(error.param, error.message);
            }
            break;
        default:
            break;
    }
}
</script>
