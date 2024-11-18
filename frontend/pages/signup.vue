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

            <form action="#" class="mt-8">
                <div class="pr-6 mb-4 relative">
                    <Icon
                        size="20px"
                        name="uil:envelope"
                        class="block absolute top-3 left-4"
                    />
                    <input
                        class="mx-auto text-button-2 block w-full border rounded-lg py-2 pl-14 pr-9"
                        type="text"
                        aria-label="username"
                        placeholder="Username"
                    />
                </div>
                <div class="pr-6 mb-4 relative">
                    <Icon
                        size="20px"
                        name="uil:padlock"
                        class="block absolute top-3 left-4"
                    />
                    <input
                        class="mx-auto text-button-2 block w-full border rounded-lg py-2 pl-14 pr-9"
                        type="password"
                        aria-label="password"
                        placeholder="Password"
                    />
                </div>
                <div class="pr-6 mb-6 relative">
                    <Icon
                        size="20px"
                        name="uil:padlock"
                        class="block absolute top-3 left-4"
                    />
                    <input
                        class="mx-auto text-button-2 block w-full border rounded-lg py-2 pl-14 pr-9"
                        type="password"
                        aria-label="Confirm password"
                        placeholder="Confirm password"
                    />
                </div>

                <input
                    type="submit"
                    value="Sign up"
                    class="block cursor-pointer hover:bg-glare-dark-green transition-colors tracking-wide text-button-2 w-full mx-auto rounded-lg p-2 bg-glare-green text-white"
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
            </form>
        </div>
    </div>
</template>
