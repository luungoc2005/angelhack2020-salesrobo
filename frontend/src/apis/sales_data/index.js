import { apiInstance } from 'apis';
import { stringify } from 'querystring';

export const uploadSalesData =
  async (data) => await apiInstance.post(`/sales-data/upload`, data)

export const updateUnitsSold =
  async (id, data) => await apiInstance.patch(`/sales-data/${id}`, data)