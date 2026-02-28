# Icon Font Management

This project uses **IcoMoon** for reliable icon font generation.

## Quick Update Workflow

### Method 1: Automated Script (Recommended)
```bash
./update-icons.sh
```
Follow the instructions, then after downloading from IcoMoon:
```bash
./update-icons.sh --extract
```

### Method 2: Manual Steps
1. **Generate Font**: Go to https://icomoon.io/app
2. **Import Icons**: Select all SVGs from `assets/icons/`
3. **Configure**: 
   - Font Name: `custom-icons`
   - Class Prefix: `icon-`
4. **Download**: Get the font kit
5. **Extract**: Place in `assets/icomoon/`
6. **Run**: `./update-icons.sh --extract`

## File Structure

```
assets/
├── icons/           # Your SVG files (97 icons)
├── icomoon/         # IcoMoon project files
└── icons-backup/    # (removed - use git history)

static/fonts/
├── icomoon.eot      # IE support
├── icomoon.ttf      # Standard format
├── icomoon.woff     # Modern browsers
├── icomoon.svg      # Fallback
├── custom-icons.css  # Generated CSS with icon classes
└── backup/          # Automatic backups
```

## Integration Points

### CSS Loading
```html
<link rel="stylesheet" href="{% static 'fonts/custom-icons.css' %}">
```

### Icon Usage
```html
<i class="icon-coyote"></i>
<i class="icon-beaver"></i>
```

### Font Family
All icons use `font-family: 'custom-icons'` automatically.

## Adding New Icons

1. Add SVG to `assets/icons/your-icon.svg`
2. Run `./update-icons.sh`
3. Follow IcoMoon instructions
4. Update `map_config.json` if needed

## Troubleshooting

- **Icons not showing**: Clear browser cache (Ctrl+Shift+R)
- **Wrong icons**: Check `map_config.json` icon names
- **Tiny icons**: Ensure SVG viewBox is standardized (IcoMoon handles this)

## Benefits vs Fantasticon

✅ **Reliable**: Professional font generation  
✅ **Visual**: Preview icons before building  
✅ **Precise**: Control over spacing and alignment  
✅ **Stable**: No command-line issues  
✅ **Cross-platform**: Works in any browser
