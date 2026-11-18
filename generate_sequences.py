"""Regenerate chronological image sequences from the local recorded clips.

Requires Pillow and either FFmpeg on PATH or imageio-ffmpeg.
The method-section virtual-gripper video remains a video on the page.
"""
from pathlib import Path
from io import BytesIO
import json
import re
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FRAME_WIDTH = 520
GAP = 12
LABEL_HEIGHT = 44
CLIPS = [
    "annotated-demo", "bottle-icl", "without-icl", "bottle-human",
    "bottle-robot", "banana-human", "cup-human", "cup-robot",
    "basket-human", "basket-robot",
]


def ffmpeg_path():
    executable = shutil.which("ffmpeg")
    if executable:
        return executable
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def label_font():
    for name in ("DejaVuSans.ttf", "Arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, 30)
        except OSError:
            pass
    return ImageFont.load_default(size=30)


def video_duration(executable, source):
    probe = subprocess.run(
        [executable, "-hide_banner", "-i", str(source)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", probe.stderr)
    if not match:
        raise RuntimeError("Unable to read clip duration: " + source.name)
    hours, minutes, seconds = map(float, match.groups())
    return hours * 3600 + minutes * 60 + seconds


def read_frame(executable, source, seconds):
    result = subprocess.run(
        [executable, "-v", "error", "-ss", f"{seconds:.4f}", "-i", str(source),
         "-frames:v", "1", "-vf", f"scale={FRAME_WIDTH}:-2", "-an",
         "-f", "image2pipe", "-c:v", "png", "pipe:1"],
        capture_output=True, check=True,
    )
    with Image.open(BytesIO(result.stdout)) as image:
        return image.convert("RGB")


def contact_sheet(frames, columns):
    rows = (len(frames) + columns - 1) // columns
    frame_height = round(FRAME_WIDTH * frames[0].height / frames[0].width)
    cell_height = frame_height + LABEL_HEIGHT
    result = Image.new(
        "RGB",
        (columns * FRAME_WIDTH + (columns + 1) * GAP,
         rows * cell_height + (rows + 1) * GAP),
        "#f3f4ef",
    )
    draw = ImageDraw.Draw(result)
    font = label_font()
    for index, frame in enumerate(frames):
        x = GAP + (index % columns) * (FRAME_WIDTH + GAP)
        y = GAP + (index // columns) * (cell_height + GAP)
        if frame.size != (FRAME_WIDTH, frame_height):
            frame = frame.resize((FRAME_WIDTH, frame_height), Image.Resampling.LANCZOS)
        result.paste(frame, (x, y))
        draw.text((x + 7, y + frame_height + 5), f"{index + 1:02d}", font=font, fill="#536264")
    return result


def save_variants(frames, stem):
    dimensions = {}
    for suffix, columns in (("", 3), ("-mobile", 2)):
        image = contact_sheet(frames, columns)
        name = stem + "-sequence" + suffix + ".webp"
        image.save(ROOT / name, "WEBP", quality=91, method=6)
        dimensions[name] = list(image.size)
    return dimensions


def main():
    executable = ffmpeg_path()
    metadata = {}
    for stem in CLIPS:
        source = ROOT / (stem + ".mp4")
        duration = video_duration(executable, source)
        end = duration - 0.1
        # Keep the no-context example inside the user's 36-second boundary.
        if stem == "without-icl":
            end = min(end, 35.9)
        times = [round(max(0.0, end) * index / 5, 4) for index in range(6)]
        frames = [read_frame(executable, source, time) for time in times]
        metadata[stem] = {
            "source_video": source.name,
            "duration_seconds": duration,
            "frame_times_seconds": times,
            "order": "left to right, then top to bottom",
            "images": save_variants(frames, stem),
        }
        print("Prepared " + stem, flush=True)

    # Reflow existing original figure keyframes for the banana task card.
    source = ROOT / "banana-orientation-success.webp"
    with Image.open(source) as image:
        if image.size != (2440, 300):
            raise ValueError("Unexpected banana keyframe sheet dimensions")
        frames = [image.crop((index * 408, 0, index * 408 + 400, 300)).convert("RGB")
                  for index in range(6)]
    metadata["banana-orientation"] = {
        "source_figure": source.name,
        "order": "original figure order; left to right, then top to bottom",
        "images": save_variants(frames, "banana-orientation"),
    }
    (ROOT / "sequences.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
