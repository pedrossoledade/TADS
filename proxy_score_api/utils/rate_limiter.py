import requests
import time
import re

class RateLimiter:
    def __init__(self, min_interval=1.0):
        self.min_interval = min_interval  # janela fixa: 1 req/s
        self.next_allowed_time = time.time()

    def wait_for_slot(self):
        now = time.time()
        if now < self.next_allowed_time:
            sleep_time = self.next_allowed_time - now
            time.sleep(sleep_time)

    def update_after_response(self, response):
        now = time.time()

        if response.status_code == 429:
            # Penalidade do servidor
            try:
                api_response = response.json()
                print(api_response)
                
                error_msg = api_response.get("error", "")
                ms_match = re.search(r'(\d+)', error_msg)
                if ms_match:
                    wait_ms = int(ms_match.group(1))
                    self.next_allowed_time = now + wait_ms / 1000.0
                    return
            except Exception:
                pass

            retry_after = response.headers.get("retry-after")
            if retry_after:
                self.next_allowed_time = now + float(retry_after)
                return

            # fallback penalidade padrão
            self.next_allowed_time = now + 2.0

        else:
            # Enforce janela fixa (1 req/s)
            self.next_allowed_time = now + self.min_interval


# Instância global
rate_limiter = RateLimiter()
