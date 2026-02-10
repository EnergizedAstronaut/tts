# Apple TTS Training System

A professional text-to-speech system built using real Apple training data, complete with phoneme sequences, audio samples, and metadata.

## Overview

This system includes:
- **Real Apple audio samples** (.caf format) from their TTS training dataset
- **Phonetic transcriptions** using Apple's proprietary phoneme notation
- **Metadata** including duration, category, and linguistic information
- **Interactive interfaces** for browsing, searching, and playing samples

## Dataset Information

### Statistics
- **Total Samples**: 151 audio recordings
- **Categories**: 3 (exclamations, questions, statements)
- **Average Duration**: ~2.5 seconds per sample
- **Locale**: en-US (American English)
- **Format**: CAF (Core Audio Format) with metadata in JSON

### Categories

1. **Exclamations** - Emotional utterances, commands, and expressions
   - Example: "What do bears like best? Honey!"
   - Example: "I can't believe I won the lottery!"

2. **Questions** - Various types of questions for natural conversation
   - Example: "Is Miami the capital of Florida?"
   - Example: "Were they traveling together?"

3. **Statements** - Declarative sentences covering various topics
   - Example: "His work is considered to be the foundation of the study."
   - Example: "These findings led to the creation of the radio and other devices."

## Phoneme Notation

Apple uses a proprietary phoneme notation system. Key elements:

- `#` - Word boundary
- Numbers (145, 146) - Stress markers or phoneme variants
- Letters (w, ^, t, d, u, etc.) - Phonetic sounds
- `~` - End of utterance marker
- `.` - Sentence boundary
- `,` - Pause/comma
- `!` `?` - Punctuation markers

### Example Phoneme Sequence

**Text**: "Were they traveling together?"
**Phonemes**: `w e # D J # 146 r 145 v L I N # 146 $ g E D e`

**Text**: "That roller coaster was so fun!"
**Phonemes**: `D 145 t # r O l e K O s t e # w $ z # s O # f ^ n`

## Files Included

### 1. Web Interface (`apple_tts_system.html`)

A fully self-contained HTML application with:
- Interactive sample browser
- Category filtering
- Text search
- Phoneme visualization
- Audio playback (using Web Speech API as fallback)
- Responsive design

**Features**:
- Browse all training samples
- Filter by category (exclamations, questions, statements)
- Search by text content
- View phoneme sequences for each sample
- Click to play samples
- Find closest match for custom text input

### 2. Python CLI Tool (`apple_tts.py`)

A command-line interface for advanced interactions:

```bash
python apple_tts.py
```

**Commands**:
- Type text → Find and play closest match
- `search <query>` → Search for samples containing text
- `play <id>` → Play specific sample by utterance ID
- `analyze <id>` → Show detailed phoneme analysis
- `list <category>` → List all samples in a category
- `stats` → Display dataset statistics
- `quit` → Exit program

**Usage Examples**:
```bash
> That was fun                    # Find closest match
> search traveling                # Search for "traveling"
> play rGqqo_19                   # Play specific sample
> analyze zEoVu_115               # Analyze phonemes
> list questions                   # List all questions
```

## Technical Details

### Audio Format
- **Original Format**: CAF (Core Audio Format)
- **Sample Rate**: 44.1 kHz
- **Channels**: Mono
- **Bit Depth**: 16-bit
- **Codec**: LPCM (Linear PCM)

### Metadata Schema

Each sample includes:
```json
{
  "script_title": "category name",
  "transcription": "full phonetic transcription with markers",
  "utterance_name": "unique identifier",
  "words": "actual text to be spoken",
  "phone_sequence": "phoneme sequence without markers",
  "sentence_idx": 0,
  "sentence_estimated_duration": 2.19,
  "locale": "en-US",
  "paragraph_idx": 0
}
```

### Phoneme Analysis

The system can analyze phoneme patterns:
- Word boundaries and segmentation
- Stress patterns (indicated by numbers)
- Phoneme diversity and frequency
- Timing alignment with audio

## Use Cases

### 1. TTS Research
- Study natural speech patterns
- Analyze phoneme-to-audio alignment
- Research prosody and intonation

### 2. Voice Training
- Train new TTS models
- Fine-tune existing models
- Create voice datasets

### 3. Linguistic Analysis
- Study phonetic transcription
- Analyze American English phonology
- Compare transcription systems

### 4. Application Development
- Build voice assistants
- Create audiobook generators
- Develop accessibility tools

## Converting Audio Files

To convert CAF files to more common formats:

```bash
# Convert to MP3
ffmpeg -i input.caf -ar 22050 -ac 1 -b:a 64k output.mp3

# Convert to WAV
ffmpeg -i input.caf -ar 44100 -ac 1 output.wav

# Batch convert all CAF files
for file in *.caf; do 
    ffmpeg -i "$file" "${file%.caf}.mp3"
done
```

## Understanding the Phoneme System

### Common Phoneme Mappings

| Phoneme | Example | IPA Equivalent |
|---------|---------|----------------|
| w | **w**ater | /w/ |
| ^ | b**u**t | /ʌ/ |
| t | **t**op | /t/ |
| d | **d**og | /d/ |
| E | b**e**d | /ɛ/ |
| I | b**i**t | /ɪ/ |
| $ | **a**bout | /ə/ |
| D | **th**is | /ð/ |
| T | **th**ink | /θ/ |
| S | **sh**ip | /ʃ/ |
| Z | vi**s**ion | /ʒ/ |
| N | si**ng** | /ŋ/ |

### Stress Markers
- `145` - Primary stress
- `146` - Secondary stress

## Integration Examples

### Python Integration

```python
from apple_tts import AppleTTS

# Initialize
tts = AppleTTS('metadata.json', './audio')

# Find a sample
sample = tts.find_closest_match("Hello, how are you?")

# Play audio
tts.play_audio(sample['utterance_name'])

# Analyze phonemes
analysis = tts.analyze_phonemes(sample['utterance_name'])
print(analysis['phonemes'])
```

### JavaScript Integration

```javascript
// Load samples
const samples = await fetch('metadata.json').then(r => r.json());

// Find match
function findMatch(text) {
    return samples.find(s => 
        s.words.toLowerCase().includes(text.toLowerCase())
    );
}

// Play using Web Speech API
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}
```

## Advanced Features

### Text Matching Algorithm

The system uses multiple matching strategies:
1. **Exact match** - Highest priority
2. **Substring match** - Contains the query
3. **Word overlap** - Common words between query and sample
4. **Phonetic similarity** - For misspellings and variations

### Phoneme Visualization

The web interface displays phoneme sequences with:
- Color coding for different phoneme types
- Word boundary highlighting
- Stress pattern visualization
- Interactive tooltips

## Performance Optimization

For large-scale deployments:

1. **Audio Caching**: Pre-convert all CAF files to MP3
2. **Metadata Indexing**: Build search index for fast queries
3. **CDN Hosting**: Serve audio from CDN for low latency
4. **Lazy Loading**: Load audio on-demand, not upfront

## Known Limitations

1. **Audio Format**: CAF files require conversion for web playback
2. **Limited Samples**: Only 151 samples in this dataset
3. **Single Voice**: All samples from one speaker
4. **No Synthesis**: System plays pre-recorded samples, doesn't synthesize new speech

## Future Enhancements

Potential improvements:
- Neural TTS synthesis using training data
- Multi-speaker support
- Real-time phoneme alignment
- Custom voice cloning
- Emotion and prosody control

## License & Attribution

This is Apple's proprietary training data. Usage should comply with applicable terms and conditions. The data is provided for research and educational purposes.

## Support & Resources

- **Dataset Source**: Apple TTS Training Data
- **Audio Format**: Core Audio Format (CAF)
- **Phoneme System**: Apple Proprietary Notation
- **Locale**: en-US (American English)

## Troubleshooting

### Audio Won't Play
- Ensure CAF files are in the correct directory
- Check ffmpeg is installed for audio conversion
- Verify file permissions

### Phoneme Display Issues
- Check JSON parsing of metadata
- Verify character encoding (UTF-8)

### Performance Issues
- Reduce sample quality for faster loading
- Enable audio caching
- Optimize search algorithms

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Author**: Built using Apple TTS Training Data
