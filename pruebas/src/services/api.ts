import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const fetchOrders = async () => {
  try {
    const response = await axios.get(`${API_URL}/orders`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener órdenes:", error);
    throw error;
  }
};
