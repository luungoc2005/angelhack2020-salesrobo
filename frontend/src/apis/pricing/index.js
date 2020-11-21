import { apiInstance } from 'apis';

export const getOptimalPricing =
  async (id) => await apiInstance.get(`/pricing/optimal_pricing/${id}`)
