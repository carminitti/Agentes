
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  vus: 15,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.05'],
  },
};
export default function () {
  const res = http.get('https://jsonplaceholder.typicode.com/todos');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
