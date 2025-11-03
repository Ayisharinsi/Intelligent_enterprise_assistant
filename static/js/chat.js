// chat.js
document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const messageInput = document.getElementById('messageInput');
  const messages = document.getElementById('messages');
  const sendBtn = document.getElementById('sendBtn');
  const statusText = document.getElementById('statusText');

  // Quick prompt buttons
  document.querySelectorAll('.chip').forEach(btn => {
    btn.addEventListener('click', () => {
      messageInput.value = btn.dataset.prompt;
      sendMessage();
    });
  });

  // Send on Enter
  messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage();
  });

  function appendMessage(text, sender='bot') {
    const div = document.createElement('div');
    div.className = 'msg ' + (sender === 'user' ? 'user' : 'bot');
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    messageInput.value = '';
    sendBtn.disabled = true;
    statusText.textContent = 'Thinking...';

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
      });

      const data = await res.json();
      const reply = data.reply || 'No response from AI.';
      appendMessage(reply, 'bot');
      statusText.textContent = 'Local AI';
    } catch (err) {
      console.error('Chat error', err);
      appendMessage('⚠️ Could not reach the AI service. Make sure the local model is running.', 'bot');
      statusText.textContent = 'Disconnected';
    } finally {
      sendBtn.disabled = false;
    }
  }

  // Optional: logout button (goes to login)
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      window.location.href = '/';
    });
  }
});
