<template>
    <div class="h-screen pl-3 md:pl-9 relative">
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
            ref="messages-container"
            class="overflow-y-auto h-[80vh] pb-10 glare-scrollbar pr-3 md:pr-9"
        >
            <div class="space-y-2 pt-16">
                <MessageItem
                    v-for="message in messages"
                    :key="message.id"
                    :text="message.text"
                    :userIsSender="message.userIsSender"
                />
                <MessageItem
                    v-for="message in messages"
                    :key="message.id"
                    :text="message.text"
                    :userIsSender="message.userIsSender"
                />
                <MessageItem
                    v-for="message in messages"
                    :key="message.id"
                    :text="message.text"
                    :userIsSender="message.userIsSender"
                />
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

<script setup>
const messages = [
    {
        text: "next time you'll be awake at this hour why not now",
        userIsSender: false,
    },
    {
        text: `Didn't I tell you not to put your phone on charge just because it's the weekend?`,
        userIsSender: false,
    },
    {
        text: "i woke up calmnnn i put it on the charger the phone was turned off next to me i took it out while i was sleeping hsadfkagshdfgsajf i slept early girl i slept at 3",
        userIsSender: true,
    },
    {
        text: "While you win in love, you continue to win in other things dhdhdhdh",
        userIsSender: true,
    },
];

const messagesContainer = useTemplateRef("messages-container");
const { y: messagesContainerScrollY } = useScroll(messagesContainer, {
    behavior: "smooth",
});

onMounted(() => {
    messagesContainerScrollY.value = messagesContainer.value.scrollHeight;
});
</script>
