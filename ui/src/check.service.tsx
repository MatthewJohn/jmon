import client from './client.tsx';

class CheckService {
  getAll() {
    return client.get("/checks");
  }

  getByNameAndEnvironment(name, environment) {
    return client.get(`/checks/${name}/environments/${environment}`);
  }

  getResultsByCheckNameAndEnvironment(name, environment) {
    return client.get(`/checks/${name}/environments/${environment}/results`);
  }
}

export default CheckService;
