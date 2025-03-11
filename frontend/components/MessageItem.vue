<template>
    <div
        class="min-h-16 flex flex-col"
        :class="userIsSender ? 'items-end' : 'items-start'"
    >
        <div :class="classObject" class="max-w-screen-sm">
            <p class="text-body-2 py-4 px-7 lg:px-14">
                {{ content }}
            </p>
        </div>
    </div>
</template>

<script setup>
const { userIsSender } = defineProps({
    content: String,
    userIsSender: Boolean,
    messageType: String,
});

const classObject = computed(() => [
    userIsSender ? "bg-primary" : "bg-[#F5F5F5]",
    userIsSender ? "text-glare-white" : "text-glare-black",
    userIsSender ? "rounded-l-2xl" : "rounded-r-2xl",
    userIsSender ? "ml-10" : "mr-10",
]);
</script>
