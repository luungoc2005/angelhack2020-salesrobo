import { apiInstance } from 'apis';

export const getHolidays = 
  async () => await apiInstance.get(`/misc-data/holidays`)
