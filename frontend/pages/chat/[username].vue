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
                    :messageType="message.messageType"
                />
            </div>
        </div>

        <div
            class="h-16 flex items-center sm:space-x-3 justify-between md:space-x-11 py-5 md:mx-9 absolute right-0 left-0 bottom-0"
        >
            <button
                title="Upload Image"
                class="text-primary p-3 rounded-full hover:bg-[#eee] transition-colors"
                @click="triggerImageUpload"
            >
                <input
                    type="file"
                    ref="fileInput"
                    accept="image/jpeg, image/png, image/gif, image/webp, image/bmp"
                    class="hidden"
                    @change="handleImageSelect"
                />
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
                title="Send Message"
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
const { $axios } = useNuxtApp();
const wsStore = useWebSocketStore();
const { sendWithResponse, send } = wsStore;
const { data } = storeToRefs(wsStore);

const messages = ref([]);
const messageInput = ref(null);

const messageInputRef = useTemplateRef("message-input");
const fileInput = useTemplateRef("fileInput");

const messagesItemDisplay = computed(() => {
    return messages.value.map((message) => {
        let res = {};

        res.content = message.content;
        res.userIsSender = message.sender === userData.username;
        res.messageType = message.message_type;

        return res;
    });
});

async function loadNewMessage(message) {
    messages.value.push(message);
    await nextTick();
    messagesContainerScrollY.value = messagesContainer.value.scrollHeight;
}

// Listen for new messages
watch(data, (newData) => {
    loadNewMessage(newData);
});

function triggerImageUpload() {
    fileInput.value.click();
}

async function handleImageSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Validate that the file is an allowed image type (excluding SVG)
    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "image/bmp",
    ];
    if (!allowedTypes.includes(file.type)) {
        alert(
            "Please select a valid image file (JPEG, PNG, GIF, WebP, or BMP)"
        );
        fileInput.value.value = ""; // Clear the file input
        return;
    }

    // Create FormData to send the image
    const formData = new FormData();
    formData.append("image", file);
    formData.append("receiver", useRoute().params.username);

    // Send the image through axios
    const response = await $axios.post("/api/upload-image", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    // Add the image to the messages
    loadNewMessage(response.data);

    // Send the image through websocket
    send({
        type: "chat.image_message",
        messagePk: response.data.id,
    });

    // Clear the file input for future uploads
    fileInput.value.value = "";
}

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
