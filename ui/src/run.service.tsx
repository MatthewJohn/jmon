import client from './client.tsx';


class CheckService {

  getByCheck(name, environment) {
    return client.get(`/checks/${name}/environments/${environment}/runs`);
  }
}

export default CheckService;
