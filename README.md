# 🌊 Wave Audio Visualizer

A stunning 3D wave audio visualizer built with Three.js. Watch your music come to life as beautiful animated waves.

## Features

- 🌊 Beautiful 3D wave visualization
- 🎵 Song library homepage
- 📤 Upload your own audio files
- 🎧 Pre-loaded song library support
- 📱 Responsive design
- 🎨 Dynamic color changes based on audio

## Adding Your Audio Files

1. Place your audio files (MP3, WAV, etc.) in the `audio/` directory
2. Update the song list in `index.html` (around line 193):

```javascript
const songs = [
    {
        title: "Your Song Title",
        artist: "Artist Name",
        duration: "3:45",
        filename: "your-song.mp3",  // Must match the file in audio/ folder
        icon: "🎸"  // Any emoji
    },
    // Add more songs...
];
```

## Deploying to Vercel

### Method 1: Vercel CLI (Fastest)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to project folder
cd audio-visualizer-deploy

# Deploy
vercel
```

### Method 2: GitHub + Vercel Dashboard

1. Push this folder to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your GitHub repository
5. Click "Deploy"

### Method 3: Drag & Drop

1. Go to [vercel.com/new](https://vercel.com/new)
2. Drag and drop this entire folder
3. Vercel will deploy it automatically

## Project Structure

```
audio-visualizer-deploy/
├── index.html          # Homepage with song library
├── visualizer.html     # Wave visualizer page
├── audio/             # Place your audio files here
│   ├── song1.mp3
│   ├── song2.mp3
│   └── ...
├── vercel.json        # Vercel configuration
├── README.md          # This file
└── .gitignore         # Git ignore file
```

## How It Works

- **Homepage**: Displays a grid of song cards from your library
- **Wave Visualizer**: Shows a dynamic 3D wireframe plane that responds to audio frequencies
- **Upload Feature**: Users can also upload their own audio files to visualize

## Browser Compatibility

Works best on:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Customization

### Change Colors
Edit the gradient colors in the `<style>` sections of either HTML file.

### Adjust Wave Sensitivity
In `visualizer.html`, find this line:
```javascript
positions[i + 2] = value * 10;  // Change the multiplier (10) to adjust wave height
```

### Modify Wave Grid Resolution
In `visualizer.html`, find:
```javascript
const geometry = new THREE.PlaneGeometry(60, 60, 50, 50);  // Change the last two numbers for more/less detail
```

## Troubleshooting

### Audio won't play
- Verify filename in `index.html` exactly matches the audio file
- Check that audio file is in the `audio/` folder
- Try a different browser (Chrome recommended)

### Can't see changes after deployment
- Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)
- Wait a minute for Vercel to propagate changes

### Songs not appearing
- Check browser console (F12) for JavaScript errors
- Verify the `songs` array syntax in `index.html`
- Ensure no missing commas or quotes

## License

Free to use and modify!
