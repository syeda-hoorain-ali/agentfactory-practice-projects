import os, sys, urllib.request, json

def load_env(path=".env"):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

def main():
    if len(sys.argv) != 2:
        print("usage: python3 fire_routine_b.py <claude/digest-branch-name>")
        sys.exit(1)
    branch = sys.argv[1]
    env = load_env()
    routine_id = env["ROUTINE_B_ID"]
    token = env["ROUTINE_B_TOKEN"]

    url = f"https://api.anthropic.com/v1/claude_code/routines/{routine_id}/fire"
    body = json.dumps({"text": branch}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "anthropic-beta": "experimental-cc-routine-2026-04-01",
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())

if __name__ == "__main__":
    main()
