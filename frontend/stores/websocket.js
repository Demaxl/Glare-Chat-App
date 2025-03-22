export const useWebSocketStore = defineStore("websocket", () => {
    const {
        public: { websocketURL },
    } = useRuntimeConfig();

    // Contains the latest cleaned data from the websocket
    const messageData = ref(null);

    // Add a new map to store message promises
    const messagePromises = new Map();
    let messageCounter = 1;

    // Add message handler to websocket options
    const {
        status,
        data: wsData,
        send: wsSend,
        open,
        close,
    } = useWebSocket(websocketURL, {
        immediate: false,
        autoReconnect: {
            retries: 3,
            delay: 1000,
            onFailed() {
                alert(
                    "Unable to connect to server. Please check your network connection and refresh."
                );
            },
        },
        onMessage() {
            const response = deserialize(wsData.value);

            // Resolve the promise if we have a matching messageId
            if (response.messageId && messagePromises.has(response.messageId)) {
                // console.log("Yes");

                const { resolve } = messagePromises.get(response.messageId);
                resolve(response);
                messagePromises.delete(response.messageId);
            }
        },
    });

    watch(wsData, (newData) => {
        // Update the cleaned data state with new data from the websocket
        let cleaned = deserialize(newData);

        switch (cleaned.type) {
            case "chat.message":
                messageData.value = cleaned;
                break;

            default:
                break;
        }
    });

    // Helper function to deserialize the websocket response message
    function deserialize(message) {
        return JSON.parse(message);
    }

    // Modified serialize function to include a message ID and accept any parameters
    function serialize({ type = "chat.message", ...params } = {}) {
        const messageId = messageCounter++;
        const payload = { type, messageId, ...params };

        // Remove specific case handling since we're now passing all params directly
        return { messageId, serialized: JSON.stringify(payload) };
    }

    function send({ type = "chat.message", ...params } = {}) {
        let { serialized } = serialize({ type, ...params });
        wsSend(serialized);
    }

    // New async send function that returns a promise
    async function sendWithResponse({ type = "chat.message", ...params } = {}) {
        const { messageId, serialized } = serialize({
            type,
            ...params,
        });

        const messagePromise = new Promise((resolve, reject) => {
            // Store the promise callbacks
            messagePromises.set(messageId, { resolve, reject });

            // Set a timeout to clean up if no response is received
            setTimeout(() => {
                if (messagePromises.has(messageId)) {
                    const { reject } = messagePromises.get(messageId);
                    reject(new Error("WebSocket response timeout"));
                    messagePromises.delete(messageId);
                }
            }, 5000); // 5 second timeout
        });

        // Send the actual message
        wsSend(serialized);

        // Return the promise
        return messagePromise;
    }

    return {
        send,
        sendWithResponse,
        open,
        data: messageData,
        close,
    };
});
