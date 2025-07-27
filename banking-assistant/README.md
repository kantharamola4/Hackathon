# Conversational AI Banking Assistant

## Overview
A modular conversational AI system for handling dynamic banking interactions such as loan applications, card blocking, and account queries. Supports multi-turn understanding, context management, and real-time task execution.

## Features
- Multi-turn, goal-oriented dialogue
- Context and state management
- Dynamic intent recognition and context switching
- Fallback and clarification logic
- Integration with mock banking APIs

## Setup
1. Install dependencies:
   ```
pip install -r requirements.txt
   ```
2. Run the assistant:
   ```
python main.py
   ```

## Supported Flows & Example Prompts
- **Loan Application**: "I want to apply for a personal loan."
- **Block Card**: "Block my credit card, it's lost."
- **Account Query**: "Show me my last 5 transactions."

## Project Structure
- `main.py`: Entry point
- `assistant/`: Dialogue, context, routing, and flows
- `apis/`: Mock banking APIs
- `docs/`: Architecture and design docs

## Dependencies
- Python 3.8+
- (See `requirements.txt`)
