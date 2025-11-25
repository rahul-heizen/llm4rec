import api from "./axios";

/**
 * Fetches the food catalog from the backend API.
 * @returns {Promise<Array>} Array of food items.
 */
export const getCatalog = async () => {
  const response = await api.get("/catalog");
  return response.data;
};
