import { apiInstance } from 'apis';
import { stringify } from 'querystring';

export const getRecommendedFeatures = 
  async (keyword) => await apiInstance.get(`/product-features/?${stringify({
    q: keyword,
  })}`)
