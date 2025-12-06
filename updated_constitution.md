<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Added sections: Mobile-First Design, Spec-Driven Development, Tech Stack Requirements sections
Removed sections: None
Modified principles: Added new principles and refined existing ones to align with user requirements
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending (check for references)
  - README.md ⚠ pending (if exists)
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Modular Architecture
All components must be designed as independent, reusable modules with clear interfaces. Code must be organized into distinct layers (frontend, backend, data processing) that can be developed, tested, and deployed separately. This ensures maintainability and allows for parallel development.

### II. Documentation-First Approach
Every feature and component must be documented before implementation. Docusaurus serves as the primary documentation platform, and all code changes must include corresponding documentation updates. This ensures the textbook remains comprehensive and accessible.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All backend APIs, RAG functionality, and frontend components must have comprehensive test coverage before deployment.

### IV. RAG-Optimized Architecture
All content processing and retrieval systems must be designed specifically for RAG (Retrieval-Augmented Generation) use cases. This includes proper document chunking, embedding strategies, and similarity search optimization to ensure accurate and efficient AI responses.

### V. API-First Backend Design
Backend services (FastAPI) must expose well-defined RESTful APIs with proper OpenAPI documentation. All frontend functionality must communicate through these APIs, ensuring clear separation of concerns and enabling independent scaling of components.

### VI. Container-First Deployment
All backend services must be containerized with Docker. Deployment processes must be automated and reproducible. This ensures consistent environments across development, testing, and production.

### VII. Mobile-First Design
All user interfaces must be designed with mobile devices as the primary target, with desktop experiences enhanced from the mobile baseline. This ensures accessibility across all devices and optimal user experience for the diverse audience of AI and robotics learners.

### VIII. Spec-Driven Development
Strict adherence to .md specifications is mandatory. All feature development must begin with a detailed specification document that outlines requirements, user stories, and acceptance criteria. Implementation must follow the spec precisely, with any deviations requiring spec updates first.

### IX. Code Modularity and Documentation
All code must be modular and thoroughly documented. Each module should have clear interfaces and comprehensive documentation explaining its purpose, usage, and dependencies. This ensures maintainability and enables collaboration across the diverse AI and robotics research community.

## Technology Stack Requirements

The project must use the specified technology stack:

### Frontend
- **Docusaurus**: React/TypeScript-based documentation framework for creating the textbook website
- **TailwindCSS**: Utility-first CSS framework for responsive and consistent styling
- **Deployment**: GitHub Pages for static site hosting

### Backend
- **FastAPI**: Python-based web framework for building APIs and backend services
- **Docker Compose**: Container orchestration for local development and deployment

### AI/Data Layer
- **Qdrant**: Vector database for storing and retrieving embeddings for the RAG system
- **OpenAI Agents**: AI models for powering the chatbot functionality
- **LangChain/LlamaIndex**: Optional tools for advanced RAG pipeline development
- **Neon**: PostgreSQL database for structured data storage

All dependencies must be properly versioned and documented.

## Project Goal

The project aims to create a comprehensive Docusaurus-based website deployed to GitHub Pages with an embedded RAG Chatbot that serves as an interactive Physical AI & Humanoid Robotics Textbook. This platform will provide both traditional textbook content and AI-powered assistance to help users understand complex concepts in physical AI and humanoid robotics.

## Development Workflow

All code changes must follow a structured workflow: feature branch → pull request → code review → automated testing → merge to main. Frontend changes must be deployed to GitHub Pages, while backend changes must be containerized and tested in isolated environments before production deployment. The RAG chatbot functionality must be thoroughly tested for accuracy and safety before deployment.

## Governance

This constitution supersedes all other development practices. All PRs/reviews must verify compliance with these principles. Any architectural changes that conflict with these principles require explicit approval and proper amendment to this constitution.

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06