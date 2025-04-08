
import os
import time
import requests
import subprocess

def wait_for_server(endpoint, timeout=30):
    print("🔄 Checking if the server is up...")
    for second in range(max_wait):
        try:
            resp = requests.get(endpoint)
            if resp.status_code in (200, 404):
                print("✅ Server is available.")
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise TimeoutError("⏰ Server startup timed out.")

def test_docker():
    print("🚧 Building the Docker image...")
    subprocess.run(["docker", "build", "-t", "flask-app", "."], check=True)

    print("📦 Launching the container...")
    subprocess.run(["docker", "run", "-d", "-p", "5000:5000", "--name", "test_container", "flask-app"], check=True)

    try:
        wait_for_server("http://localhost:5000")

        print("📨 Sending request to /score...")
        api_url = "http://localhost:5000/score"
        payload = {"text": "I love Python!"}
        response = requests.post(api_url, json=payload)

        assert response.status_code == 200, f"❌ Got {response.status_code}, expected 200"
        result = response.json()
        assert any(key in result for key in ("label", "prediction")), "Missing expected key in response JSON"

        print("🎉 Test successful. Response data:", result)

    finally:
        print("🧼 Tearing down the container...")
        subprocess.run(["docker", "stop", "test_container"])
        subprocess.run(["docker", "rm", "test_container"])

if __name__ == "__main__":
    run_container_test()
