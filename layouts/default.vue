<template>
    <div class="w-full">
        <div class="flex h-screen">
            <div
                class="bg-[#FAFAFA] basis-full md:max-w-[400px] md:basis-1/4 p-6 pr-2"
            >
                <NuxtIcon
                    name="logo"
                    class="w-[150px] block h-[43px] mb-[88px]"
                    :filled="true"
                    :fontControlled="false"
                />

                <p class="text-subtitle-1 font-semibold mb-7 text-black">
                    Messages
                </p>

                <div class="pr-6 mb-10 relative">
                    <NuxtIcon
                        name="search"
                        class="block absolute top-3 left-4"
                        filled
                    />
                    <input
                        class="mx-auto text-button-2 block w-full rounded-3xl border placeholder:text-[#C7C3C3] border-[#E8E8E8] py-3 pl-14 pr-9"
                        type="text"
                        placeholder="Search people or messages"
                    />
                </div>

                <div class="space-y-6">
                    <MessageItem />
                    <MessageItem />
                </div>
            </div>
            <div class="hidden md:block md:basis-3/4">
                <slot />
            </div>
        </div>
    </div>
</template>

<style>
.nuxt-icon svg {
    margin-bottom: 0;
    width: auto;
    height: auto;
}
</style>
