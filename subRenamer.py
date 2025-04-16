from pathlib import Path
import re

# Define video file extensions
VIDEO_EXTENSIONS = {
    '.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv',
    '.webm', '.mpeg', '.mpg', '.m4v', '.3gp', '.3g2',
    '.ts', '.vob', '.rm', '.rmvb', '.asf', '.f4v',
    '.m2ts', '.divx'
}

# Folder where the script is located
folder = Path(__file__).parent

# Regex for S03E03 format (case-insensitive)
srt_regex = re.compile(r'[sS]\d{2}[eE]\d{2}', re.IGNORECASE)
video_regex = re.compile(r'[sS]\d{2}[eE]\d{2}', re.IGNORECASE)

# Loop through .srt files
for srt_file in folder.glob("*.srt"):
    print(f"\nChecking SRT file: {srt_file.name}")
    match = srt_regex.search(srt_file.name)

    if match:
        ep_code = match.group(0).lower()  # Match the full episode code (S03E03 or s03e03)
        print(f"  Episode code extracted: {ep_code}")

        matched = False
        # Loop through video files
        for video_file in folder.iterdir():
            if video_file.is_file() and video_file.suffix.lower() in VIDEO_EXTENSIONS:
                print(f"    Comparing with video: {video_file.name}")
                # Ensure the video file name contains the episode code
                if video_regex.search(video_file.name.lower()) and ep_code in video_file.name.lower():
                    new_name = video_file.with_suffix('.srt')
                    print(f"    ✅ Match found! Renaming {srt_file.name} → {new_name.name}")

                    # Check if the new name already exists
                    if new_name.exists():
                        print(f"    ⚠️ Target file {new_name.name} already exists. Skipping renaming.")
                        continue  # Skip renaming and continue with the next file
                    else:
                        srt_file.rename(new_name)
                        matched = True
                    break
        if not matched:
            print("    ⚠️ No matching video file found.")
    else:
        print("  ⚠️ No episode code found in filename.")
