/**
 * Configuration for the Agentic AI Chat application
 */
const CONFIG = {
    // API endpoints
    API: {
        CHAT: '/api/chat',
        TOOL_RESULTS: '/api/tool-results'
    },
    
    // Timing constants (in milliseconds)
    TIMING: {
        TYPING_DELAY: 30, // Delay between characters for typing effect
        POLL_INTERVAL: 1000 // How often to poll for auto-execution results
    },
    
    // Message display options
    MESSAGES: {
        USE_TYPING_EFFECT: true, // Whether to animate messages with typing effect
        MAX_HISTORY: 100 // Maximum number of messages to keep in the UI
    }
}; 