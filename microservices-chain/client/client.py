import asyncio
import json
import httpx

API = "http://127.0.0.1:8053"

def pretty(title: str, data):
    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))

async def main():
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(base_url=API, timeout=timeout) as s:
        # 1) Ping (GET)
        r = await s.get("/ping")
        r.raise_for_status()
        pretty("PING", r.json())

        # 2) Hello (GET com query string)
        r = await s.get("/hello", params={"name": "Ana"})
        r.raise_for_status()
        pretty("HELLO", r.json())

        # 3) Echo (POST com JSON)
        r = await s.post("/echo", json={"text": "Welcome Ana!"})
        r.raise_for_status()
        pretty("ECHO", r.json())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except httpx.HTTPError as e:
        print("HTTP error:", e)
    except Exception as e:
        print("Unexpected error:", e)
