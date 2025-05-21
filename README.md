# Hotel Reservation Admin Dashboard

This is a Streamlit-based admin dashboard for hotel reservation management.

## Project Structure

- `src/` - Main source code
  - `pages/` - Streamlit pages (Reservation List, Reservation Detail)
  - `components/` - Reusable UI components
  - `api/` - API integration logic
  - `utils/` - Utility functions

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run src/app.py
   ```

## Features
- Reservation list with filtering, sorting, pagination, and CRUD actions
- Reservation detail page with dummy data, editable form, and delete functionality
- Responsive, clean UI
- Modular, maintainable code
