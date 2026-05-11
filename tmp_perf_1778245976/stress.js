import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 20 },
    { duration: '15s', target: 50 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'],
    http_req_failed: ['rate<0.10'],
  },
};

export default function () {
  const res = http.get('https://swapi.dev/api/starships/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(0.5);
}
