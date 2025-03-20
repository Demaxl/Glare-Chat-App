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
                    <span class="text-body-1 font-semibold text-glare-black">{{
                        useRoute().params.username
                    }}</span>
                    <span class="text-caption text-glare-gray"
                        >@{{ useRoute().params.username }}</span
                    >
                </div>
            </div>
        </div>
        <div
            ref="messages-container"
            class="overflow-y-auto h-[80vh] pb-10 glare-scrollbar pr-3 md:pr-9"
        >
            <div class="space-y-2 pt-16">
                <MessageItem
                    v-for="message in messagesItemDisplay"
                    :key="message.id"
                    :content="message.content"
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
                ref="message-input"
                type="text"
                class="shadow-[0px_0px_1px_0px_#00000040] focus:outline-primary border block grow rounded-3xl px-6 py-3 h-10 max-w-[850px] text-body-2"
                placeholder="Type a messsage"
                v-model="messageInput"
                @keyup.enter="sendMessage"
            />

            <button
                class="text-primary p-3 rounded-full hover:bg-[#eee] transition-colors"
                @click="sendMessage"
            >
                <Icon class="align-middle" name="iconoir:send" size="24px" />
            </button>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    layout: "chat",
});

const { userData } = useAuthStore();
const messagesContainer = useTemplateRef("messages-container");
const { y: messagesContainerScrollY } = useScroll(messagesContainer, {
    behavior: "smooth",
});
const wsStore = useWebSocketStore();
const { sendWithResponse, send } = wsStore;
const { data } = storeToRefs(wsStore);

const messages = ref([]);
const messageInput = ref(null);

const messageInputRef = useTemplateRef("message-input");

const messagesItemDisplay = computed(() => {
    return messages.value.map((message) => {
        let res = {};

        switch (message.message_type) {
            case "text":
                res.content = message.content;
                res.userIsSender = message.sender === userData.username;
                res.messageType = "text";
                break;
            default:
                break;
        }

        return res;
    });
});

function sendMessage() {
    if (messageInput.value) {
        send({
            type: "chat.message",
            receiver: useRoute().params.username,
            message: messageInput.value,
        });
        messageInput.value = "";
    }
}

// Listen for new messages
watch(data, async (newData) => {
    messages.value.push(newData);
    await nextTick();
    messagesContainerScrollY.value = messagesContainer.value.scrollHeight;
});

onMounted(async () => {
    const initialMessages = await sendWithResponse({
        type: "chat.initial_messages",
        receiver: useRoute().params.username,
    });
    messages.value = initialMessages.initial_messages;
    await nextTick();
    messagesContainerScrollY.value = messagesContainer.value.scrollHeight;

    messageInputRef.value.focus();
});
</script>
