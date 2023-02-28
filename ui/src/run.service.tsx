import client from './client.tsx';


class CheckService {

  listByCheck(name, environment) {
    return client.get(`/checks/${name}/environments/${environment}/runs`);
  }

  getById(name, environment, runTimestamp) {
    return client.get(`/checks/${name}/environments/${environment}/runs/${runTimestamp}`);
  }

  getLogById(name, environment, runTimestamp) {
    return client.get(`/checks/${name}/environments/${environment}/runs/${runTimestamp}/artifacts/artifact.log`);
  }
}

export default CheckService;
