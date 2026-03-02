document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const uploadForm = document.getElementById('upload-form');
    const chatHistory = document.getElementById('chat-history');
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const imageModal = document.getElementById('image-modal');
    const closeModal = document.getElementById('close-modal');
    const gateContainer = document.getElementById('gate-container');
    const gates = document.getElementsByClassName('.gate');
    const container = document.querySelector('.container');


    chatHistory.scrollTop = chatHistory.scrollHeight;

    setTimeout(() => {
        gateContainer.classList.add("gate-open");
    }, 500);

    setTimeout(() => {
        gateContainer.style.display = "none";
        container.style.display = "block";
    }, 2000);
    


    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(chatForm);
        try {
            const response = await fetch("/generate", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            appendChatEntry(data);
            chatForm.reset();
        } catch (error) {
            console.error(error);
        }
    });

    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(uploadForm);
        try {
            const response = await fetch("/generate_with_image", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            appendChatEntry(data);
            uploadForm.reset();
            imagePreview.style.display = "none";
        } catch (error) {
            console.error(error);
        }
    });

    function appendChatEntry(entry) {
        const chatEntryDiv = document.createElement("div");
        chatEntryDiv.classList.add("chat-entry");
        chatEntryDiv.innerHTML = `
            <p><strong>You:</strong> ${entry.user}</p>
            <p><strong>AI:</strong><pre> ${entry.bot}</pre></p>
        `;
        chatHistory.appendChild(chatEntryDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    closeModal.onclick = function() {
        imageModal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == imageModal) {
            imageModal.style.display = "none";
        }
    }
});
const chatContainer = document.querySelector('.chat-history-container');

let isDown = false;
let startX;
let scrollLeft;

// Mouse down event
chatContainer.addEventListener('mousedown', (e) => {
    isDown = true;
    chatContainer.classList.add('active');
    startX = e.pageX - chatContainer.offsetLeft;
    scrollLeft = chatContainer.scrollLeft;
});

// Mouse leave event
chatContainer.addEventListener('mouseleave', () => {
    isDown = false;
    chatContainer.classList.remove('active');
});

// Mouse up event
chatContainer.addEventListener('mouseup', () => {
    isDown = false;
    chatContainer.classList.remove('active');
});

// Mouse move event
chatContainer.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - chatContainer.offsetLeft;
    const walk = (x - startX) * 2; // The multiplier controls the scroll speed
    chatContainer.scrollLeft = scrollLeft - walk;
});


