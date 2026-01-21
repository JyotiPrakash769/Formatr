import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/api/status")
    
    if response.status_code == 200:
        print("Backend Status check: PASSED")
        print(response.json())
    else:
        print(f"Backend Status check: FAILED {response.status_code} {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"Backend Import/Startup Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
