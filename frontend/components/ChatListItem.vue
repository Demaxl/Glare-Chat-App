<template>
    <nuxt-link
        :to="`/chat/${username}`"
        class="block transition-all hover:bg-gray-200 rounded-lg hover:-m-4 hover:-mr-1 hover:p-4 hover:pr-1"
        exact-active-class="bg-gray-300 -m-4 -mr-1 p-4 pr-1 "
    >
        <div
            class="flex items-center text-glare-gray transition-colors cursor-pointer"
        >
            <div class="flex items-center flex-grow">
                <img
                    class="mr-3 w-9 h-9"
                    src="/images/default_message_icon.png"
                    alt="Message Icon"
                />

                <div class="flex flex-col truncate">
                    <div>
                        <span
                            class="mr-2 text-body-1 font-semibold text-glare-black"
                            >{{
                                messageIsSelf ? `${username} (You)` : username
                            }}</span
                        >

                        <!-- <span class="text-button-3">@suzana</span> -->
                    </div>
                    <p
                        class="text-[10px] leading-4 truncate md:max-w-[250px] max-w-[250px] sm:max-w-[500px]"
                    >
                        <span v-if="userIsSender">You:</span>
                        <span v-if="messageType === 'image'">
                            <Icon
                                name="uil:image"
                                size="15px"
                                class="align-middle"
                            ></Icon>
                            Image
                        </span>
                        <span v-else>{{ message }}</span>
                    </p>
                </div>
            </div>
            <div class="text-[10px] leading-4 pl-2 text-nowrap">
                {{ formattedDate }}
            </div>
        </div>
    </nuxt-link>
</template>

<script setup>
const { timestamp } = defineProps({
    // displayName: String,
    username: String,
    message: String,
    messageIsSelf: Boolean,
    userIsSender: Boolean,
    messageType: String,
    timestamp: String,
});

// Parse the timestamp into a Date object
const date = new Date(timestamp);

// Format the date to "Month day" using Intl.DateTimeFormat
const formattedDate = computed(() => {
    return new Intl.DateTimeFormat("en-US", {
        month: "short", // Short month name (e.g., "Jan", "Feb")
        day: "numeric", // Day of the month
    }).format(date);
});
</script>
