import requests
import threading
import time
import statistics
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "https://jsonplaceholder.typicode.com"
TEST_URL = f"{BASE_URL}/posts"

def run_load_test(url, vus, duration_s, headers=None, method='GET', payload=None):
    results = []
    errors = []
    stop_event = threading.Event()
    lock = threading.Lock()

    def worker():
        while not stop_event.is_set():
            start = time.time()
            try:
                if method == 'GET':
                    resp = requests.get(url, headers=headers, timeout=10, verify=False)
                else:
                    resp = requests.request(method, url, headers=headers, json=payload, timeout=10, verify=False)
                duration_ms = (time.time() - start) * 1000
                with lock:
                    results.append({'duration_ms': duration_ms, 'status': resp.status_code, 'content_length': len(resp.content)})
                    if resp.status_code >= 400:
                        errors.append(resp.status_code)
            except Exception as e:
                with lock:
                    errors.append(str(e))

    threads = [threading.Thread(target=worker) for _ in range(vus)]
    for t in threads:
        t.start()
    time.sleep(duration_s)
    stop_event.set()
    for t in threads:
        t.join()

    if not results:
        return {}

    durations = [r['duration_ms'] for r in results]
    sorted_r = sorted(durations)
    n = len(sorted_r)
    return {
        "p50_ms": round(sorted_r[int(n * 0.50)], 2),
        "p95_ms": round(sorted_r[min(int(n * 0.95), n-1)], 2),
        "p99_ms": round(sorted_r[min(int(n * 0.99), n-1)], 2),
        "min_ms": round(sorted_r[0], 2),
        "max_ms": round(sorted_r[-1], 2),
        "error_rate_pct": round(len(errors) / (len(results) + len(errors)) * 100, 2) if (len(results) + len(errors)) > 0 else 0.0,
        "throughput_rps": round(len(results) / duration_s, 2),
        "vus_peak": vus,
        "duration_s": duration_s,
        "total_requests": len(results) + len(errors),
        "mode": "fallback_python",
        "sample_statuses": list(set([r['status'] for r in results[:5]])),
        "sample_content_length": results[0]['content_length'] if results else 0
    }

# TC-PERF-001 — GET /posts responde dentro do SLA (< 1500ms, 100 posts)
# Validações adicionais: status 200, retorna exatamente 100 posts
# Primeiro, validar a resposta básica (status + contagem)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("[CONFIG] Validando resposta base de GET /posts antes do teste de carga...")
try:
    r = requests.get(TEST_URL, timeout=15, verify=False)
    base_status = r.status_code
    base_body = r.json() if r.status_code == 200 else []
    base_count = len(base_body) if isinstance(base_body, list) else 0
    print(f"[VALIDATE] Status base: {base_status} | Posts retornados: {base_count}")
except Exception as e:
    base_status = 0
    base_count = 0
    print(f"[ERROR] Falha na validação base: {e}")

print(f"[CONFIG] 10 VUs, duração 30s, tipo: performance | threshold: p95 < 1500ms")
print(f"[RUN] Iniciando teste de carga (modo fallback Python)...")

metrics = run_load_test(TEST_URL, vus=10, duration_s=30)

if metrics:
    p95 = metrics['p95_ms']
    error_rate = metrics['error_rate_pct']

    print(f"[METRIC] p50={metrics['p50_ms']}ms, p95={p95}ms, p99={metrics['p99_ms']}ms")
    print(f"[METRIC] min={metrics['min_ms']}ms, max={metrics['max_ms']}ms")
    print(f"[METRIC] error_rate={error_rate}%, throughput={metrics['throughput_rps']} rps")
    print(f"[METRIC] total_requests={metrics['total_requests']}")

    threshold_p95 = p95 < 1500
    threshold_error = error_rate < 1.0
    threshold_status = base_status == 200
    threshold_count = base_count == 100

    print(f"[THRESHOLD] p(95) < 1500ms: {'PASSOU' if threshold_p95 else 'FALHOU'} (atual: {p95}ms)")
    print(f"[THRESHOLD] error rate < 1%: {'PASSOU' if threshold_error else 'FALHOU'} (atual: {error_rate}%)")
    print(f"[VALIDATE] status == 200: {'PASSOU' if threshold_status else 'FALHOU'} (atual: {base_status})")
    print(f"[VALIDATE] retorna exatamente 100 posts: {'PASSOU' if threshold_count else 'FALHOU'} (atual: {base_count})")

    overall_pass = threshold_p95 and threshold_error and threshold_status and threshold_count

    thresholds = [
        {"check": "p(95) < 1500ms", "result": "passed" if threshold_p95 else "failed", "actual": f"{p95}ms"},
        {"check": "error rate < 1%", "result": "passed" if threshold_error else "failed", "actual": f"{error_rate}%"},
        {"check": "status == 200", "result": "passed" if threshold_status else "failed", "actual": str(base_status)},
        {"check": "retorna exatamente 100 posts", "result": "passed" if threshold_count else "failed", "actual": str(base_count)}
    ]

    logs = [
        f"[CONFIG] 10 VUs, duração 30s, tipo: performance",
        f"[RUN] Script iniciado (modo fallback Python)",
        f"[VALIDATE] GET {TEST_URL} — status {base_status}, {base_count} posts retornados",
        f"[METRIC] p50={metrics['p50_ms']}ms, p95={p95}ms, p99={metrics['p99_ms']}ms",
        f"[METRIC] error_rate={error_rate}%, throughput={metrics['throughput_rps']} rps",
        f"[METRIC] total_requests={metrics['total_requests']}, vus_peak={metrics['vus_peak']}",
        f"[THRESHOLD] p(95) < 1500ms {'✓' if threshold_p95 else '— FALHOU'} (atual: {p95}ms)",
        f"[THRESHOLD] error rate < 1% {'✓' if threshold_error else '— FALHOU'} (atual: {error_rate}%)",
        f"[VALIDATE] status == 200 {'✓' if threshold_status else '— FALHOU'} (atual: {base_status})",
        f"[VALIDATE] 100 posts retornados {'✓' if threshold_count else '— FALHOU'} (atual: {base_count})"
    ]

    output = {
        "executor": "k6",
        "environment": BASE_URL,
        "generated_files": [{"path": "tmp_perf_20260508_114735/script.py", "content": ""}],
        "results": [
            {
                "id": "TC-PERF-001",
                "title": "GET /posts responde dentro do SLA",
                "status": "passed" if overall_pass else "failed",
                "type": "performance",
                "metrics": {
                    "p50_ms": metrics['p50_ms'],
                    "p95_ms": metrics['p95_ms'],
                    "p99_ms": metrics['p99_ms'],
                    "min_ms": metrics['min_ms'],
                    "max_ms": metrics['max_ms'],
                    "error_rate_pct": metrics['error_rate_pct'],
                    "throughput_rps": metrics['throughput_rps'],
                    "vus_peak": metrics['vus_peak'],
                    "duration_s": metrics['duration_s']
                },
                "thresholds": thresholds,
                "logs": logs,
                "error": None if overall_pass else f"Threshold(s) falharam: {', '.join([t['check'] for t in thresholds if t['result']=='failed'])}"
            }
        ],
        "summary": {
            "total": 1,
            "passed": 1 if overall_pass else 0,
            "failed": 0 if overall_pass else 1,
            "mode": "fallback_python"
        }
    }
else:
    output = {
        "executor": "k6",
        "environment": BASE_URL,
        "results": [
            {
                "id": "TC-PERF-001",
                "title": "GET /posts responde dentro do SLA",
                "status": "error",
                "type": "performance",
                "metrics": {},
                "thresholds": [],
                "logs": ["[ERROR] Nenhum resultado coletado — possível erro de conexão"],
                "error": "Nenhum resultado coletado"
            }
        ],
        "summary": {"total": 1, "passed": 0, "failed": 1, "mode": "fallback_python"}
    }

print(json.dumps(output, ensure_ascii=False, indent=2))
