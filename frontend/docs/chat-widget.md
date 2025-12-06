# Chat Widget Component

The Chat Widget is an interactive component that provides AI-powered assistance for the Physical AI & Humanoid Robotics Textbook.

## Overview

The Chat Widget appears as a floating button in the bottom-right corner of the screen. When clicked, it opens a chat window that allows users to ask questions about the textbook content and receive AI-generated responses based on the textbook material.

## Features

- **Floating Button**: Unobtrusive design that doesn't interfere with reading
- **Real-time Chat**: Instant responses to user queries
- **Source Attribution**: Responses include citations to relevant textbook sections
- **Mobile Responsive**: Works well on all device sizes
- **Accessibility**: Keyboard navigation and screen reader support

## Usage

The chat widget is integrated into the Docusaurus layout and will appear on all textbook pages.

## How It Works

1. User clicks the floating chat button
2. Chat window opens with a welcome message
3. User types a question about the textbook content
4. Question is sent to the backend API
5. Backend searches vector database for relevant content
6. AI generates response based on retrieved content
7. Response is displayed in the chat window with source citations

## API Integration

The widget communicates with the backend API at `http://localhost:8000/api/v1/chat/` to process queries and receive responses.