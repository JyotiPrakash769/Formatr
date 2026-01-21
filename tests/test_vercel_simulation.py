import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    # Mimic Vercel import
    from api.index import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Check Status
    response = client.get("/api/status")
    if response.status_code == 200:
        print("Vercel Entry Point (api/index.py): PASSED")
        print(response.json())
    else:
        print(f"Vercel Entry Point FAILED {response.status_code} {response.text}")
        sys.exit(1)

    # Check Static File Serving (Root)
    response_static = client.get("/")
    if response_static.status_code == 200:
         print("Static File Serving (/): PASSED")
    else:
         print(f"Static File Serving (/) FAILED {response_static.status_code}")
         
except Exception as e:
    print(f"Vercel Simulation Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
