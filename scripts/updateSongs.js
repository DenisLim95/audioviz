#!/usr/bin/env node

/**
 * Utility script to regenerate the `songs` array in `index.html`
 * using the contents of the local `/audio` directory. Run with:
 *    node scripts/updateSongs.js
 */

const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const audioDir = path.join(projectRoot, 'audio');
const indexHtmlPath = path.join(projectRoot, 'index.html');
const INDENT = '        '; // matches indentation of the <script> tag block

const iconMap = [
    { keywords: ['plane', 'flight'], icon: '✈️' },
    { keywords: ['soul'], icon: '💫' },
    { keywords: ['ss'], icon: '⭐' },
    { keywords: ['coltran', 'sax'], icon: '🎷' },
    { keywords: ['rach', 'piano', 'suite'], icon: '🎹' },
    { keywords: ['look'], icon: '🙌' },
    { keywords: ['peace'], icon: '🕊️' },
    { keywords: ['sunday', 'ny'], icon: '🌆' },
    { keywords: ['deoul'], icon: '🌌' },
    { keywords: ['frenn'], icon: '🎧' },
    { keywords: ['hyori'], icon: '🌠' },
    { keywords: ['fall'], icon: '🍂' }
];

function getAudioFiles(dir) {
    if (!fs.existsSync(dir)) {
        throw new Error(`Audio directory not found at ${dir}`);
    }

    return fs
        .readdirSync(dir)
        .filter((name) => {
            const fullPath = path.join(dir, name);
            const isFile = fs.statSync(fullPath).isFile();
            const isAudio = /\.(wav|mp3|m4a|aac|ogg)$/i.test(name);
            return isFile && isAudio;
        })
        .sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
}

function formatTitle(fileName) {
    const base = fileName.replace(/\.[^/.]+$/, '');
    return base
        .replace(/[-_]+/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .split(' ')
        .map((word) => (word ? word[0].toUpperCase() + word.slice(1) : ''))
        .join(' ');
}

function pickIcon(title) {
    const lower = title.toLowerCase();
    const matched = iconMap.find((entry) => entry.keywords.some((kw) => lower.includes(kw)));
    return matched ? matched.icon : '🎵';
}

function escapeForJs(value) {
    return value.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

function buildSongObject(fileName) {
    const title = formatTitle(fileName);
    return {
        title,
        artist: 'Local Library',
        duration: '—',
        filename: fileName,
        icon: pickIcon(title)
    };
}

function serializeSong(song) {
    return (
        `${INDENT}    {\n` +
        `${INDENT}        title: "${escapeForJs(song.title)}",\n` +
        `${INDENT}        artist: "${escapeForJs(song.artist)}",\n` +
        `${INDENT}        duration: "${song.duration}",\n` +
        `${INDENT}        filename: "${escapeForJs(song.filename)}",\n` +
        `${INDENT}        icon: "${song.icon}"\n` +
        `${INDENT}    }`
    );
}

function updateIndexHtml(songObjects) {
    if (!fs.existsSync(indexHtmlPath)) {
        throw new Error(`index.html not found at ${indexHtmlPath}`);
    }

    const html = fs.readFileSync(indexHtmlPath, 'utf8');
    const songsRegex = /const songs = \[[\s\S]*?\];/;

    if (!songsRegex.test(html)) {
        throw new Error('Could not find `const songs = [...]` block inside index.html');
    }

    const serializedSongs = songObjects.map(serializeSong).join(',\n');
    const replacement = `const songs = [\n${serializedSongs}\n${INDENT}];`;
    const updatedHtml = html.replace(songsRegex, replacement);

    fs.writeFileSync(indexHtmlPath, updatedHtml);
}

function main() {
    try {
        const audioFiles = getAudioFiles(audioDir);
        if (audioFiles.length === 0) {
            console.warn('No audio files found. Aborting without changes.');
            return;
        }

        const songObjects = audioFiles.map(buildSongObject);
        updateIndexHtml(songObjects);
        console.log(`Updated songs list with ${songObjects.length} entries from ${audioDir}`);
    } catch (err) {
        console.error(err.message);
        process.exitCode = 1;
    }
}

main();

