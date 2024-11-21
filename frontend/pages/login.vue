<template>
    <div class="flex justify-center items-center min-h-screen">
        <div
            class="mx-auto text-center bg-[#FAFAFA] tracking-wide p-8 rounded-2xl shadow-[0_0_20px_rgba(0,0,0,0.1)] w-[500px] max-w-xl"
        >
            <Icon size="40px" name="icon:logo" class="block mx-auto mb-10" />
            <p class="font-bold text-subtitle-1 mb-3">Welcome Back</p>

            <p class="text-body-2 text-gl-glare-blacktracking-normal">
                Don't have an account yet?
                <nuxt-link
                    to="/signup"
                    class="font-semibold text-black hover:underline"
                    >Sign up</nuxt-link
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
                    />
                    <ErrorMessage
                        name="username"
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
                        aria-label="password"
                        name="password"
                        placeholder="Password"
                    />
                </div>

                <input
                    type="submit"
                    :disabled="
                        !meta.dirty ||
                        !(meta.touched && meta.valid) ||
                        isSubmitting
                    "
                    value="Login"
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
import { object, string } from "yup";
import useAuth from "~/composables/useAuth";

const router = useRouter();

const initialValues = {
    username: "",
    password: "",
};

const schema = object({
    username: string().required("Required"),
    password: string().required(),
});

async function onSubmit({ username, password }, { setErrors }) {
    const { data, status, error } = await useAuth().login(username, password);

    switch (status) {
        case 200:
            router.push("/");
            break;
        case 400:
            setErrors({
                username: error,
            });
            break;
        default:
            break;
    }
}
</script>
