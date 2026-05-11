import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '20s',
  thresholds: {
    http_req_duration: ['p(95)<3000'],
    http_req_failed: ['rate<0.05'],
  },
};

export default function () {
  const res = http.get('https://swapi.dev/api/people/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
