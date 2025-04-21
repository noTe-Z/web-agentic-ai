/**
 * Main application module for Agentic AI Chat
 */
class App {
    constructor() {
        // Elements
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.conversationIdElement = document.getElementById('conversation-id');
        this.connectionStatusElement = document.getElementById('connection-status');
        
        // State
        this.conversationId = null;
        this.isProcessing = false;
        
        // Initialize
        this.init();
    }
    
    /**
     * Initialize the application
     */
    init() {
        // Add event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                this.sendMessage();
            }
        });
        
        // Focus the input
        this.userInput.focus();
        
        // Set initial status
        this.updateStatus('connected');
    }
    
    /**
     * Send a user message to the API
     */
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isProcessing) {
            return;
        }
        
        try {
            // Update UI state
            this.isProcessing = true;
            this.userInput.disabled = true;
            this.sendButton.disabled = true;
            
            // Add message to UI
            messageRenderer.addUserMessage(message);
            
            // Clear input
            this.userInput.value = '';
            
            // Send to API
            this.updateStatus('sending');
            const response = await apiClient.sendMessage(message, this.conversationId);
            
            // Update conversation ID
            if (response.conversation_id) {
                this.conversationId = response.conversation_id;
                this.conversationIdElement.textContent = `Conversation: ${this.conversationId.substring(0, 8)}...`;
            }
            
            // Handle response
            if (response.message) {
                await messageRenderer.addAssistantMessage(response.message.content);
            }
            
            // Handle tool calls
            if (response.tool_calls && response.tool_calls.length > 0) {
                toolHandler.displayToolCalls(response.tool_calls, this.conversationId);
            }
            
            this.updateStatus('connected');
        } catch (error) {
            console.error('Error in send message flow:', error);
            messageRenderer.addAssistantMessage(`Error: ${error.message}`);
            this.updateStatus('error');
        } finally {
            // Reset UI state
            this.isProcessing = false;
            this.userInput.disabled = false;
            this.sendButton.disabled = false;
            this.userInput.focus();
        }
    }
    
    /**
     * Update the connection status display
     * 
     * @param {string} status - The status to display (connected, sending, error)
     */
    updateStatus(status) {
        switch (status) {
            case 'connected':
                this.connectionStatusElement.textContent = 'Connected';
                this.connectionStatusElement.style.color = '#10b981';
                break;
            case 'sending':
                this.connectionStatusElement.textContent = 'Sending...';
                this.connectionStatusElement.style.color = '#3b82f6';
                break;
            case 'error':
                this.connectionStatusElement.textContent = 'Error';
                this.connectionStatusElement.style.color = '#ef4444';
                break;
            default:
                this.connectionStatusElement.textContent = status;
        }
    }
    
    /**
     * Clear the conversation and start a new one
     */
    clearConversation() {
        messageRenderer.clearMessages();
        toolHandler.clearToolCalls();
        this.conversationId = null;
        this.conversationIdElement.textContent = 'New conversation';
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
}); 