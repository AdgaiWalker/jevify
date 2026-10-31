import urllib.request
import urllib.error
import json
import time

URL = "https://api.typesafe.ai/v1/systemone"
KEYS = [
    "apikey_2998e6693e0329444758839b8e9f443cf4e_b83254734358781cd5052308f8a0426736d50140c91fe368289899f68461840e",
    "apikey_2167e318d347b9594f3aae2b73e465d5ad8d_1f3c179c80d85547eef274ef039d94198e9a3096f85769a4818ca2339f9f8064"
]

payload = {
    "model": "jev-latest",
    "state": "The user reported: 'Payment gateway timed out during checkout, user was debited 100 USD but order shows cancelled.'",
    "questions": {
        "severity": {
            "type": "score",
            "instructions": "Rate severity of the incident for business operations.",
            "criteria": [
                "Minor / cosmetic issue",
                "Partial degraded service with existing workaround",
                "Critical blocking financial loss or major failure"
            ]
        },
        "target_team": {
            "type": "choice",
            "instructions": "Which department should handle this ticket?",
            "criteria": {
                "billing": "Financial transactions, refunds, duplicate charges, payment errors",
                "devops": "Server outages, network latency, infrastructure down",
                "frontend": "UI glitch, styling, browser compatibility"
            }
        },
        "needs_immediate_escalation": {
            "type": "noul",
            "instructions": "Does this require on-call engineer immediate paging?"
        }
    }
}

for idx, key in enumerate(KEYS):
    print(f"\n--- Testing API Key {idx+1} ---")
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "TypeSafe-Client/1.0"
        },
        method="POST"
    )
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            elapsed = time.time() - start_time
            body = resp.read().decode("utf-8")
            print(f"Status: {resp.status} (Elapsed: {elapsed*1000:.1f}ms)")
            parsed = json.loads(body)
            print("Response:", json.dumps(parsed, indent=2, ensure_ascii=False))
            break
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start_time
        err_body = e.read().decode("utf-8")
        print(f"HTTPError: {e.code} (Elapsed: {elapsed*1000:.1f}ms)")
        print("Error Body:", err_body)
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"Exception: {e} (Elapsed: {elapsed*1000:.1f}ms)")
