# Parent Pal

An AI-powered parenting assistant that helps parents track their baby's sleep patterns and access parenting information with location-based services.

## Table of Contents

- [Problem](#problem)
- [Solution](#solution)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Screenshots](#screenshots)
---

## Problem

New parents face two critical challenges:

### 1. Information Overload & Access

- Parents struggle to find reliable, quick answers to parenting questions (e.g., "Why is my baby crying?", "What are the developmental milestones for a 6-month-old?")
- Difficulty locating nearby parenting resources like pediatricians, hospitals, parks, or sleep consultants
- Need for real-time, contextual information that combines knowledge with actionable location data

### 2. Sleep Pattern Tracking

- Babies' sleep patterns are critical indicators of health and development
- Manual tracking of sleep logs is tedious and error-prone
- Parents need persistent, personalized records to identify patterns and share with healthcare providers
- Existing tools lack intelligent assistance for data entry and pattern analysis

---

## Solution

Parent Pal is an intelligent multi-agent system built using Google's Agent Development Kit (ADK) that provides:

### Core Capabilities

#### 1. **Intelligent Sleep Tracking**

- Natural language interface for logging sleep data ("Baby slept from 2pm to 4pm")
- Persistent storage using MCP Toolbox with PostgreSQL backend
- User-specific records identified by name and email (stored in user_info table)
- Full CRUD operations: log, retrieve, update, and delete sleep records (sleep_track table)
- Context-aware time parsing (understands "today", "yesterday", "now")

#### 2. **Parenting Knowledge & Location Services**

- Real-time answers to parenting questions using Google Search
- Nearby location discovery using Google Maps API
- Parallel processing for simultaneous knowledge and location retrieval
- Synthesized responses that combine information with actionable location data

#### 3. **Conversational Interface**

- Natural, context-aware interactions
- User identity management (only asks for details when needed for sleep tracking)
- Intelligent routing between different capabilities

---

## Architecture

Parent Pal uses a **hierarchical multi-agent architecture** with specialized agents coordinated by a root agent.

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Root Agent                              │
│              (Parent Pal Coordinator)                       │
│                                                             │
│  • Routes user requests to appropriate sub-agents          │
│  • Manages user context (name/email)                       │
│  • Provides conversational interface                        │
└─────────────────┬───────────────────────────┬───────────────┘
                  │                           │
        ┌─────────▼─────────┐       ┌────────▼──────────┐
        │  Sleep Tracker    │       │   Parallel Agent  │
        │      Tool         │       │   (Knowledge +    │
        │                   │       │    Location)      │
        └─────────┬─────────┘       └────────┬──────────┘
                  │                           │
                  │                  ┌────────┴─────────┐
                  │                  │                  │
                  │         ┌────────▼────────┐ ┌──────▼────────┐
                  │         │ Parenting Agent │ │ Maps Agent    │
                  │         │                 │ │               │
                  │         │ • Google Search │ │ • Google Maps │
                  │         └─────────────────┘ └───────────────┘
                  │
         ┌────────▼──────────┐
         │  Tools:           │
         │  • Datetime       │
         │  • Toolbox DB     │
         │    (CRUD ops)     │
         └───────────────────┘
```

### Component Details

#### 1. Root Agent (`parent_pal/agent.py:39`)

- **Role:** Main coordinator and user interface
- **Model:** Gemini 2.5 Flash
- **Responsibilities:**
  - Route requests based on user intent
  - Maintain user context across conversations
  - Intelligently ask for identity only when needed (for sleep tracking)
  - Provide warm, conversational responses

#### 2. Sleep Tracker Agent (`parent_pal/sub_agents/sleep_track_agent/agent.py:13`)

- **Role:** Manage all sleep-related operations
- **Tools:**
  - `get_current_datetime()`: Resolves relative time references
  - MCP Toolbox database tools: CRUD operations for sleep records
- **Features:**
  - User-specific data isolation (user_info table)
  - Natural language time parsing
  - Persistent storage via MCP Toolbox with PostgreSQL backend (sleep_track table)

#### 3. Parallel Agent (`parent_pal/agent.py:25`)

- **Role:** Execute parenting and location searches simultaneously
- **Sub-agents:**
  - **Parenting Agent** (`parent_pal/sub_agents/parenting_agent/agent.py:7`)
    - Uses Google Search for parenting information
    - Provides evidence-based advice on milestones, care tips, and common issues
  - **Maps Location Agent** (`parent_pal/sub_agents/maps_location_agent/agent.py:9`)
    - Uses Google Maps MCP server
    - Finds nearby pediatricians, hospitals, parks, etc.
- **Benefits:** Reduces response latency by running searches in parallel

### Technology Stack

- **Framework:** Google Agent Development Kit (ADK)
- **LLM:** Gemini 2.5 Flash
- **Database:** MCP Toolbox with PostgreSQL backend (local)
  - `user_info` table: User identity and profile information
  - `sleep_track` table: Baby sleep tracking records
- **External APIs:**
  - Google Search API
  - Google Maps API (via MCP)
- **Tools:**
  - MCP (Model Context Protocol) for external integrations
  - MCP Toolbox for database operations
  - StdioServerParameters for MCP server connections

### Data Flow

1. **User Input** → Root Agent analyzes intent
2. **Routing Decision:**
   - Sleep tracking request → Sleep Tracker Agent → MCP Toolbox → PostgreSQL (user_info & sleep_track tables)
   - Parenting/location query → Parallel Agent → [Parenting Agent + Maps Agent]
3. **Tool Execution:** Agents call respective tools (MCP Toolbox/DB, Search, Maps)
4. **Response Synthesis:** Results aggregated and formatted
5. **User Output** → Natural language response with actionable information

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install google-adk
pip install toolbox_core
```

### 2. Set Up Toolbox

Set up toolbox using the [GenAI Toolbox repository](https://github.com/googleapis/genai-toolbox)

### 3. Set Up Database

Download and install [postgres-client cli (psql).](https://www.tigerdata.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows)

Connect to PostgreSQL and create the database:

```bash
psql -h 127.0.0.1 -p 5432 -U local
```

Create the database:

```sql
CREATE DATABASE parent_pal;
```

Then exit psql and run the SQL script to create tables:

```bash
cd parent_pal/dataset
psql -h 127.0.0.1 -p 5432 -U local -d parent_pal -f create_table.sql
```

### 4. Start Toolbox Server

In one terminal, from the root folder run:

```bash
./toolbox --tools-file "tools.yaml"
```

### 5. Configure Environment Variables

Rename `.env.example` to `.env` and provide the required API keys.

### 6. Run the Application

In a new terminal, from the root folder run:

```bash
adk web
```

---





## Screenshots

Asking user info while choosing sleep tracker
<img width="936" height="597" alt="image" src="https://github.com/user-attachments/assets/bfa28aa3-ffe6-4b8e-b570-4382d37c6250" />

Create , Update, List Sleep Logs
<img width="936" height="597" alt="image" src="https://github.com/user-attachments/assets/379a9012-c5c3-437a-b5b3-f146c52ea705" />


Delete Sleep Log
<img width="946" height="540" alt="image" src="https://github.com/user-attachments/assets/f530a51a-683f-419c-9e21-dfbfd3da5a4a" />

Parenting Related queries
<img width="946" height="583" alt="image" src="https://github.com/user-attachments/assets/4ca88e5c-0b2d-4422-a1b6-b8c5f2d7125c" />


Location Related Queries

<img width="946" height="490" alt="image" src="https://github.com/user-attachments/assets/38ee6cbb-1110-4338-8039-dc2ba77c6fc4" />






