<template>
    <nuxt-link to="/chat" class="block">
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
                            >{{ username }}</span
                        >
                        <!-- <span class="text-button-3">@suzana</span> -->
                    </div>
                    <p
                        class="text-[10px] leading-4 truncate md:max-w-[250px] max-w-[250px] sm:max-w-[500px]"
                    >
                        <!-- Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Itaque dicta id, est quaerat, ea perspiciatis suscipit
                        quas, quis quisquam magnam aspernatur officiis. Esse
                        harum tempore eum consequuntur consectetur itaque dolore
                        saepe quos, tempora illum magni modi reprehenderit
                        beatae officia vel officiis fugit asperiores ratione!
                        Exercitationem, voluptatum deserunt nisi hic corrupti
                        qui modi, quis accusantium accusamus provident
                        voluptatibus dolore, dicta commodi quos earum! Sed
                        doloribus rerum fugit? Quisquam nobis iusto similique
                        minima amet reiciendis sed, quae, optio numquam error ad
                        est magnam! Mollitia qui veniam porro assumenda non
                        delectus officia. Molestiae deleniti soluta pariatur
                        veniam voluptate aspernatur, laboriosam possimus
                        eligendi sed. -->
                        <span v-if="userIsSender">You:</span> {{ message }}
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
    userIsSender: Boolean,
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
