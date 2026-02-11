#!/usr/bin/env python3
"""
MIDI Visualization Mapper
Maps individual instrument MIDI tracks to synchronized audio visualization data.

This script analyzes MIDI files for each instrument and creates timing/intensity
data that can be used to create instrument-specific visualizations in the web app.

Usage:
    python midi_visualization_mapper.py --audio song.wav --midi piano.mid drums.mid bass.mid

Output:
    JSON file with timestamp-based visualization data for each instrument
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import mido
    from mido import MidiFile
except ImportError:
    print("Error: 'mido' library not installed. Install with: pip install mido")
    sys.exit(1)

try:
    import librosa
    import numpy as np
except ImportError:
    print("Error: 'librosa' library not installed. Install with: pip install librosa")
    sys.exit(1)


def parse_midi_track(midi_file_path, instrument_name, track_index=None):
    """
    Parse a MIDI file and extract note events with timing.
    If track_index is None, parse all tracks together.
    
    Returns:
        List of events: [{time: seconds, note: int, velocity: int, duration: seconds}]
    """
    mid = MidiFile(midi_file_path)
    
    events = []
    tempo = 500000  # Default tempo (120 BPM)
    ticks_per_beat = mid.ticks_per_beat
    
    # Track active notes to calculate duration
    active_notes = {}
    
    # Process specific track or all tracks
    tracks_to_process = [mid.tracks[track_index]] if track_index is not None else mid.tracks
    
    for track in tracks_to_process:
        current_time = 0
        
        for msg in track:
            # Update time
            current_time += mido.tick2second(msg.time, ticks_per_beat, tempo)
            
            # Update tempo if tempo change event
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            
            # Note on event
            elif msg.type == 'note_on' and msg.velocity > 0:
                note_key = (msg.note, msg.channel)
                active_notes[note_key] = {
                    'start_time': current_time,
                    'velocity': msg.velocity,
                    'note': msg.note,
                    'channel': msg.channel
                }
            
            # Note off event (or note_on with velocity 0)
            elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                note_key = (msg.note, msg.channel)
                if note_key in active_notes:
                    note_info = active_notes[note_key]
                    duration = current_time - note_info['start_time']
                    
                    events.append({
                        'time': note_info['start_time'],
                        'note': note_info['note'],
                        'velocity': note_info['velocity'],
                        'duration': duration,
                        'instrument': instrument_name,
                        'channel': note_info['channel']
                    })
                    
                    del active_notes[note_key]
    
    return sorted(events, key=lambda x: x['time'])


def parse_single_midi_file(midi_file_path):
    """
    Parse a single MIDI file and separate tracks by name or channel.
    
    Returns:
        Dictionary: {instrument_name: [events]}
    """
    mid = MidiFile(midi_file_path)
    instrument_tracks = {}
    
    print(f"Found {len(mid.tracks)} tracks in MIDI file")
    
    for track_idx, track in enumerate(mid.tracks):
        # Try to get track name
        track_name = None
        for msg in track:
            if msg.type == 'track_name':
                track_name = msg.name
                break
        
        # Skip empty tracks or tracks with no notes
        has_notes = any(msg.type in ['note_on', 'note_off'] for msg in track)
        if not has_notes:
            print(f"  Track {track_idx}: '{track_name or 'Unnamed'}' - Skipping (no notes)")
            continue
        
        # Use track name or generate one
        if not track_name or track_name.strip() == '':
            track_name = f"Track_{track_idx}"
        
        print(f"  Track {track_idx}: '{track_name}' - Processing")
        
        # Parse this specific track
        events = parse_midi_track(midi_file_path, track_name, track_index=track_idx)
        
        if events:
            instrument_tracks[track_name] = events
            print(f"    Found {len(events)} note events")
    
    return instrument_tracks


def analyze_audio_sync(audio_path):
    """
    Analyze audio file to get timing and tempo information.
    
    Returns:
        Dictionary with audio metadata
    """
    y, sr = librosa.load(audio_path)
    
    # Get tempo
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    
    # Get duration
    duration = librosa.get_duration(y=y, sr=sr)
    
    return {
        'duration': float(duration),
        'tempo': float(tempo),
        'sample_rate': sr,
        'beat_times': beat_times.tolist()
    }


def create_visualization_timeline(events, audio_info, time_resolution=0.1):
    """
    Create a timeline of visualization data points.
    
    Args:
        events: List of MIDI events
        audio_info: Audio metadata
        time_resolution: Seconds between data points (default 0.1 = 10fps)
    
    Returns:
        List of timeline points with aggregated note data
    """
    duration = audio_info['duration']
    timeline = []
    
    # Create time slots
    num_slots = int(duration / time_resolution) + 1
    
    for i in range(num_slots):
        slot_time = i * time_resolution
        slot_end = slot_time + time_resolution
        
        # Find all events active in this time slot
        active_events = [
            e for e in events 
            if e['time'] <= slot_end and (e['time'] + e['duration']) >= slot_time
        ]
        
        if active_events:
            # Calculate aggregate intensity
            total_velocity = sum(e['velocity'] for e in active_events)
            avg_velocity = total_velocity / len(active_events)
            
            # Calculate pitch range
            notes = [e['note'] for e in active_events]
            avg_pitch = sum(notes) / len(notes)
            pitch_range = max(notes) - min(notes) if len(notes) > 1 else 0
            
            timeline.append({
                'time': slot_time,
                'active_notes': len(active_events),
                'intensity': avg_velocity / 127.0,  # Normalize to 0-1
                'avg_pitch': avg_pitch,
                'pitch_range': pitch_range,
                'notes': notes
            })
        else:
            timeline.append({
                'time': slot_time,
                'active_notes': 0,
                'intensity': 0,
                'avg_pitch': 0,
                'pitch_range': 0,
                'notes': []
            })
    
    return timeline


def generate_visualization_config(instrument_tracks, audio_info):
    """
    Generate a complete visualization configuration for all instruments.
    
    Returns:
        Dictionary with per-instrument visualization data and sync info
    """
    config = {
        'audio': audio_info,
        'instruments': {}
    }
    
    for instrument_name, events in instrument_tracks.items():
        timeline = create_visualization_timeline(events, audio_info)
        
        config['instruments'][instrument_name] = {
            'total_events': len(events),
            'timeline': timeline,
            'note_range': {
                'min': min(e['note'] for e in events) if events else 0,
                'max': max(e['note'] for e in events) if events else 0
            },
            'avg_velocity': sum(e['velocity'] for e in events) / len(events) if events else 0
        }
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description='Map MIDI instruments to audio visualization data'
    )
    parser.add_argument('--audio', required=True, help='Path to audio file (WAV/MP3)')
    parser.add_argument('--midi', required=True, 
                       help='MIDI file (single file with multiple tracks, or multiple files)')
    parser.add_argument('--output', help='Output JSON file (default: audio_name_viz.json)')
    parser.add_argument('--resolution', type=float, default=0.1,
                       help='Time resolution in seconds (default: 0.1)')
    parser.add_argument('--single-file', action='store_true',
                       help='Parse single MIDI file with multiple tracks (default: auto-detect)')
    
    args = parser.parse_args()
    
    # Validate audio file
    if not os.path.exists(args.audio):
        print(f"Error: Audio file not found: {args.audio}")
        sys.exit(1)
    
    print(f"Analyzing audio: {args.audio}")
    audio_info = analyze_audio_sync(args.audio)
    print(f"  Duration: {audio_info['duration']:.2f}s")
    print(f"  Tempo: {audio_info['tempo']:.1f} BPM")
    
    # Check if single MIDI file or multiple
    midi_path = args.midi
    
    if not os.path.exists(midi_path):
        print(f"Error: MIDI file not found: {midi_path}")
        sys.exit(1)
    
    print(f"\nParsing MIDI file: {midi_path}")
    
    # Parse single MIDI file with multiple tracks
    instrument_tracks = parse_single_midi_file(midi_path)
    
    if not instrument_tracks:
        print("Error: No valid tracks found in MIDI file")
        sys.exit(1)
    
    # Generate visualization config
    print("\nGenerating visualization configuration...")
    config = generate_visualization_config(instrument_tracks, audio_info)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        audio_name = Path(args.audio).stem
        output_path = f"viz_data/{audio_name}_viz.json"
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    # Save configuration
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✓ Visualization data saved to: {output_path}")
    print(f"\nSummary:")
    for instrument, data in config['instruments'].items():
        print(f"  {instrument}: {data['total_events']} events, "
              f"notes {data['note_range']['min']}-{data['note_range']['max']}")


if __name__ == '__main__':
    main()

