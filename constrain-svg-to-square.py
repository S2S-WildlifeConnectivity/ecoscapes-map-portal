#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
import re

def analyze_svg_bounds(svg_path):
    """Analyze SVG and return bounding box information"""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        # Find all path elements
        paths = root.findall('.//path', namespaces=root.nsmap)
        if not paths:
            print(f"⚠️  No path elements found in {svg_path}")
            return None, None, None, None
        
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')
        
        # Analyze each path to find bounds
        for path in paths:
            d = path.get('d')
            if d:
                # Extract coordinates from path data
                coords = re.findall(r'[MmLlHhVvCcSsQqTtAa][\s-]*([-\d.?\d+(?:\.\d+)?)(?![\s-]*[MmLlHhVvCcSsQqTtAa][\s-]*([-\d.?\d+(?:\.\d+)?)(?![\s-]*[ZzLlHhVvCcSsQqTtAa])', d)
                
                for coord in coords:
                    if coord and coord[0]:  # Skip empty coordinates
                        x, y = map(float, coord[0].split(','))
                        min_x = min(min_x, x)
                        max_x = max(max_x, x)
                        min_y = min(min_y, y)
                        max_y = max(max_y, y)
        
        if min_x == float('inf') or max_x == float('inf'):
            print(f"⚠️  Could not determine bounds for {svg_path}")
            return None, None, None, None
        
        width = max_x - min_x
        height = max_y - min_y
        
        # Determine if it's already square or close to square
        aspect_ratio = width / height if height > 0 else 0
        
        return {
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'is_square': abs(aspect_ratio - 1.0) < 0.1
        }

def constrain_to_square(svg_path, output_path):
    """Constrain SVG to a square by adding a viewBox that centers the content"""
    try:
        bounds = analyze_svg_bounds(svg_path)
        if not bounds:
            print(f"❌ Cannot process {svg_path}: no bounds found")
            return False
        
        width, height = bounds['width'], bounds['height']
        
        # Use the larger dimension for the square
        size = max(width, height)
        half_size = size / 2
        
        # Create new viewBox that centers the content
        # Format: "min_x min_y width height"
        viewbox = f"{-half_size:.3f} {-half_size:.3f} {size:.3f} {size:.3f}"
        
        # Read the original SVG
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Insert new viewBox after the opening svg tag
        content = re.sub(
            r'<svg[^>]*>',
            f'<svg viewBox="{viewbox}"',
            content,
            count=1
        )
        
        # Write the constrained SVG
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {svg_path}: {e}")
        return False

def main():
    icons_dir = './assets/icons'
    
    if not os.path.exists(icons_dir):
        print(f"❌ Icons directory not found: {icons_dir}")
        return
    
    svg_files = [f for f in os.listdir(icons_dir) if f.endswith('.svg')]
    
    print(f"🔍 Analyzing {len(svg_files)} SVG files...")
    
    processed = 0
    squares_made = 0
    
    for svg_file in svg_files:
        input_path = os.path.join(icons_dir, svg_file)
        output_path = os.path.join(icons_dir, svg_file)
        
        if constrain_to_square(input_path, output_path):
            processed += 1
            squares_made += 1
        else:
            print(f"⚠️  Skipped {svg_file}")
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Processed: {processed} files")
    print(f"  📐 Made square: {squares_made} files")
    print(f"  📁 Total SVG files: {len(svg_files)}")
    
    if squares_made > 0:
        print(f"\n🎯 Next step: Rebuild icon font with npm run build:icons")

if __name__ == '__main__':
    main()
