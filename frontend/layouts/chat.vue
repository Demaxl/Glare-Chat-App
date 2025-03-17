<template>
    <div class="w-full">
        <div class="flex h-screen">
            <div
                :class="{ 'hidden md:flex': isChatView, flex: !isChatView }"
                class="bg-[#FAFAFA] basis-full flex-col justify-between md:max-w-[400px] md:basis-1/4 p-6 pr-2 relative"
            >
                <div>
                    <nuxt-link to="/">
                        <Icon
                            name="icon:logo"
                            class="w-[150px] block h-[43px] mb-[88px]"
                        />
                    </nuxt-link>
                    <p class="text-subtitle-1 font-semibold mb-7 text-black">
                        Messages
                    </p>
                    <div class="pr-6 mb-10 relative">
                        <Icon
                            name="icon:search"
                            class="block absolute top-3 left-4"
                        />
                        <input
                            ref="searchInput"
                            class="mx-auto text-button-2 block w-full rounded-3xl border placeholder:text-[#C7C3C3] border-[#E8E8E8] py-3 pl-14 pr-9"
                            type="text"
                            placeholder="Search people"
                            @input="debouncedUserSearch"
                            v-model="searchQuery"
                        />
                    </div>
                    <!-- <div class="space-y-6"> -->
                    <TransitionGroup name="list" tag="div" class="space-y-6">
                        <ChatListItem
                            v-for="(message, index) in recentContacts"
                            :key="index"
                            v-bind="message"
                        />
                    </TransitionGroup>
                    <!-- </div> -->
                </div>
                <div class="flex justify-between relative items-center">
                    <div class="flex">
                        <img
                            class="w-9 h-9 mr-3"
                            src="/images/default_message_icon.png"
                            alt="User profile picture"
                        />
                        <div class="flex flex-col">
                            <span
                                class="text-body-1 font-semibold text-glare-black"
                                >{{ userData.username }}</span
                            >
                            <span class="text-caption text-glare-gray"
                                >@{{ userData.username }}</span
                            >
                        </div>
                    </div>
                    <button
                        :class="{
                            'bg-[#eee]': isProfileDropdownOpen,
                            'bg-transparent': !isProfileDropdownOpen,
                        }"
                        class="p-2 font-bold hover:bg-[#eee] rounded transition-colors"
                        @click="toggleDropdown()"
                    >
                        <Icon
                            class="align-middle"
                            name="iconoir:more-horiz"
                            size="24px"
                        />
                    </button>
                    <Transition
                        enter-active-class="animate__animated animate__fadeInUp "
                        leave-active-class="animate__animated animate__fadeOutDown"
                    >
                        <div
                            v-show="isProfileDropdownOpen"
                            class="absolute right-0 rounded-lg z-10 -top-[110%] border border-[#E8E8E8] shadow-[0px_4px_4px_0px_#0000000A]"
                        >
                            <nuxt-link
                                to="/logout"
                                class="text-red-600 block p-3 rounded font-bold transition-colors hover:bg-[#eee] text-button-3"
                            >
                                Sign out
                            </nuxt-link>
                        </div>
                    </Transition>
                </div>
            </div>
            <div
                :class="{ hidden: !isChatView, 'basis-full': isChatView }"
                class="md:block md:basis-3/4"
            >
                <slot />
            </div>
        </div>
    </div>
</template>

<script setup>
const route = useRoute();
const isChatView = computed(() => route.name === "chat-username");
const [isProfileDropdownOpen, toggleDropdown] = useToggle(false);
const { searchInput } = useSearchFocus();

const { userData } = useAuthStore();

const recentMessages = ref([]);
// Goes through all recent messages to return the list of recently contacted users
const recentContacts = computed(() => {
    // console.log(recentMessages.value);

    const contacts = [];
    const chosen = new Set();

    let username;
    let userIsSender;
    for (const message of recentMessages.value) {
        // Get the username of the user that is not the current user
        if (message.sender !== userData.username) {
            // User received the message
            username = message.sender;
            userIsSender = false;
        } else {
            // User sent the message
            username = message.receiver;
            userIsSender = true;
        }

        // If the username is already in the list, skip it
        if (chosen.has(username)) continue;

        // Flag to check if the message is sent by the current user (a self message)
        let messageIsSelf = message.sender === message.receiver ? true : false;

        contacts.push({
            username,
            userIsSender,
            messageIsSelf,
            message: message.content,
            timestamp: message.timestamp,
        });
        chosen.add(username);
    }
    return contacts;
});

const searchQuery = ref(null);

const wsStore = useWebSocketStore();
const { sendWithResponse, open } = wsStore;
const { data } = storeToRefs(wsStore);

// Get recent messages of user after connection
async function getRecentMessages() {
    try {
        const response = await sendWithResponse({
            type: "chat.recent_messages",
        });
        recentMessages.value = response.recent_messages;
    } catch (error) {
        console.error("Failed to get recent messages:", error);
    }
}

async function search() {
    try {
        const response = await sendWithResponse({
            type: "chat.search",
            query: searchQuery.value,
        });
        recentMessages.value = response.users.map((user) => {
            if (!user.latest_message) {
                return {
                    sender: user.username,
                    receiver: userData.username,
                    content: "Start new chat",
                    timestamp: new Date().toISOString(),
                };
            }
            return user.latest_message;
        });
    } catch (error) {
        console.error("Failed to search for user:", error);
    }
}

const debouncedUserSearch = useDebounceFn(() => {
    // If the search query is empty, get recent messages
    if (searchQuery.value) {
        search();
    } else {
        getRecentMessages();
    }
}, 500);

// Listen for new messages
watch(data, (newData) => {
    recentMessages.value.unshift(newData);
});

onMounted(() => {
    // Open the websocket connection
    open();
    getRecentMessages();
});
</script>

<style scoped>
.nuxt-icon svg {
    margin-bottom: 0;
    width: auto;
    height: auto;
}

.animate__animated {
    --animate-duration: 0.3s;
}
.list-move, /* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
    transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateX(30px);
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
    position: absolute;
}
</style>
