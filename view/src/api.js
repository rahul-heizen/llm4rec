import api from "./axios";

/**
 * Fetches the food catalog from the backend API.
 * @returns {Promise<Array>} Array of food items.
 */
export const getCatalog = async () => {
  const response = await api.get("/catalog");
  return response.data;
};

/**
 * Gets recommended food items based on user background.
 * @param {string} userBackground - User's background info.
 * @returns {Promise<Array>} Array of recommended food items.
 */
export const getRecommendations = async (userBackground) => {
  const response = await api.post("/recommend", {
    user_background: userBackground,
  });
  return response.data;
};
