#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
import xml.etree.ElementTree as ET
import re

PORT = 8081

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/markers':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            try:
                # Fetch KML data
                kml_url = 'https://www.google.com/maps/d/kml?forcekml=1&mid=1FTxaAFeVVhBaC2YqCh6iWr5bzrxg6ko'
                with urllib.request.urlopen(kml_url) as response:
                    kml_data = response.read().decode('utf-8')

                # Fetch HTML page to extract coordinates
                html_url = 'https://www.google.com/maps/d/viewer?mid=1FTxaAFeVVhBaC2YqCh6iWr5bzrxg6ko'
                with urllib.request.urlopen(html_url) as response:
                    html_data = response.read().decode('utf-8')

                # Extract coordinates from HTML using regex
                coord_pattern = r'\[(50\.\d+),(7\.\d+)\]'
                coordinates = re.findall(coord_pattern, html_data)
                coord_dict = {i: (float(lat), float(lng)) for i, (lat, lng) in enumerate(coordinates)}

                # Parse KML
                root = ET.fromstring(kml_data)

                # Define namespaces
                namespaces = {
                    'kml': 'http://www.opengis.net/kml/2.2',
                    'gx': 'http://www.google.com/kml/ext/2.2'
                }

                markers = []
                placemarks = root.findall('.//kml:Placemark', namespaces)

                for idx, placemark in enumerate(placemarks):
                    name_el = placemark.find('kml:name', namespaces)
                    if name_el is None:
                        continue

                    name = name_el.text

                    # Extract incident count and IDs from ExtendedData
                    extended_data = placemark.find('kml:ExtendedData', namespaces)
                    incident_count = 1
                    incident_ids = []

                    if extended_data is not None:
                        for data in extended_data.findall('kml:Data', namespaces):
                            data_name = data.get('name')
                            value_el = data.find('kml:value', namespaces)
                            if value_el is not None and value_el.text:
                                if data_name == 'No. of Incidents per Location':
                                    try:
                                        incident_count = int(float(value_el.text))
                                    except:
                                        pass
                                elif data_name == 'Incident-Ids':
                                    incident_ids = [id.strip() for id in value_el.text.split(',')]

                    # Get coordinates from extracted dict
                    if idx in coord_dict:
                        lat, lng = coord_dict[idx]

                        markers.append({
                            'name': name,
                            'lat': lat,
                            'lng': lng,
                            'count': incident_count,
                            'incidents': incident_ids
                        })

                result = {
                    'count': len(markers),
                    'markers': markers
                }
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                print(f"Error: {e}")
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            super().do_GET()

# Allow port reuse
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print(f"Open http://localhost:{PORT}/index.html in your browser")
    httpd.serve_forever()
