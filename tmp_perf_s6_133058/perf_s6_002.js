import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '20s',
  insecureSkipTLSVerify: true,
  thresholds: {
    http_req_failed: ['rate<0.02'],
    http_req_duration: ['p(95)<3500'],
  },
};

export default function () {
  const res = http.get('https://opentdb.com/api.php?amount=5&type=boolean');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response_code is 0': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body && body.response_code === 0;
      } catch { return false; }
    },
  });

  sleep(1);
}
