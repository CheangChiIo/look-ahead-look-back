# Look Ahead to Look Back

Project website for **Selective Context Acquisition from Human Videos for World-Action Models**.

[Open the project page](https://cheangchiio.github.io/look-ahead-look-back/)

## Editing the page

This is a static website. No build step or web framework is required.

- Edit `index.html` for authors, text, captions, links, and section content.
- Edit `styles.css` for layout, colors, and responsive styling. Page text and chart labels use Arial/Helvetica; body text and controls use relative font sizes.
- Edit `app.js` for video behavior, tabs, image enlargement, and data tables.
- Run `python generate_sequences.py` after replacing a source recording to regenerate its six-frame desktop and mobile sequences (requires Pillow and FFmpeg or imageio-ffmpeg). Frame selection and image dimensions are recorded in `sequences.json`.
- The virtual-gripper illustration in the method section retains its video player.
- When result values change, update `results.json`, regenerate both desktop and mobile figures with `generate_results.py` (requires Matplotlib), and update the headline metrics, task badges, effect-size prose, and figure alt text in `index.html` together.
- Replace `paper.pdf` or `supplementary.pdf` to update the public reading copies.

You can edit text files directly in GitHub's web editor. Commit changes to the `main` branch. GitHub Pages publishes from the repository root and updates the website automatically.

For local preview, run `python -m http.server 8765` in this directory and open `http://localhost:8765`.

## Media and results

The page presents recorded human and robot interactions as six-frame chronological image sequences, with frame numbers. Read each sequence left to right, then top to bottom; click to enlarge. The banana configuration examples retain the original research-figure keyframes. The no-context comparison uses only the first 36 seconds. Only the method-section virtual-gripper illustration remains a video. Original recordings are retained as regeneration inputs.

Reported success rates and evaluation conditions are included alongside the figures and in `results.json`.

## Authors

Ziyu Gong, Ziyao Zheng, Qi Lu, Pengfei Ning, Haotian Xiong, Tianjun Shi, Jiawei Xu, Cheng-zhong Xu, and Li Li.

University of Macau.
