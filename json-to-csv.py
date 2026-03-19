import json
import csv
import re


def extract_source_parts(source_html):
    """Extract raw URL and link text from an HTML anchor tag, or return as-is."""
    if not source_html:
        return "", ""
    match = re.search(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', source_html)
    if match:
        return match.group(1), match.group(2)
    # Not an anchor tag — treat as plain URL with no custom link text
    return source_html.strip(), ""


def main():
    input_file = 'map_config.json'
    output_file = 'ecoscapes-export.csv'

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fieldnames = [
        'Theme', 'ThemeInfo', 'Theme Icon',
        'SubTheme', 'SubthemeInfo', 'SubThemeIcon',
        'Indicator', 'IndicatorInfo', 'Source', 'LinkText',
        'UnitOfMeasure', 'posttag', 'IndicatorIcon', 'map1', 'map2'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for theme in data.get('themes', []):
            for subtheme in theme.get('subthemes', []):
                for indicator_id in subtheme.get('indicators', []):
                    indicator = data.get('indicators', {}).get(indicator_id, {})
                    if not indicator:
                        continue

                    source_url, link_text = extract_source_parts(indicator.get('source', ''))

                    writer.writerow({
                        'Theme': theme.get('name', ''),
                        'ThemeInfo': theme.get('description', ''),
                        'Theme Icon': theme.get('icon', ''),
                        'SubTheme': subtheme.get('name', ''),
                        'SubthemeInfo': subtheme.get('description', ''),
                        'SubThemeIcon': subtheme.get('icon', ''),
                        'Indicator': indicator.get('title', ''),
                        'IndicatorInfo': indicator.get('description', ''),
                        'Source': source_url,
                        'LinkText': link_text,
                        'UnitOfMeasure': indicator.get('unit_of_measure', ''),
                        'posttag': '',
                        'IndicatorIcon': indicator.get('icon', ''),
                        'map1': indicator.get('map1_url', ''),
                        'map2': indicator.get('map2_url', '')
                    })

    print(f"✅ Export complete: {output_file} created.")


if __name__ == "__main__":
    main()