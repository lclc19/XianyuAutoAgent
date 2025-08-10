# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
XianyuAutoAgent is an AI-powered customer service automation system for the Xianyu (闲鱼) platform, providing 24/7 intelligent responses, multi-agent coordination, and context-aware conversations.

## Development Commands

### Installation and Setup
```bash
# Clone repository
git clone https://github.com/shaxiu/XianyuAutoAgent.git
cd XianyuAutoAgent

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy .env.example or create new)
cp .env.example .env
# Required: API_KEY, COOKIES_STR, MODEL_BASE_URL, MODEL_NAME
```

### Running the Application
```bash
# Start the main application
python main.py

# Run with custom log level
LOG_LEVEL=INFO python main.py
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t xianyu-agent .
docker-compose up -d
```

## High-Level Architecture

### Core Components

1. **WebSocket Connection Layer** (`main.py:XianyuLive`)
   - Maintains persistent WebSocket connection to Xianyu platform
   - Handles heartbeat mechanism (15s interval)
   - Token refresh management (1h default)
   - Message encryption/decryption using `utils/xianyu_utils.py`

2. **Multi-Agent System** (`XianyuAgent.py`)
   - **IntentRouter**: Routes messages to appropriate agents based on keywords/patterns
   - **ClassifyAgent**: Intent classification using LLM
   - **PriceAgent**: Handles price negotiations with dynamic temperature
   - **TechAgent**: Technical consultation with web search capability
   - **DefaultAgent**: General conversation handler

3. **Context Management** (`context_manager.py`)
   - SQLite-based conversation history storage
   - Per-chat-session context tracking
   - Bargain count tracking for pricing negotiations
   - Item information caching

4. **API Integration** (`XianyuApis.py`)
   - Token acquisition and refresh
   - Item information retrieval
   - Cookie management with auto-update to .env

### Message Flow

1. **Incoming Message**: WebSocket → Decrypt → Parse message type
2. **Processing**: 
   - Extract user/item/chat IDs
   - Check manual mode status (toggle with configured keyword)
   - Retrieve item info (cache or API)
   - Get conversation context from SQLite
3. **Response Generation**:
   - Intent detection (rule-based → LLM fallback)
   - Agent selection and reply generation
   - Context update and persistence
4. **Outgoing**: Format → Encrypt → Send via WebSocket

### Key Features

- **Manual Override**: Sellers can toggle manual mode using configured keywords (default: "。")
- **Message Filtering**: 5-minute message expiry, system message filtering
- **Safety Module**: Blocks sensitive information (微信, QQ, 支付宝, etc.)
- **Dynamic Pricing**: Bargain count tracking with temperature adjustment
- **Persistent Storage**: SQLite for conversation history and item cache

## Environment Variables

```bash
# Required
API_KEY=                  # LLM API key
COOKIES_STR=             # Xianyu web cookies
MODEL_BASE_URL=          # Default: Alibaba DashScope
MODEL_NAME=              # Default: qwen-max

# Optional
TOGGLE_KEYWORDS=         # Manual mode toggle (default: "。")
HEARTBEAT_INTERVAL=15    # WebSocket heartbeat interval
TOKEN_REFRESH_INTERVAL=3600  # Token refresh interval
MANUAL_MODE_TIMEOUT=3600 # Manual mode auto-exit timeout
MESSAGE_EXPIRE_TIME=300000  # Message expiry (5 min)
LOG_LEVEL=DEBUG         # Logging level
```

## Database Structure

The system uses SQLite (`data/chat_history.db`) with tables:
- `messages`: Conversation history with chat_id indexing
- `chat_bargain_counts`: Per-session bargain tracking
- `item_info`: Cached item details

## Prompts

Located in `prompts/` directory:
- `classify_prompt.txt`: Intent classification rules
- `price_prompt.txt`: Pricing negotiation strategy
- `tech_prompt.txt`: Technical consultation guidelines
- `default_prompt.txt`: General conversation handling

## Security Considerations

- Never commit `.env` file with real credentials
- Cookies auto-refresh mechanism updates `.env` file
- Message encryption/decryption for platform communication
- Automatic filtering of sensitive contact information

## Common Issues

1. **Cookie Expiry**: System will exit if cookies invalid - update COOKIES_STR
2. **Token Refresh**: Automatic refresh every hour with reconnection
3. **Connection Loss**: Auto-reconnect with 5-second delay
4. **Manual Mode**: Use toggle keyword to switch between AI/manual responses