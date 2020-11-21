import { apiInstance } from 'apis';
import { stringify } from 'querystring';

export const searchProducts = 
  async (keyword, productImageName) => await apiInstance.get(`/search?${stringify({
    q: keyword,
    product_image: productImageName,
  })}`)

export const getSuggestions = 
  async (keyword) => await apiInstance.get(`/search/suggestions`)

export const uploadProductImage =
  async (data) => await apiInstance.post(`/search/upload_image`, data)