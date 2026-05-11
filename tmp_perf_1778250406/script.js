import http from 'k6/http';
import { check, sleep } from 'k6';

// TC-CL-005: Carga — home page com 10 VUs, p95 < 3000ms
export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<3000'],
    http_req_failed: ['rate<0.05'],
  },
};

export default function () {
  const res = http.get('https://automationexercise.com/');
  check(res, {
    'status 200': (r) => r.status === 200,
    'body nao vazio': (r) => r.body !== null && r.body.length > 0,
  });
  sleep(1);
}
