import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 15 },
    { duration: '20s', target: 15 },
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'],
    http_req_failed: ['rate<0.05'],
  },
};

export default function () {
  const res = http.get('https://swapi.dev/api/planets/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
