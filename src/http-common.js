import axios from "axios";

export default axios.create({
  baseURL: "http://91.236.1.204:8080/api",
  headers: {
    "Content-type": "application/json",
    "Access-Control-Allow-Origin": "*",
  },
});
