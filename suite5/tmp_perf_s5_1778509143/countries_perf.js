import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '20s',
  insecureSkipTLSVerify: true,
  thresholds: {
    http_req_duration: ['p(95)<4000'],
    http_req_failed: ['rate<0.02'],
  },
};

export default function () {
  const res = http.get('https://restcountries.com/v3.1/all?fields=name,capital,population');
  check(res, {
    'status 200': (r) => r.status === 200,
    'is array': (r) => {
      try { return Array.isArray(JSON.parse(r.body)); } catch { return false; }
    },
  });
  sleep(1);
}
