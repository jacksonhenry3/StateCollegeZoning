import random
import json
import colorsys
import folium
from collections import Counter

# Coordinates
latitude = 40.7934
longitude = -77.8600

# Load GeoJSON file
with open('county_zoning.geojson') as f:
    geojson_data = json.load(f)

# Count occurrences and calculate area for each zone code
zone_counter = Counter()
zone_area = {}
for feature in geojson_data['features']:
    zone_code = feature['properties']['Zoning']
    zone_counter[zone_code] += 1
    zone_area[zone_code] = zone_area.get(zone_code, 0) + feature['properties']['SHAPESTArea']

# Sort zone codes by total land area
sorted_zones = sorted(zone_area.items(), key=lambda x: x[1], reverse=True)
top_zones = dict(sorted_zones)

# Generate category-color mappings
categories = [
    "Low Density Residential",
    "Residential Zones",
    "Industrial Zones",
    "Natural and Conservation Zones",
    "Cultural and Recreational Zones",
    "Commercial Zones",
    "Agricultural Zones",
    "Mixed-Use Zones",
    "Commercial/Industrial Zones",
    "Specialized Zones"
]

hues = [i / len(categories) for i in range(len(categories))]
brightneses = [(i / len(categories)) / 5.0 + .7 for i in range(len(categories))]
saturations = [(i / len(categories)) / 5.0 + .4 for i in range(len(categories))]

random.shuffle(brightneses)
random.shuffle(saturations)

category_colors = {}
for category, hue, brightness, saturation in zip(categories, hues, brightneses, saturations):
    rgb_color = colorsys.hsv_to_rgb(hue, saturation, brightness)
    hex_color = "#" + "".join([hex(int(c * 255))[2:].zfill(2) for c in rgb_color])
    category_colors[category] = hex_color

# Category mapping
category_mapping = {
    "Suburban Single Family Residential": "Low Density Residential",
    "Rural Residential": "Low Density Residential",
    "Residential, Single Household Suburban": "Low Density Residential",
    "Residential, Single Family Suburban": "Low Density Residential",
    "Rural Residence": "Low Density Residential",
    "Village/Rural Center": "Low Density Residential",
    "Residential - Office": "Low Density Residential",
    "Village Residential": "Low Density Residential",
    "Rural District": "Low Density Residential",
    "Residence 4": "Low Density Residential",
    "Residential, Special": "Low Density Residential",
    "Residence 3B": "Low Density Residential",
    "Agricultural Residential": "Low Density Residential",
    "Manufactured Home Residence": "Low Density Residential",
    "Medium Density Residential": "Low Density Residential",
    "Residential Urban": "Low Density Residential",
    "High Density Residential": "Residential Zones",
    "Residential-Office": "Low Density Residential",
    "Residential Suburban": "Low Density Residential",
    "Medium Density Residence": "Low Density Residential",
    "Two-Family Residential": "Low Density Residential",
    "Townhouse Residential": "Low Density Residential",
    "Residence 1": "Low Density Residential",
    "High Density Village Residential": "Residential Zones",
    "Residential-Commercial": "Low Density Residential",
    "Residential Office": "Low Density Residential",

    "Residential, Single Family": "Low Density Residential",
    "Residence 3H": "Low Density Residential",
    "Town Residential": "Low Density Residential",
    "Residential, Two Family": "Low Density Residential",
    "Low Density Residence": "Low Density Residential",
    "Residence Office": "Low Density Residential",
    "Single Family Residential": "Low Density Residential",
    "Residential, Low Density": "Low Density Residential",

    "General Industrial": "Commercial Zones",
    "Central Business": "Commercial Zones",
    "Highway Commercial": "Commercial Zones",
    "Regional Business Park": "Commercial Zones",
    "General Commercial District": "Commercial Zones",
    "Commercial Manufacturing": "Commercial Zones",
    "Commercial/Industrial": "Commercial Zones",
    "Commercial Planned": "Commercial Zones",
    "Downtown Commercial": "Commercial Zones",
    "Commercial General": "Commercial Zones",
    "Commercial Incentive": "Commercial Zones",
    "Commercial/Office": "Commercial Zones",
    "Commercial, Village": "Commercial Zones",
    "Commercial Transitional": "Commercial Zones",
    "Commercial": "Commercial Zones",
    "Gateway Commercial": "Commercial Zones",
    "Commercial, General": "Commercial Zones",
    "Office Commercial": "Commercial Zones",
    "Commercial - Industrial, Planned": "Commercial Zones",

    "Heavy Industrial": "Industrial Zones",
    "Limited Industrial": "Industrial Zones",
    "Industrial Enterprise": "Industrial Zones",
    "Industrial, General": "Industrial Zones",
    "Light Industial": "Industrial Zones",
    "Industrial Research Development/Light": "Industrial Zones",
    "Light Industry, Research and Development": "Industrial Zones",
    "Manufacturing Home Park": "Industrial Zones",
    "General Commercial/Light Industrial": "Industrial Zones",
    "Industrial": "Industrial Zones",

    "Natural Area": "Natural and Conservation Zones",
    "Woodland/Conservation District": "Natural and Conservation Zones",
    "Woodland/Conservation": "Natural and Conservation Zones",
    "Forest/Gameland": "Natural and Conservation Zones",
    "Stream Valley": "Natural and Conservation Zones",
    "Open Space/Forest": "Natural and Conservation Zones",
    "Forested Conservation": "Natural and Conservation Zones",
    "Natural Resources and Recycling": "Natural and Conservation Zones",
    "Agricultural Preservation": "Natural and Conservation Zones",
    "Conservation": "Natural and Conservation Zones",
    "Quarry": "Natural and Conservation Zones",
    "Forest Preservation": "Natural and Conservation Zones",

    "Cultural": "Cultural and Recreational Zones",
    "Park": "Cultural and Recreational Zones",
    "Recreation/Conservation": "Cultural and Recreational Zones",
    "Traditional Town": "Cultural and Recreational Zones",
    "Medical Campus": "Cultural and Recreational Zones",
    "University Planned": "Cultural and Recreational Zones",
    "Open Space": "Cultural and Recreational Zones",
    "Recreation Use": "Cultural and Recreational Zones",

    "Natural Resources": "Agricultural Zones",
    "Prime Agricultural District": "Agricultural Zones",
    "Conservation/Agriculture": "Agricultural Zones",
    "Rural Agriculture": "Agricultural Zones",
    "Agriculture": "Agricultural Zones",
    "Agriculture & Open Space": "Agricultural Zones",
    "Agriculture Research": "Agricultural Zones",

    "Highway Mixed Use": "Mixed-Use Zones",
    "Village Mixed-Use": "Mixed-Use Zones",
    "Mixed Use": "Mixed-Use Zones",

    "Planned Research Business Park": "Specialized Zones",
    "Public/Semi-Public": "Specialized Zones",
    "Water Front Business": "Specialized Zones",
    "Planned Community": "Specialized Zones",
    "Commercial Aviation": "Specialized Zones",
    "Planned Regional Business": "Specialized Zones",
    "Interchange Commercial": "Specialized Zones",
    "Planned Office": "Specialized Zones",
    "Residence Office A": "Specialized Zones",
    "Planned Commercial 2": "Commercial Zones",
    "Planned Commercial 3": "Commercial Zones",
    "Planned Commercial 1": "Commercial Zones",
    "Planned Commercial": "Commercial Zones",
    "Planned Airport": "Specialized Zones",
    "Planned Residential": "Low Density Residential",
    "Residence 2": "Low Density Residential",
    "Mineral Extraction": "Specialized Zones",
    "Urban Village": "Specialized Zones",
    "Rural Heritage": "Specialized Zones",
    "Forest": "Natural and Conservation Zones",
    "Mobile Home Park": "Residential Zones",
    "General Commercial": "Commercial Zones",
    "Residential": "Residential Zones",
    "Village": "Residential Zones",
    "Terraced Streetscape": "Specialized Zones",
    "Residence 3": "Residential Zones",
    "Light Industrial": "Industrial Zones",
    "Two Family Residential": "Residential Zones",
    "Public": "Specialized Zones",
    "Rural Commercial": "Commercial Zones",
    "Office Buffer 2": "Specialized Zones",
    "Office Buffer": "Specialized Zones",
    "Manufactured Home Park": "Residential Zones",
    "Low Density Residential": "Low Density Residential",
    "Rural Resource": "Specialized Zones",
    "Suburban Residential": "Low Density Residential",
    "Residential Medium Density": "Residential Zones",
    "Agricultural Development": "Agricultural Zones",
    "Multifamily Residential": "Residential Zones",
    "Multi-Family Residential": "Residential Zones",
    "Residential, Medium Density": "Residential Zones",
    "Residential District": "Residential Zones",
    "Commercial, GC": "Commercial Zones",
    "General Residential": "Residential Zones",
    "Conservation/Woodland": "Natural and Conservation Zones",
    "Low Density Village Residential": "Low Density Residential",
    "Village Mixed Use": "Mixed-Use Zones",
}


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

term_color_mapping = {}
for term, category in category_mapping.items():
    general_color = category_colors[category]
    hsv = colorsys.rgb_to_hsv(*hex_to_rgb(general_color))
    new_hue = hsv[0]
    new_color = colorsys.hsv_to_rgb(new_hue, hsv[1], hsv[2])
    new_color = '#%02x%02x%02x' % tuple([int(x) for x in new_color])
    term_color_mapping[term] = new_color

# Create the map
m = folium.Map(location=[latitude, longitude], zoom_start=14)

# Style GeoJSON features and add to the map
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'fillColor': term_color_mapping.get(feature['properties']['Zoning'], '#000'),
        'color': 'white',
        'weight': .5,
        'fillOpacity': 0.45
    },
    tooltip=folium.GeoJsonTooltip(fields=['Zoning'], aliases=['Zone Code'])
).add_to(m)

# Create and add legend to the map
legend_html = '<div style="position: fixed; top: 50px; left: 50px; background-color: #EEE; padding: 10px; border: 1px solid black; z-index: 1000;">'
for prefix, color in category_colors.items():
    legend_html += f'<div><span style="color: {color}; font-size: 16px;">■</span> {prefix}</div>'
legend_html += '</div>'
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map as an HTML file
m.save('index.html')
