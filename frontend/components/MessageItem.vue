<template>
    <div>
        <div
            class="min-h-16 flex flex-col"
            :class="userIsSender ? 'items-end' : 'items-start'"
        >
            <div :class="classObject" class="max-w-screen-sm">
                <div class="text-body-2 py-4 px-7 lg:px-14">
                    <p v-if="messageType === 'text'">{{ content }}</p>
                    <img
                        v-else
                        class="max-w-[300px] w-full h-auto cursor-pointer"
                        :src="content"
                        alt="Message Icon"
                        @click="showModal = true"
                    />
                </div>
            </div>
        </div>
        <!-- Modal for full-screen image preview -->
        <Transition
            enter-active-class="animate__animated animate__fadeIn animate__faster"
            leave-active-class="animate__animated animate__fadeOut animate__faster"
        >
            <div
                v-show="showModal"
                class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
            >
                <OnClickOutside @trigger="closeModal">
                    <img
                        :src="content"
                        class="max-w-full max-h-full"
                        alt="Full Screen Image"
                    />
                </OnClickOutside>
                <button
                    @click="showModal = false"
                    class="absolute top-4 right-4 text-white"
                >
                    <Icon
                        name="material-symbols:close-rounded"
                        size="24px"
                    ></Icon>
                </button>
            </div>
        </Transition>
    </div>
</template>

<script setup>
import { OnClickOutside } from "@vueuse/components";
const { userIsSender, messageType, content } = defineProps({
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

const showModal = ref(false);

function closeModal() {
    showModal.value = false;
}
</script>
