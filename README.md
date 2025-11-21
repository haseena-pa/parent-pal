# Parent Pal

Parent Pal is an AI-powered application designed to assist parents with two core needs: accessing parenting knowledge (including milestones and nearby facilities) and tracking their baby's sleep patterns.

## Features

The application consists of two specialized agents:

### 1. Parenting & Location Agent (`baby_parenting_info_agent`)

A comprehensive workflow that answers general parenting questions and finds relevant real-world locations.

- **Parenting Advice:** Provides information on baby milestones, general care, and parenting tips using Google Search.
- **Location Finder:** Helps users find nearby essential services like hospitals, pediatricians, and sleep consultants using the Google Maps MCP server.
- **Workflow:** Uses a **Parallel Agent** to fetch knowledge and location data simultaneously, followed by a **Summary Agent** that synthesizes the information into a helpful response.

### 2. Baby Sleep Tracker Agent (`sleep_track_agent`)

A dedicated assistant for managing a baby's sleep schedule with persistent storage.

- **Log Sleep:** Records start and end times for naps and night sleep.
- **Manage Records:** Allows parents to update or delete incorrect sleep entries.
- **History:** Retrieves past sleep records to help track patterns.
- **Personalization:** Identifies parents by name and email to maintain user-specific records.
