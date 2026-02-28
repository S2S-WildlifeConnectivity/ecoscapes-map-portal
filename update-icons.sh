#!/bin/bash

# IcoMoon Font Update Script
# Usage: ./update-icons.sh

echo "🎯 IcoMoon Font Update Script"
echo "================================"

# Check if assets/icons directory exists
if [ ! -d "assets/icons" ]; then
    echo "❌ assets/icons directory not found"
    exit 1
fi

# Count SVG files
SVG_COUNT=$(find assets/icons -name "*.svg" | wc -l)
echo "📊 Found $SVG_COUNT SVG files in assets/icons/"

echo ""
echo "📋 Instructions:"
echo "1. Open https://icomoon.io/app"
echo "2. Click 'Import Icons'"
echo "3. Select all SVGs from: assets/icons/"
echo "4. Click 'Generate Font'"
echo "5. Configure settings (optional):"
echo "   - Font Name: custom-icons"
echo "   - Class Prefix: icon-"
echo "   - CSS Prefix: .icon-"
echo "6. Click 'Download'"
echo "7. Extract the downloaded zip"
echo "8. Run this script again with: ./update-icons.sh --extract"
echo ""

if [ "$1" == "--extract" ]; then
    echo "🔧 Extracting IcoMoon files..."
    
    # Check if icomoon directory exists in assets
    if [ ! -d "assets/icomoon" ]; then
        echo "❌ assets/icomoon directory not found"
        echo "   Please extract IcoMoon zip to assets/icomoon/ first"
        exit 1
    fi
    
    # Backup current font files
    echo "💾 Backing up current fonts..."
    mkdir -p static/fonts/backup
    cp static/fonts/icomoon.* static/fonts/backup/ 2>/dev/null || true
    cp static/fonts/custom-icons.css static/fonts/backup/ 2>/dev/null || true
    
    # Copy new font files
    echo "📁 Copying new font files..."
    cp assets/icomoon/fonts/* static/fonts/
    
    # Create new CSS with correct paths
    echo "🎨 Updating CSS..."
    cat > static/fonts/custom-icons.css << 'EOF'
@font-face {
  font-family: 'custom-icons';
  src:  url('/static/fonts/icomoon.eot');
  src:  url('/static/fonts/icomoon.eot#iefix') format('embedded-opentype'),
    url('/static/fonts/icomoon.ttf') format('truetype'),
    url('/static/fonts/icomoon.woff') format('woff'),
    url('/static/fonts/icomoon.svg#icomoon') format('svg');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}

[class^="icon-"], [class*=" icon-"] {
  font-family: 'custom-icons' !important;
  speak: never;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  font-size: 1em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon:before {
  font-family: 'custom-icons' !important;
  font-style: normal;
  font-weight: normal !important;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
EOF
    
    # Append icon class definitions
    tail -n +28 assets/icomoon/style.css >> static/fonts/custom-icons.css
    
    echo "✅ Font update complete!"
    echo "📂 Files updated:"
    echo "   - static/fonts/icomoon.* (font files)"
    echo "   - static/fonts/custom-icons.css (CSS)"
    echo ""
    echo "🔄 Next steps:"
    echo "   1. Clear browser cache (Ctrl+Shift+R)"
    echo "   2. Test icons in your application"
    echo "   3. Commit changes if working correctly"
fi
