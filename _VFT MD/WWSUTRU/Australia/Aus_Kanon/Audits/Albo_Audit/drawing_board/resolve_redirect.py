import requests

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF56cl5NaUUlDR6Vbd7K8aVKRBeOPFBEsr5p_Pet1Vgs6N53D8kAFyUylJmeUKp6pwqF9kqqheektX4l5dvGuOc6emvQTBqg_eKlVjkHHEenBCNCIN-99Ug4hJ8xtY1ZNeTs8DJwh-Rszk="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
try:
    resp = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
    print("Final URL:", resp.url)
except Exception as e:
    print("Error:", e)
