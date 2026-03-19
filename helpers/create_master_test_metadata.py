import pandas as pd
import os

# Define paths for all test metadata and audio files
test_configs = [
    {
        'metadata_path': 'sk/sk_test_metadata.csv',
        'audio_dir': 'sk/sk_test_audios',
        'audio_prefix': 'audio'  # For mapping AudioID to filename
    },
    {
        'metadata_path': 'test_file/lamin_test_metadata.csv',
        'audio_dir': 'test_file/Lamin',
        'audio_prefix': None  # AudioID directly matches filename
    },
    {
        'metadata_path': 'test_file/sein_test_metadata.csv',
        'audio_dir': 'test_file/Sein',
        'audio_prefix': None  # AudioID directly matches filename
    }
]

# Combine all metadata
all_data = []

for config in test_configs:
    # Read metadata
    df = pd.read_csv(config['metadata_path'], index_col=0)
    
    # Build file paths
    file_paths = []
    for audio_id in df['AudioID']:
        if config['audio_prefix']:
            # For sk data: AudioID 1 -> audio1.wav
            filename = f"{config['audio_prefix']}{audio_id}.wav"
        else:
            # For test_file data: AudioID 2_1 -> 2_1.wav
            filename = f"{audio_id}.wav"
        
        file_path = os.path.join(config['audio_dir'], filename)
        file_paths.append(file_path)
    
    # Add path column
    df['file_path'] = file_paths
    
    # Add source information
    if 'sk_test' in config['metadata_path']:
        df['source'] = 'sk'
    elif 'lamin' in config['metadata_path']:
        df['source'] = 'lamin'
    else:
        df['source'] = 'sein'
    
    all_data.append(df)

# Combine all datasets
master_df = pd.concat(all_data, ignore_index=True)

# Verify all files exist
print("Verifying file paths exist...")
missing_files = []
for path in master_df['file_path']:
    if not os.path.exists(path):
        missing_files.append(path)

if missing_files:
    print(f"⚠️  Warning: {len(missing_files)} files not found:")
    for f in missing_files:
        print(f"  - {f}")
else:
    print("✓ All files verified!")

# Save master metadata
output_path = 'test_metadata_master.csv'
master_df.to_csv(output_path, index=False)
print(f"\n✓ Master test metadata saved to: {output_path}")
print(f"Total test samples: {len(master_df)}")
print(f"\nDataset breakdown:")
print(master_df['source'].value_counts())
print(f"\nColumns: {list(master_df.columns)}")
print(f"\nFirst few rows:")
print(master_df.head(10))
