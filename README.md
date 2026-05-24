# Incident Report System

A web-based incident reporting system with interactive map and email notifications via Web3Forms.

## Setup

### 1. Install Dependencies

No additional Python packages required (uses standard library).

### 2. Run the Server

```bash
python3 serve.py
```

Server runs at: http://localhost:8081

### 3. Open the Application

Open http://localhost:8081/index.html in your browser.

## How It Works

- **Map**: Displays incident markers from Google My Maps with counts
- **Form**: Click on map to select location, fill in incident details
- **Email**: Reports are sent via Web3Forms API (browser-based, no backend setup needed)
- **Fallback**: If Web3Forms fails, modal provides a mailto: link to send manually

## Files

- `index.html` - Main application (map, form, incident table)
- `serve.py` - Simple HTTP server (serves files + provides markers API)
- `favicon.svg` - Site icon
- `.gitignore` - Prevents committing sensitive files

## Features

✅ Interactive OpenStreetMap with clickable location selection  
✅ Automatic address lookup via reverse geocoding  
✅ Current location detection  
✅ Icon-based incident type selection (multiple types allowed)  
✅ Sortable incident table with all reported locations  
✅ Email delivery via Web3Forms API (zero configuration)  
✅ Error handling with manual email fallback  

## Troubleshooting

**Markers not loading?**
- Make sure you access via http://localhost:8081/index.html (not file://)
- Check that serve.py is running

**Email not sending?**
- Check your internet connection
- Check browser console for errors
- Use the "E-Mail manuell senden" button in the error modal as fallback
