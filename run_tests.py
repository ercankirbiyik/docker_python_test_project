import time
import requests
import docker
import subprocess

# Selenium Grid'in sağlığını kontrol eden fonksiyon
def check_grid_health():
    grid_url = "http://localhost:4444/wd/hub/status"
    while True:
        try:
            response = requests.get(grid_url)
            if response.status_code == 200 and response.json()["value"]["ready"]:
                print("Selenium Grid is ready.")
                break
        except requests.exceptions.ConnectionError:
            print("Waiting for Selenium Grid...")
        time.sleep(2)

# Docker konteynerlerini başlatan fonksiyon
def start_docker_containers(node_count):
    client = docker.from_env()

    # Selenium Hub'ı başlatmadan önce mevcut bir hub olup olmadığını kontrol et
    try:
        client.containers.get("selenium-hub")
        print("Selenium Hub zaten çalışıyor.")
    except docker.errors.NotFound:
        print("Starting Selenium Hub...")
        client.containers.run(
            "selenium/hub:4.1.0",
            name="selenium-hub",
            ports={"4444/tcp": 4444},
            detach=True
        )

    # Chrome Node'ları başlat
    for i in range(node_count):
        print(f"Starting Chrome Node {i + 1}...")
        client.containers.run(
            "selenium/node-chrome:4.1.0",
            name=f"chrome-node-{i + 1}",
            environment={
                "SE_EVENT_BUS_HOST": "selenium-hub",
                "SE_EVENT_BUS_PUBLISH_PORT": 4442,
                "SE_EVENT_BUS_SUBSCRIBE_PORT": 4443,
            },
            ports={"5900/tcp": None},  # Her Node için VNC bağlantısı yapılabilir
            volumes={"/dev/shm": {'bind': '/dev/shm', 'mode': 'rw'}},  # Bu satırı düzelt
            detach=True
        )

# Testleri başlatan fonksiyon
def run_tests():
    print("Running tests...")
    subprocess.run(["docker", "run", "python-test"])

# Ana fonksiyon
def main(node_count=1):
    # Docker konteynerlerini başlat
    start_docker_containers(node_count)

    # Selenium Grid'in sağlığını kontrol et
    check_grid_health()

    # Testleri çalıştır
    run_tests()

# Komut satırından gelen node sayısına göre scripti çalıştırma
if __name__ == "__main__":
    # 1 ile 5 arasında bir node sayısı belirle
    node_count = int(input("Kaç tane Chrome Node başlatmak istersiniz (1-5)? "))
    if 1 <= node_count <= 5:
        main(node_count)
    else:
        print("Geçersiz node sayısı. Lütfen 1 ile 5 arasında bir sayı girin.")
