import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 6,
  duration: '25s',
  insecureSkipTLSVerify: true,
  thresholds: {
    http_req_duration: ['p(95)<2500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://dog.ceo/api/breeds/image/random');
  check(res, {
    'status 200': (r) => r.status === 200,
    'message success': (r) => {
      try { return JSON.parse(r.body).status === 'success'; } catch { return false; }
    },
    'has image url': (r) => {
      try { return typeof JSON.parse(r.body).message === 'string'; } catch { return false; }
    },
  });
  sleep(1);
}
