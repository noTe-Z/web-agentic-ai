/**
 * Tool handler for managing tool calls and results
 */
class ToolHandler {
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        if (!this.container) {
            throw new Error(`Tool container not found: ${containerSelector}`);
        }
        
        this.pendingToolCalls = new Map();
    }
    
    /**
     * Display tool calls from the API response
     * 
     * @param {Array<Object>} toolCalls - The tool calls from the API
     * @param {string} conversationId - The conversation ID
     */
    displayToolCalls(toolCalls, conversationId) {
        if (!toolCalls || toolCalls.length === 0) {
            this.hideToolSection();
            return;
        }
        
        // Store pending tool calls for later reference
        toolCalls.forEach(toolCall => {
            this.pendingToolCalls.set(toolCall.id, {
                ...toolCall,
                conversationId
            });
        });
        
        // Show the tool section
        this.showToolSection();
        
        // Clear existing tool calls
        this.container.innerHTML = '';
        
        // Create elements for each tool call
        toolCalls.forEach(toolCall => {
            const toolCallElement = document.createElement('div');
            toolCallElement.className = 'tool-call';
            toolCallElement.id = `tool-call-${toolCall.id}`;
            
            // Format the tool call display
            toolCallElement.innerHTML = `
                <h3>${toolCall.name}</h3>
                <div class="tool-input">
                    <strong>Input:</strong>
                    <pre>${JSON.stringify(toolCall.input, null, 2)}</pre>
                </div>
                <div class="tool-result-container" id="result-${toolCall.id}">
                    <textarea 
                        class="tool-result-input" 
                        placeholder="Enter the result of this tool call..."
                        rows="4"
                    ></textarea>
                </div>
                <div class="tool-actions">
                    <button class="tool-button submit-result" data-tool-id="${toolCall.id}">
                        Submit Result
                    </button>
                </div>
            `;
            
            this.container.appendChild(toolCallElement);
            
            // Add event listener for the submit button
            const submitButton = toolCallElement.querySelector('.submit-result');
            submitButton.addEventListener('click', () => this.handleToolResult(toolCall.id));
        });
    }
    
    /**
     * Handle submitting a tool result
     * 
     * @param {string} toolCallId - The ID of the tool call
     */
    async handleToolResult(toolCallId) {
        const toolCall = this.pendingToolCalls.get(toolCallId);
        if (!toolCall) {
            console.error(`Tool call not found: ${toolCallId}`);
            return;
        }
        
        const resultContainer = document.querySelector(`#result-${toolCallId}`);
        const resultInput = resultContainer.querySelector('.tool-result-input');
        const resultValue = resultInput.value.trim();
        
        if (!resultValue) {
            alert('Please enter a result for this tool call.');
            return;
        }
        
        try {
            // Update UI to show loading state
            const submitButton = document.querySelector(`.submit-result[data-tool-id="${toolCallId}"]`);
            submitButton.textContent = 'Submitting...';
            submitButton.disabled = true;
            
            // Send the result to the API
            const response = await apiClient.sendToolResults(toolCall.conversationId, [
                {
                    tool_call_id: toolCallId,
                    result: resultValue
                }
            ]);
            
            // Display the result in the UI
            resultContainer.innerHTML = `
                <div class="tool-result">
                    <strong>Result:</strong>
                    <pre>${resultValue}</pre>
                </div>
            `;
            
            // Remove the pending tool call
            this.pendingToolCalls.delete(toolCallId);
            
            // If there are no more pending tool calls, hide the tool section
            if (this.pendingToolCalls.size === 0) {
                this.hideToolSection();
            }
            
            // Process the response message
            if (response.message) {
                await messageRenderer.addAssistantMessage(response.message.content);
            }
            
            // Handle any new tool calls in the response
            if (response.tool_calls && response.tool_calls.length > 0) {
                this.displayToolCalls(response.tool_calls, response.conversation_id);
            }
            
        } catch (error) {
            console.error('Error submitting tool result:', error);
            alert(`Error submitting result: ${error.message}`);
            
            // Restore the UI state
            const submitButton = document.querySelector(`.submit-result[data-tool-id="${toolCallId}"]`);
            submitButton.textContent = 'Submit Result';
            submitButton.disabled = false;
        }
    }
    
    /**
     * Show the tool section
     */
    showToolSection() {
        this.container.classList.add('active');
    }
    
    /**
     * Hide the tool section
     */
    hideToolSection() {
        this.container.classList.remove('active');
    }
    
    /**
     * Check if there are any pending tool calls
     * 
     * @returns {boolean} - True if there are pending tool calls
     */
    hasPendingToolCalls() {
        return this.pendingToolCalls.size > 0;
    }
    
    /**
     * Clear all tool calls from the container
     */
    clearToolCalls() {
        this.container.innerHTML = '';
        this.pendingToolCalls.clear();
        this.hideToolSection();
    }
}

// Create a singleton instance
const toolHandler = new ToolHandler('#tool-section'); 