<template>
    <div class="h-screen md:px-9 relative">
        <div class="py-3 flex items-center">
            <nuxt-link
                to="/"
                class="me-5 text-glare-green rounded-full p-2 hover:bg-[#eee] transition-colors"
            >
                <Icon name="uil:arrow-left" size="36px" class="align-middle" />
            </nuxt-link>
            <div class="flex space-x-3">
                <img
                    class="w-9 h-9"
                    src="/images/default_message_icon.png"
                    alt="Message Icon"
                />
                <div class="flex flex-col">
                    <span class="text-body-1 font-semibold text-glare-black"
                        >Suzana Colin</span
                    >
                    <span class="text-caption text-glare-gray">@suzana</span>
                </div>
            </div>
        </div>

        <div
            class="h-16 flex items-center sm:space-x-3 justify-between md:space-x-11 py-5 md:mx-9 absolute right-0 left-0 bottom-0"
        >
            <button
                class="text-primary p-3 rounded-full hover:bg-[#eee] transition-colors"
            >
                <Icon
                    class="align-middle"
                    name="uil:image-upload"
                    size="24px"
                />
            </button>
            <input
                type="text"
                class="shadow-[0px_0px_1px_0px_#00000040] focus:outline-primary border block grow rounded-3xl px-6 py-3 h-10 max-w-[850px] text-body-2"
                placeholder="Type a messsage"
            />

            <button
                class="text-primary p-3 rounded-full hover:bg-[#eee] transition-colors"
            >
                <Icon class="align-middle" name="iconoir:send" size="24px" />
            </button>
        </div>
    </div>
</template>
