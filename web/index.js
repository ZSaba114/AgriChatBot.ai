$(document).ready(function() {
    const chatPanel = $("#chatPanel");
    const form = $("#chatbot-form");
    const inputField = $("#messageText");
    const clearBtn = $("#chatbot-form-btn-clear");
    const voiceCheckbox = $("#voiceReadingCheckbox");

    // ============================
    // Function to append a message
    // ============================
    function appendMessage(message, sender) {
        const msgDiv = $("<div>").addClass("message");
        if(sender === "user") {
            msgDiv.addClass("user-message").text(message);
        } else {
            msgDiv.addClass("bot-message").text(message);
            // Voice reading if enabled
            if(voiceCheckbox.is(":checked") && 'speechSynthesis' in window){
                const utterance = new SpeechSynthesisUtterance(message);
                window.speechSynthesis.speak(utterance);
            }
        }
        chatPanel.append(msgDiv);
        chatPanel.scrollTop(chatPanel[0].scrollHeight); // Scroll to bottom
    }

    // ============================
    // Handle form submission
    // ============================
    form.on("submit", function(e) {
        e.preventDefault();
        const message = inputField.val().trim();
        if(message === "") return;

        appendMessage(message, "user"); // Display user message
        inputField.val(""); // Clear input

        // Send message to Flask backend
        $.ajax({
            url: "/ask",
            type: "POST",
            data: { messageText: message },
            success: function(data) {
                const answer = data.answer || "Sorry, I didn't get that.";
                appendMessage(answer, "bot");
            },
            error: function(err) {
                appendMessage("Error: Could not reach the server.", "bot");
                console.error(err);
            }
        });
    });

    // ============================
    // Clear chat
    // ============================
    clearBtn.on("click", function() {
        chatPanel.empty();
    });

    // ============================
    // Optional: Voice input (microphone)
    // ============================
    const voiceBtn = $("#chatbot-form-btn-voice");
    if('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        voiceBtn.on("click", function() {
            recognition.start();
        });

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            inputField.val(transcript);
            form.submit();
        };

        recognition.onerror = function(event) {
            console.error("Speech recognition error:", event.error);
        };
    } else {
        voiceBtn.hide(); // hide button if browser doesn't support
    }
});
