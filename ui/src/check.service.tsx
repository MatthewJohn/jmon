import client from './client.tsx';

class CheckService {
  getAll() {
    return client.get("/checks");
  }

  get(name) {
    return client.get(`/checks/${name}`);
  }

  getResultsByCheckNameAndEnvironment(name, environment) {
    return client.get(`/checks/${name}/environments/${environment}/results`);
  }
}

export default new CheckService();
