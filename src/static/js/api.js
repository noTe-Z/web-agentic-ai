/**
 * API client for interacting with the Agentic AI Chat backend
 */
class ApiClient {
    /**
     * Send a message to the chat API
     * 
     * @param {string} message - The message content to send
     * @param {string|null} conversationId - The conversation ID (optional)
     * @returns {Promise<Object>} - The API response
     */
    async sendMessage(message, conversationId = null) {
        try {
            const response = await fetch(CONFIG.API.CHAT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: [
                        {
                            role: 'user',
                            content: message
                        }
                    ],
                    conversation_id: conversationId
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(`API error: ${response.status} - ${errorData.detail || response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }
    
    /**
     * Send tool results to the API
     * 
     * @param {string} conversationId - The conversation ID
     * @param {Array<Object>} toolResults - The results of tool executions
     * @returns {Promise<Object>} - The API response
     */
    async sendToolResults(conversationId, toolResults) {
        try {
            const response = await fetch(CONFIG.API.TOOL_RESULTS, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    tool_results: toolResults
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(`API error: ${response.status} - ${errorData.detail || response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error sending tool results:', error);
            throw error;
        }
    }
}

// Create a singleton instance
const apiClient = new ApiClient(); 