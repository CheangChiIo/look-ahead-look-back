# Look Ahead to Look Back

Project website for **Selective Context Acquisition from Human Videos for World-Action Models**.

[Open the project page](https://cheangchiio.github.io/look-ahead-look-back/)

## Editing the page

This is a static website. No build step or web framework is required.

- Edit `index.html` for authors, text, captions, links, and section content.
- Edit `styles.css` for layout, colors, and responsive styling.
- Edit `app.js` for video behavior, tabs, image enlargement, and data tables.
- Replace a media file while retaining its filename to update its content.
- When result values change, update `results.json`, regenerate the corresponding figures with `generate_results.py` (requires Matplotlib), and update the headline metrics, task badges, effect-size prose, and figure alt text in `index.html` together.
- Replace `paper.pdf` or `supplementary.pdf` to update the public reading copies.

You can edit text files directly in GitHub's web editor. Commit changes to the `main` branch. GitHub Pages publishes from the repository root and updates the website automatically.

For local preview, run `python -m http.server 8765` in this directory and open `http://localhost:8765`.

## Media and results

The page uses recorded human and robot videos, source photographs from the research figures, and figures from the manuscript. The ordered banana sequences are keyframes, with the method and outcome labels retained. Overview playback speed is indicated beside the video; recorded clips appear in the task gallery. The no-context comparison retains the first 36 seconds.

Reported success rates and evaluation conditions are included alongside the figures and in `results.json`.

## Authors

Ziyu Gong, Ziyao Zheng, Qi Lu, Pengfei Ning, Haotian Xiong, Tianjun Shi, Jiawei Xu, Cheng-zhong Xu, and Li Li.

University of Macau.
