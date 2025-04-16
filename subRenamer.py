from pathlib import Path
import re

""" It works with files containing format s02e03 case insensitive"""

VIDEO_EXTENSIONS = {
    '.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv',
    '.webm', '.mpeg', '.mpg', '.m4v', '.3gp', '.3g2',
    '.ts', '.vob', '.rm', '.rmvb', '.asf', '.f4v',
    '.m2ts', '.divx'
}

folder = Path(__file__).parent

srt_regex = re.compile(r'[sS]\d{2}[eE]\d{2}', re.IGNORECASE)
video_regex = re.compile(r'[sS]\d{2}[eE]\d{2}', re.IGNORECASE)

for srt_file in folder.glob("*.srt"):
    print(f"\nChecking SRT file: {srt_file.name}")
    match = srt_regex.search(srt_file.name)

    if match:
        ep_code = match.group(0).lower()
        print(f"  Episode code extracted: {ep_code}")

        matched = False

        for video_file in folder.iterdir():
            if video_file.is_file() and video_file.suffix.lower() in VIDEO_EXTENSIONS:
                print(f"    Comparing with video: {video_file.name}")

                if video_regex.search(video_file.name.lower()) and ep_code in video_file.name.lower():
                    new_name = video_file.with_suffix('.srt')
                    print(f"    ✅ Match found! Renaming {srt_file.name} → {new_name.name}")

                    if new_name.exists():
                        print(f"    ⚠️ Target file {new_name.name} already exists. Skipping renaming.")
                        continue
                    else:
                        srt_file.rename(new_name)
                        matched = True
                    break
        if not matched:
            print("    ⚠️ No matching video file found.")
    else:
        print("  ⚠️ No episode code found in filename.")
