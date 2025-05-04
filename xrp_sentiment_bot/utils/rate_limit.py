import time, requests

def rate_limited_request(url, headers=None):
    retries = 5
    for i in range(retries):
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 429:
            wait = 2 ** (i + 1)
            print(f"Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
        else:
            res.raise_for_status()
    raise Exception("Rate limit failed after retries")

