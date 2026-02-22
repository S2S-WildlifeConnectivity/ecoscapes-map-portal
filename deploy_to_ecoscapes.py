import os
import json
import shutil
import subprocess
from pathlib import Path


def collect_static():
    """Collect static files for GitHub Pages."""
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs', exist_ok=True)

    # Copy template and static files
    shutil.copytree('templates', 'docs/templates', dirs_exist_ok=True)

    # Create a simple HTML file for GitHub Pages
    with open('docs/index.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>EcoScapes Maps</title>
            <meta http-equiv="refresh" content="0; url=/ecoscapes-map-portal/sample/" />
        </head>
        <body>
            <p>Redirecting to map viewer...</p>
        </body>
        </html>
        """)

    # Load the map config to get theme groups
    with open('map_config.json') as f:
        config = json.load(f)

    # Create a version of the site for each theme group
    theme_groups = config.get('themeGroups', [])

    for group in theme_groups:
        group_dir = os.path.join('docs', group['id'])
        os.makedirs(group_dir, exist_ok=True)

        shutil.copy('templates/mapviewer/map.html', os.path.join(group_dir, 'index.html'))

        # Inject theme group logic
        with open(os.path.join(group_dir, 'index.html'), 'r+') as f:
            content = f.read()
            content = content.replace("<script>", f"""
            <script>
            if (!window.location.search.includes('theme_group=')) {{
                const newUrl = new URL(window.location.href);
                newUrl.searchParams.set('theme_group', '{group["id"]}');
                window.history.replaceState({{}}, '', newUrl);
            }}
            """)
            f.seek(0)
            f.write(content)
            f.truncate()

    # Default "all themes" version
    os.makedirs('docs/all', exist_ok=True)
    shutil.copy('templates/mapviewer/map.html', 'docs/all/index.html')

    # Copy map config
    shutil.copy('map_config.json', 'docs/map_config.json')

    # Local test server
    with open('docs/server.py', 'w') as f:
        f.write("""
        import http.server
        import socketserver
        import json
        import os

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/map_config.json':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    with open('map_config.json', 'rb') as f:
                        self.wfile.write(f.read())
                    return
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

        if __name__ == '__main__':
            PORT = 8000
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print(f"Serving at port {PORT}")
                httpd.serve_forever()
        """)


def deploy_to_github():
    """Deploy the static site to GitHub Pages (organisation repo)."""
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Deploy to GitHub Pages'], check=True)

    # Add org remote if missing
    try:
        subprocess.run([
            'git', 'remote', 'add', 'origin',
            'git@github.com:S2S-WildlifeConnectivity/ecoscapes-map-portal.git'
        ], check=True)
    except subprocess.CalledProcessError:
        pass  # Remote already exists

    # Check if there are changes to commit
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        subprocess.run(['git', 'commit', '-m', 'Deploy to GitHub Pages'], check=True)
    else:
        print("No changes to commit, proceeding with push...")
    
    # Push to master (your repo uses master)
    subprocess.run(['git', 'push', '-u', 'origin', 'master'], check=True)

    print("\nDeployment to GitHub Pages is ready!")
    print("1. Go to your repository settings on GitHub")
    print("2. Go to Pages settings")
    print("3. Set source to 'Deploy from a branch'")
    print("4. Select 'master' branch and '/docs' folder")
    print("5. Click Save")
    print("\nYour site will be available at:")
    print("   https://s2s-wildlifeconnectivity.github.io/ecoscapes-map-portal/")
    print("Example map page:")
    print("   https://s2s-wildlifeconnectivity.github.io/ecoscapes-map-portal/sample/")


if __name__ == '__main__':
    print("Preparing files for GitHub Pages...")
    collect_static()

    print("\nTo test locally:")
    print("1. cd docs")
    print("2. python3 -m http.server 8000")
    print("3. Open one of these URLs in your browser:")
    print("   - http://localhost:8000/all/ (All themes)")

    # Load config again for printing theme URLs
    with open('map_config.json') as f:
        config = json.load(f)
    for group in config.get('themeGroups', []):
        print(f"   - http://localhost:8000/{group['id']}/ ({group['name']} theme group)")

    print()

    deploy = input("Would you like to deploy to GitHub now? (y/n): ").lower()
    if deploy == 'y':
        deploy_to_github()
