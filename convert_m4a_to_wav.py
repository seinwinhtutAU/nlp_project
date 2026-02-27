import os
from pydub import AudioSegment
test_file_dir = os.path.join(os.path.dirname(__file__), 'test_file')

def convert_m4a_to_wav(m4a_file_path, output_dir):

    try:
        audio = AudioSegment.from_file(m4a_file_path, format="m4a")

        base_name = os.path.splitext(os.path.basename(m4a_file_path))[0]

        wav_file_path = os.path.join(output_dir, f"{base_name}.wav")

        audio.export(wav_file_path, format="wav")
        
        print(f"✓ Converted: {base_name}.m4a -> {base_name}.wav")
        return True
    
    except Exception as e:
        print(f"✗ Error converting {os.path.basename(m4a_file_path)}: {str(e)}")
        return False

def main():
    """Main function to convert all M4A files to WAV"""
    
    if not os.path.exists(test_file_dir):
        print(f"Error: test_file directory not found at {test_file_dir}")
        return

    m4a_files = [f for f in os.listdir(test_file_dir) if f.lower().endswith('.m4a')]
    
    if not m4a_files:
        print("No M4A files found in test_file directory")
        return
    
    print(f"Found {len(m4a_files)} M4A files to convert\n")
    
    successful = 0
    for m4a_file in m4a_files:
        m4a_path = os.path.join(test_file_dir, m4a_file)
        if convert_m4a_to_wav(m4a_path, test_file_dir):
            successful += 1
    
    print(f"\nConversion complete: {successful}/{len(m4a_files)} files successfully converted")

if __name__ == "__main__":
    main()
