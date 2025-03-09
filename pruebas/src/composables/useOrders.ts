import { useQuery } from "@tanstack/vue-query";
import { fetchOrders } from "../services/api";

export const useOrders = () => {
  return useQuery({
    queryKey: ["orders"],
    queryFn: fetchOrders,
  });
};
