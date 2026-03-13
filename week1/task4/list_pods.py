import os
import requests

TOKEN_PATH = "/var/run/secrets/tokens/token"
CA_PATH    = "/var/run/secrets/tokens/ca.crt"
NAMESPACE  = os.environ.get("TARGET_NAMESPACE", "task1")

token = open(TOKEN_PATH).read().strip()
api   = f"https://kubernetes.default.svc/api/v1/namespaces/{NAMESPACE}/pods"

resp = requests.get(
    api,
    headers={"Authorization": f"Bearer {token}"},
    verify=CA_PATH
)

pods = resp.json()

if "items" not in pods:
    print("API error:", pods)
else:
    print(f"pod list in {NAMESPACE} namespace:\n")
    for item in pods["items"]:
        print(item["metadata"]["name"])
