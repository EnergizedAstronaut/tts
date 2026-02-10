#!/usr/bin/env python3
"""
Apple TTS Training System
A text-to-speech system using Apple's real training data with phoneme sequences
"""

import json
import subprocess
import os
from pathlib import Path
import difflib

class AppleTTS:
    def __init__(self, metadata_path, audio_dir):
        """Initialize the TTS system with metadata and audio files"""
        self.metadata_path = metadata_path
        self.audio_dir = Path(audio_dir)
        self.samples = []
        self.load_metadata()
        
    def load_metadata(self):
        """Load the training metadata"""
        print("Loading Apple TTS training data...")
        with open(self.metadata_path, 'r') as f:
            for line in f:
                if line.strip():
                    self.samples.append(json.loads(line))
        print(f"Loaded {len(self.samples)} training samples")
        
    def get_stats(self):
        """Get statistics about the training data"""
        categories = set(s['script_title'] for s in self.samples)
        avg_duration = sum(s['sentence_estimated_duration'] for s in self.samples) / len(self.samples)
        
        return {
            'total_samples': len(self.samples),
            'categories': len(categories),
            'category_names': sorted(categories),
            'avg_duration': round(avg_duration, 2),
            'total_duration': round(sum(s['sentence_estimated_duration'] for s in self.samples), 2)
        }
    
    def find_sample_by_id(self, utterance_name):
        """Find a sample by its utterance name"""
        for sample in self.samples:
            if sample['utterance_name'] == utterance_name:
                return sample
        return None
    
    def find_closest_match(self, text):
        """Find the closest matching sample for given text"""
        text = text.lower().strip()
        best_match = None
        best_score = 0
        
        for sample in self.samples:
            sample_text = sample['words'].lower()
            
            # Exact match
            if sample_text == text:
                return sample
            
            # Use difflib for similarity matching
            score = difflib.SequenceMatcher(None, text, sample_text).ratio()
            
            # Bonus for word matches
            text_words = set(text.split())
            sample_words = set(sample_text.split())
            word_overlap = len(text_words & sample_words) / len(text_words) if text_words else 0
            score += word_overlap * 0.3
            
            if score > best_score:
                best_score = score
                best_match = sample
        
        return best_match if best_score > 0.3 else None
    
    def search_samples(self, query):
        """Search for samples containing the query text"""
        query = query.lower()
        results = []
        
        for sample in self.samples:
            if query in sample['words'].lower():
                results.append(sample)
        
        return results
    
    def filter_by_category(self, category):
        """Filter samples by category"""
        return [s for s in self.samples if s['script_title'] == category]
    
    def play_audio(self, utterance_name):
        """Play audio for a specific utterance"""
        sample = self.find_sample_by_id(utterance_name)
        if not sample:
            print(f"Sample {utterance_name} not found")
            return False
        
        # Look for the audio file
        audio_file = self.audio_dir / f"{utterance_name}.caf"
        
        if not audio_file.exists():
            print(f"Audio file not found: {audio_file}")
            print(f"Using text-to-speech synthesis for: {sample['words']}")
            # Fallback to system TTS
            self.synthesize_text(sample['words'])
            return True
        
        # Convert and play CAF file
        print(f"Playing: {sample['words']}")
        print(f"Phonemes: {sample['phone_sequence']}")
        print(f"Duration: {sample['sentence_estimated_duration']}s")
        
        try:
            # Convert CAF to WAV and play
            temp_wav = '/tmp/temp_audio.wav'
            subprocess.run([
                'ffmpeg', '-i', str(audio_file), 
                '-y', temp_wav
            ], capture_output=True, check=True)
            
            # Play the audio
            subprocess.run(['ffplay', '-nodisp', '-autoexit', temp_wav], 
                         capture_output=True)
            
            # Cleanup
            os.remove(temp_wav)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio: {e}")
            return False
    
    def synthesize_text(self, text):
        """Synthesize text using system TTS as fallback"""
        try:
            # Use espeak if available
            subprocess.run(['espeak', text], check=True)
        except FileNotFoundError:
            # Try macOS say command
            try:
                subprocess.run(['say', text], check=True)
            except FileNotFoundError:
                print(f"TTS not available. Text: {text}")
    
    def analyze_phonemes(self, utterance_name):
        """Analyze and display phoneme information"""
        sample = self.find_sample_by_id(utterance_name)
        if not sample:
            return None
        
        phonemes = sample['phone_sequence'].split(' # ')
        
        return {
            'text': sample['words'],
            'phoneme_count': len(phonemes),
            'phonemes': phonemes,
            'full_sequence': sample['phone_sequence'],
            'transcription': sample['transcription']
        }
    
    def generate_report(self):
        """Generate a comprehensive report of the training data"""
        stats = self.get_stats()
        
        report = []
        report.append("=" * 60)
        report.append("APPLE TTS TRAINING DATA REPORT")
        report.append("=" * 60)
        report.append(f"\nTotal Samples: {stats['total_samples']}")
        report.append(f"Categories: {stats['categories']}")
        report.append(f"Average Duration: {stats['avg_duration']}s")
        report.append(f"Total Duration: {stats['total_duration']}s")
        report.append(f"\nCategories: {', '.join(stats['category_names'])}")
        
        report.append("\n" + "-" * 60)
        report.append("CATEGORY BREAKDOWN")
        report.append("-" * 60)
        
        for category in stats['category_names']:
            cat_samples = self.filter_by_category(category)
            cat_duration = sum(s['sentence_estimated_duration'] for s in cat_samples)
            report.append(f"\n{category.upper()}:")
            report.append(f"  Samples: {len(cat_samples)}")
            report.append(f"  Total Duration: {cat_duration:.2f}s")
            report.append(f"  Avg Duration: {cat_duration/len(cat_samples):.2f}s")
        
        report.append("\n" + "-" * 60)
        report.append("SAMPLE EXAMPLES (First 5)")
        report.append("-" * 60)
        
        for i, sample in enumerate(self.samples[:5], 1):
            report.append(f"\n{i}. {sample['utterance_name']} ({sample['script_title']})")
            report.append(f"   Text: {sample['words']}")
            report.append(f"   Duration: {sample['sentence_estimated_duration']}s")
            report.append(f"   Phonemes: {sample['phone_sequence'][:80]}...")
        
        return "\n".join(report)


def main():
    """Main interactive TTS demo"""
    print("\n" + "="*60)
    print("APPLE TTS TRAINING SYSTEM")
    print("="*60 + "\n")
    
    # Initialize TTS
    metadata_path = '/mnt/user-data/uploads/metadata_data.json'
    audio_dir = '/mnt/user-data/uploads'
    
    tts = AppleTTS(metadata_path, audio_dir)
    
    # Display stats
    print(tts.generate_report())
    
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("\nCommands:")
    print("  1. Type text to find and play closest match")
    print("  2. 'search <query>' - Search for samples")
    print("  3. 'play <id>' - Play specific sample by ID")
    print("  4. 'analyze <id>' - Analyze phonemes for sample")
    print("  5. 'list <category>' - List samples in category")
    print("  6. 'stats' - Show statistics")
    print("  7. 'quit' - Exit")
    
    while True:
        print("\n" + "-"*60)
        user_input = input("\n> ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if user_input.lower() == 'stats':
            stats = tts.get_stats()
            print(f"\nTotal Samples: {stats['total_samples']}")
            print(f"Categories: {', '.join(stats['category_names'])}")
            print(f"Average Duration: {stats['avg_duration']}s")
            continue
        
        if user_input.lower().startswith('search '):
            query = user_input[7:]
            results = tts.search_samples(query)
            print(f"\nFound {len(results)} matches:")
            for r in results[:10]:
                print(f"  {r['utterance_name']}: {r['words']}")
            continue
        
        if user_input.lower().startswith('play '):
            utterance_id = user_input[5:].strip()
            tts.play_audio(utterance_id)
            continue
        
        if user_input.lower().startswith('analyze '):
            utterance_id = user_input[8:].strip()
            analysis = tts.analyze_phonemes(utterance_id)
            if analysis:
                print(f"\nText: {analysis['text']}")
                print(f"Phoneme Count: {analysis['phoneme_count']}")
                print(f"Phonemes: {' '.join(analysis['phonemes'][:10])}...")
                print(f"Full Sequence: {analysis['full_sequence']}")
            continue
        
        if user_input.lower().startswith('list '):
            category = user_input[5:].strip()
            samples = tts.filter_by_category(category)
            print(f"\n{len(samples)} samples in '{category}':")
            for s in samples[:15]:
                print(f"  {s['utterance_name']}: {s['words']}")
            continue
        
        # Default: find closest match and play
        match = tts.find_closest_match(user_input)
        if match:
            print(f"\nClosest match: {match['utterance_name']}")
            print(f"Text: {match['words']}")
            print(f"Category: {match['script_title']}")
            print(f"Duration: {match['sentence_estimated_duration']}s")
            
            play = input("\nPlay this sample? (y/n): ").strip().lower()
            if play == 'y':
                tts.play_audio(match['utterance_name'])
        else:
            print("\nNo close match found. Try a different phrase.")


if __name__ == '__main__':
    main()
