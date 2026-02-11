# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A 3D audio visualizer web application built with Three.js. Features two visualization modes:
- **Wave Visualizer** (`visualizer.html`) - 3D wireframe plane responding to audio frequencies
- **MIDI Instrument Visualizer** (`visualizer-midi.html`) - Separate 3D shapes per instrument using pre-processed MIDI data

## Development

This is a static site with no build step. Open HTML files directly in a browser or deploy to Vercel.

### Local Development
```bash
# Serve locally (any static server works)
python3 -m http.server 8000
# or
npx serve .
```

### Update Song Library
```bash
# Regenerates the songs array in index.html from audio/ directory contents
node scripts/updateSongs.js
```

### Generate MIDI Visualization Data
```bash
# Install Python dependencies first
pip install -r scripts/requirements.txt

# Generate visualization JSON for a song
python scripts/midi_visualization_mapper.py --audio audio/song.wav --midi midi_files/song.mid
# Output goes to viz_data/{song}_viz.json
```

## Architecture

**Page Flow:**
- `index.html` - Song library homepage with upload support
- Clicking a song navigates to `visualizer.html` (or `visualizer-midi.html` if Shift+click)
- Audio filename passed via URL query params (`?song=...&title=...`)

**MIDI Visualization Pipeline:**
1. `scripts/midi_visualization_mapper.py` parses MIDI files and audio to create JSON timeline data
2. Output JSON stored in `viz_data/{songname}_viz.json`
3. `visualizer-midi.html` loads JSON and syncs 3D shape animations to audio playback

**Key Implementation Details:**
- Audio analysis uses Web Audio API (AudioContext, AnalyserNode)
- 3D rendering uses Three.js r128 via CDN
- Uploaded files stored temporarily in sessionStorage as base64
- CORS headers for audio files configured in `vercel.json`

## Deployment

Deployed to Vercel. Push to main or run `vercel` CLI.
