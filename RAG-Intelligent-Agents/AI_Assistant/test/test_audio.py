#!/usr/bin/env python3
"""
Audio Test Script
Test the audio transcription functionality with your QA-01.mp3 file
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import transcribe_mp3, whisper_model
import whisper

def test_audio_file(file_path):
    """Test audio transcription with detailed debugging"""
    
    print(f"🎵 Testing audio file: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Check file size
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    print(f"📊 File size: {file_size:.2f} MB")
    
    # Check file permissions
    if not os.access(file_path, os.R_OK):
        print(f"❌ Cannot read file: {file_path}")
        return
    
    print("✅ File checks passed")
    
    try:
        # Test direct Whisper transcription
        print("\n🔊 Loading Whisper model...")
        model = whisper.load_model("base")
        print("✅ Whisper model loaded")
        
        print("\n🎧 Starting transcription...")
        result = model.transcribe(file_path, verbose=True)
        
        print(f"\n✅ Transcription completed!")
        print(f"📝 Text length: {len(result['text'])} characters")
        print(f"🎵 Language detected: {result.get('language', 'Unknown')}")
        
        print("\n📄 Transcribed text:")
        print("-" * 50)
        print(result["text"])
        print("-" * 50)
        
        # Test through our agent function
        print("\n🤖 Testing through agent function...")
        agent_result = transcribe_mp3(file_path)
        print("Agent result:", agent_result[:200] + "..." if len(agent_result) > 200 else agent_result)
        
    except Exception as e:
        print(f"❌ Error during transcription: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with your specific file
    test_file = "/Users/abdulrehman/Downloads/QA-01.mp3"
    test_audio_file(test_file)
