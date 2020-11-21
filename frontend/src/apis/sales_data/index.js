import { apiInstance } from 'apis';
import { stringify } from 'querystring';

export const uploadSalesData =
  async (data) => await apiInstance.post(`/sales-data/upload`, data)