import { apiInstance } from 'apis';

export const getProducts = 
  async () => await apiInstance.get(`/products/`)

export const getProductById =
  async (id) => await apiInstance.get(`/products/${id}`)

export const putProduct = 
  async (data) => await apiInstance.put(`/products/`, data)

export const postProduct = 
  async (id, data) => await apiInstance.post(`/products/${id}`, data)

export const patchProduct = 
  async (id, data) => await apiInstance.patch(`/products/${id}`, data)