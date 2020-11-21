import { apiInstance } from 'apis';
import { stringify } from 'querystring';

export const searchProducts = 
  async (keyword, productImageName, priceFrom, priceTo) => await apiInstance.get(`/search?${stringify({
    q: keyword,
    product_image: productImageName,
    price_from: priceFrom,
    price_to: priceTo,
  })}`)

export const searchReviews = 
  async (keyword) => await apiInstance.get(`/search/reviews?${stringify({
    q: keyword,
  })}`)

export const getSuggestions = 
  async (keyword) => await apiInstance.get(`/search/suggestions`)

export const uploadProductImage =
  async (data) => await apiInstance.post(`/search/upload-image`, data)