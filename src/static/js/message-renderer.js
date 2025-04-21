/**
 * Message renderer for displaying chat messages
 */
class MessageRenderer {
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        if (!this.container) {
            throw new Error(`Message container not found: ${containerSelector}`);
        }
    }
    
    /**
     * Add a user message to the chat
     * 
     * @param {string} message - The message content
     */
    addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = message;
        
        this.container.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    /**
     * Add an assistant message to the chat
     * 
     * @param {string} message - The message content
     * @param {boolean} useTypingEffect - Whether to use typing effect
     */
    async addAssistantMessage(message, useTypingEffect = CONFIG.MESSAGES.USE_TYPING_EFFECT) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message assistant-message';
        
        // Process Markdown in the message (simple handling)
        const formattedMessage = this.formatMessage(message);
        
        if (useTypingEffect) {
            this.container.appendChild(messageElement);
            await this.animateTyping(messageElement, formattedMessage);
        } else {
            messageElement.innerHTML = formattedMessage;
            this.container.appendChild(messageElement);
        }
        
        this.scrollToBottom();
    }
    
    /**
     * Format a message with basic Markdown-like syntax
     * 
     * @param {string} message - The raw message content
     * @returns {string} - The formatted HTML
     */
    formatMessage(message) {
        // Handle code blocks
        let formatted = message.replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>');
        
        // Handle inline code
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Handle links
        formatted = formatted.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        // Handle bold
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Handle italics
        formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // Handle newlines
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    }
    
    /**
     * Animate typing effect for a message
     * 
     * @param {HTMLElement} element - The message element
     * @param {string} text - The formatted HTML content
     */
    async animateTyping(element, text) {
        // For HTML content, we need to handle tags differently
        let inTag = false;
        let currentText = '';
        
        for (let i = 0; i < text.length; i++) {
            const char = text[i];
            
            // Check if we're inside an HTML tag
            if (char === '<') {
                inTag = true;
            }
            
            // Append the character
            currentText += char;
            
            // If not in a tag, add a delay
            if (!inTag) {
                element.innerHTML = currentText;
                await new Promise(resolve => setTimeout(resolve, CONFIG.TIMING.TYPING_DELAY));
            }
            
            // Check if we're exiting a tag
            if (char === '>') {
                inTag = false;
                element.innerHTML = currentText;
            }
        }
    }
    
    /**
     * Scroll the conversation container to the bottom
     */
    scrollToBottom() {
        this.container.scrollTop = this.container.scrollHeight;
    }
    
    /**
     * Clear all messages from the container
     */
    clearMessages() {
        this.container.innerHTML = '';
    }
}

// Create a singleton instance
const messageRenderer = new MessageRenderer('#conversation'); 