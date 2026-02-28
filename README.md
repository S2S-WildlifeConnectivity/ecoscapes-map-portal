# EcoScapes Map Viewer

A simple web application for toggling between two map views with a clean, modern interface.

## Features

- Toggle between two map views with a single click
- Responsive design that works on all devices
- Easy configuration via JSON
- Deployable to GitHub Pages

## Local Development

1. Clone the repository:
   ```bash
   git clone git@github.com:NiallxD/ecoscapes-maps.git
   cd ecoscapes-maps
   ```

2. Run the local server:
   ```bash
   python -m http.server 8000
   ```

3. Open in your browser:
   ```
   http://localhost:8000/sample/
   ```

## Configuration

Edit `map_config.json` to add or modify map views. Each entry should have:

```json
{
    "page_name": {
        "map1_url": "https://example.com/map1",
        "map2_url": "https://example.com/map2"
    }
}
```

## Icon Font System

This project uses **IcoMoon** for reliable icon font generation and management. The system provides professional-quality icons with consistent sizing and cross-browser compatibility.

### Quick Icon Updates

**Automated Script (Recommended)**:
```bash
npm run icons
# or
./update-icons.sh
```

Follow the instructions, then after downloading from IcoMoon:
```bash
./update-icons.sh --extract
```

### Adding New Icons

1. **Add SVG Icons**:
   - Place your SVG icons in the `assets/icons` directory
   - Each SVG file should be named with the icon name you want (e.g., `home.svg`, `settings.svg`)
   - Icons can be any size - IcoMoon will standardize them

2. **Generate Font with IcoMoon**:
   - Go to https://icomoon.io/app
   - Click "Import Icons" → select all SVGs from `assets/icons/`
   - Click "Generate Font"
   - Configure settings:
     - Font Name: `custom-icons`
     - Class Prefix: `icon-`
   - Click "Download"

3. **Update Project**:
   - Extract the downloaded zip to `assets/icomoon/`
   - Run: `./update-icons.sh --extract`
   - Clear browser cache (Ctrl+Shift+R)

4. **Using Icons in HTML**:
   ```html
   <i class="icon-home"></i>
   <i class="icon-settings"></i>
   ```

5. **Using Icons in Configuration**:
   ```json
   {
     "icon": "icon-home"
   }
   ```

### File Structure

```
assets/
├── icons/           # Your SVG files
└── icomoon/         # IcoMoon project files

static/fonts/
├── icomoon.*        # Font files (eot, ttf, woff, svg)
├── custom-icons.css # Generated CSS with icon classes
└── backup/          # Automatic backups
```

### Benefits

✅ **Professional Quality**: IcoMoon provides reliable font generation  
✅ **Visual Preview**: See icons before building  
✅ **Consistent Sizing**: All icons standardized automatically  
✅ **Cross-Browser**: Works in all browsers including IE  
✅ **Easy Updates**: Simple script-based workflow  
✅ **Safe**: Automatic backups prevent breaking changes

### Detailed Documentation

For complete workflow details and troubleshooting, see: **[ICON_WORKFLOW.md](ICON_WORKFLOW.md)**

## Deployment to GitHub Pages 

1. Run the deployment script:
   ```bash
   python deploy_to_ecoscapes.py
   ```
   
2. Follow the on-screen instructions to complete the GitHub Pages setup.

3. Your site will be available at:
   ```
   https://s2s-wildlifeconnectivity.github.io/ecoscapes-map-portal/
   ```

## Adding New Pages

1. Add a new entry to `map_config.json`
2. Access it at: `https://s2s-wildlifeconnectivity.github.io/ecoscapes-map-portal/'
`

# Updated for deployment
# CSS copying fix
