# 🚀 Quick Start Guide

## Setup in 3 Easy Steps

### Step 1: Add Your Audio Files
1. Open the `audio/` folder
2. Drop in your MP3, WAV, or other audio files
3. Name them whatever you want (e.g., `song1.mp3`, `cool-track.mp3`)

### Step 2: Update Song List
1. Open `index.html` in any text editor
2. Find the `songs` array (around line 193)
3. Update with your song details:

```javascript
const songs = [
    {
        title: "My Awesome Song",      // Song title
        artist: "Cool Artist",         // Artist name
        duration: "3:45",              // Song length
        filename: "song1.mp3",         // MUST match your file!
        icon: "🎸"                     // Any emoji
    },
    {
        title: "Another Great Track",
        artist: "Another Artist",
        duration: "4:20",
        filename: "song2.mp3",
        icon: "🎹"
    }
    // Add as many songs as you want!
];
```

### Step 3: Deploy to Vercel

**Option A - CLI (Fastest):**
```bash
npm install -g vercel
cd audio-visualizer-deploy
vercel
```

**Option B - Drag & Drop:**
1. Go to https://vercel.com/new
2. Drag the entire folder onto the page
3. Click "Deploy"

**Option C - GitHub:**
1. Push to GitHub
2. Import at vercel.com
3. Deploy

## That's It! 🎉

Your visualizer will be live at: `https://your-project.vercel.app`

## Quick Tips

✅ Audio filenames must EXACTLY match what's in `index.html`  
✅ Files should be in the `audio/` folder  
✅ MP3 format works best  
✅ Keep file sizes under 10MB for best performance  
✅ Users can also upload their own files on the site!

## Need Help?

Check the full README.md for detailed instructions and troubleshooting.

---

**Ready to see your music come alive as waves? 🌊**
