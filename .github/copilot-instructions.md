# Copilot Instructions for AI Support Ticket System

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Context
This is a minimal, token-efficient AI-powered support ticket system designed for engineering and consulting companies.

## Key Principles
- Prioritize low token usage in all implementations
- Keep responses concise and structured
- Use compressed data formats (JSON, abbreviated keys)
- Implement minimal but functional features only
- Focus on engineering/consulting workflow patterns

## Code Style Guidelines
- Use short, descriptive variable names
- Implement compact data structures
- Prefer functional programming patterns where appropriate
- Include docstrings for AI interaction methods
- Use type hints for better code clarity

## AI Interaction Patterns
- Structured JSON responses for ticket operations
- Abbreviated field names (id, desc, cat, pri, stat)
- Status codes instead of verbose messages
- Batch operations when possible to reduce token count
