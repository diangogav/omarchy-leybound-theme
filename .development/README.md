# Wallpaper generation

The eight release wallpapers are deterministic SVG scenes rendered to 4K PNG.

## Requirements

- Python 3
- `rsvg-convert` from librsvg
- ImageMagick (only for the contact sheet)

## Rebuild the wallpapers

Run from the repository root:

```bash
scenes=(sigil veil rift summoning eclipse constellation leylines grimoire)
files=(0-sigil 1-veil 2-rift 3-summoning 4-eclipse 5-constellation 6-leylines 7-grimoire)

for i in "${!scenes[@]}"; do
  python .development/generate-wallpapers.py "${scenes[$i]}" \
    | rsvg-convert -w 3840 -h 2160 -o "backgrounds/${files[$i]}.png"
done
```

The generator uses only deterministic arithmetic and seeded pseudo-random sequences. Rebuilding with the same renderer version produces byte-identical PNGs.

## Rebuild the contact sheet

```bash
magick montage backgrounds/*.png \
  -thumbnail 640x360 \
  -tile 2x4 \
  -geometry 640x360+12+12 \
  -background '#04050a' \
  .github/assets/wallpapers.png
```

`preview.png` is the publication preview for the theme selector and should remain 640×360 sRGB.
