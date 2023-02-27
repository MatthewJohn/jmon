import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:5000/api/v1",
  headers: {
    "Content-type": "application/json"
  }
});

class CheckService {
  getAll() {
    return client.get("/checks");
  }

  get(name) {
    return client.get(`/checks/${name}`);
  }
}

export default new CheckService();
