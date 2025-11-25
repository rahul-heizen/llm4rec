import axios from "axios";

const api = axios.create({
  baseURL: "https://llm4rec-api.vercel.app",
  timeout: 5000,
});

export default api;
