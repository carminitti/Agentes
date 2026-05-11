import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 8,
  duration: '25s',
  insecureSkipTLSVerify: true,
  thresholds: {
    http_req_failed: ['rate<0.02'],
    http_req_duration: ['p(95)<3000'],
  },
};

export default function () {
  const res = http.get('https://api.adviceslip.com/advice', {
    headers: { 'Cache-Control': 'no-cache' },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'slip.advice nao vazio': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body && body.slip && typeof body.slip.advice === 'string' && body.slip.advice.length > 0;
      } catch { return false; }
    },
  });

  sleep(0.5);
}
