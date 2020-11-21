import { apiInstance } from 'apis';

export const getForecastPlot =
  async (id) => await apiInstance.get(`/forecast/${id}`)
