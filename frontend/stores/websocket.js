export const useWebSocketStore = defineStore("websocket", () => {
    const {
        public: { websocketURL },
    } = useRuntimeConfig();

    // Current status of websocket instance
    const status = ref(null);

    // Holds the data returned from the server
    const data = ref(null);

    // Add a new map to store message promises
    const messagePromises = new Map();
    let messageCounter = 1;

    // Add message handler to websocket options
    const {
        status: wsStatus,
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
            // console.log(response);
            // console.log(messagePromises);
            // console.log(response.messageId);
            // console.log(messagePromises);

            // Resolve the promise if we have a matching messageId
            if (response.messageId && messagePromises.has(response.messageId)) {
                // console.log("Yes");

                const { resolve } = messagePromises.get(response.messageId);
                resolve(response);
                messagePromises.delete(response.messageId);
            }
        },
    });

    // Update local refs when websocket values change
    watch(wsStatus, (newStatus) => {
        status.value = newStatus;
    });

    watch(wsData, (newData) => {
        data.value = newData;
    });

    // Helper function to deserialize the websocket response message
    function deserialize(message) {
        return JSON.parse(message);
    }

    // Modified serialize function to include a message ID
    function serialize(type = "chat.message", receiver = null, message = null) {
        const messageId = messageCounter++;
        const payload = { type, messageId };
        switch (type) {
            case "chat.message":
                payload.message = message;
                payload.receiver = receiver;
                break;
            case "chat.initial_messages":
                payload.receiver = receiver;
                break;
            default:
                break;
        }
        return { messageId, serialized: JSON.stringify(payload) };
    }

    function send(type = "chat.message", receiver = null, message = null) {
        wsSend(serialize(type, message, receiver));
    }

    // New async send function that returns a promise
    async function sendWithResponse(
        type = "chat.message",
        receiver = null,
        message = null
    ) {
        const { messageId, serialized } = serialize(type, receiver, message);

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
        send: wsSend,
        sendWithResponse,
        open,
        data,
        status,
        close,
    };
});
