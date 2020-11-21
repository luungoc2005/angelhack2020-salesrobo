import React, { useState, useEffect } from 'react';
import {
  PageHeader,
  Layout,
  Typography,
  Avatar,
  Image,
  List,
  InputNumber,
} from 'antd';
import {
  useParams,
} from 'react-router-dom';
import Plot from 'react-plotly.js';

import { BASE_URL } from 'apis';
import { searchProducts, searchReviews } from 'apis/search';
import { getProductById } from 'apis/products';
import { updateUnitsSold } from 'apis/sales_data';
import { getOptimalPricing } from 'apis/pricing';
import { getForecastPlot } from 'apis/forecast';

import amazonIcon from 'assets/amazon_favicon.ico';
import shopeeIcon from 'assets/shopee_favicon.ico';

const siteIcons = {
  'amazon': amazonIcon,
  'shopee': shopeeIcon,
}

export const ProductPage = () => {
  const { id: productId } = useParams();
  const [ productData, setProductData ] = useState({});
  const [ pricingData, setPricingData ] = useState({});
  const [ forecastPlot, setForecastPlot ] = useState([]);

  const [ searchResults, setSearchResults ] = useState([]);
  const [ reviewResults, setReviewResults ] = useState([]);
  
  const fetchProductData = async () => {
    const resp = await getProductById(productId);
    setProductData(resp.data);

    const searchResp = await searchProducts(
      resp.data.keyword,
      resp.data.product_image,
      resp.data.price_from,
      resp.data.price_to
    )
    setSearchResults(searchResp.data);

    const reviewsResp = await searchReviews(
      resp.data.keyword,
    )
    setReviewResults(reviewsResp.data);
  }

  const fetchPricingData = async () => {
    try {
      const resp = await getOptimalPricing(productId);
      setPricingData(resp.data);
    }
    catch {
      setPricingData(null);
    }
  }

  const fetchForecastPlot = async () => {
    try {
      const resp = await getForecastPlot(productId);
      setForecastPlot(resp.data);
    }
    catch {
      setForecastPlot(null);
    }
  }

  useEffect(() => {
    fetchProductData();
    fetchPricingData();
    fetchForecastPlot();
  }, [productId, setProductData, setPricingData, setSearchResults, setReviewResults])

  const handleUnitsSoldChange = async (value) => {
    try {
      await updateUnitsSold(productId, {
        units_sold: value,
      });
      fetchForecastPlot();
    }
    catch {}
  }

  return <>
    <PageHeader
      title="Product information"
    >
      <Layout.Content>
        <div style={{ width: '100%', padding: '24px 0' }}>
          <Image 
            alt="Product Image"
            src={`${BASE_URL}/uploads/${productData.product_image}`}
            style={{
              maxWidth: 128,
              maxHeight: 128,
            }}
          />
        </div>
        
        <Typography.Paragraph>
          Keyword: {productData ? productData.keyword : 'N/A'}
        </Typography.Paragraph>
        
        <Typography.Paragraph>
          Price range: {productData.price_from ? `$ ${productData.price_from}` : '?'} - {productData.price_to ? `$ ${productData.price_to}` : '?'}
        </Typography.Paragraph>

        <Typography.Paragraph>
          Marginal cost: {productData.marginal_cost ? `$ ${productData.marginal_cost}` : '?'}
        </Typography.Paragraph>

        <Typography.Paragraph>
          Units sold today: <InputNumber 
            defaultValue={0}
            onChange={handleUnitsSoldChange}
          />
        </Typography.Paragraph>
      </Layout.Content>
    </PageHeader>
    <PageHeader
      title="Recommendations"
    >
      <Layout.Content>
        {pricingData && <>
          <Typography.Title level={5}>Profit-maximizing price:</Typography.Title>
          <Typography.Paragraph>
            <Typography.Text style={{ fontSize: 'large' }}>{`$ ${Math.round(pricingData.optimal_price * 100) / 100}`}</Typography.Text>
          </Typography.Paragraph>
          <Typography.Paragraph>
            <Typography.Text>Elasticity = {`${Math.round(pricingData.elasticity * 100) / 100}`}</Typography.Text>
            <Typography.Text> - </Typography.Text>
            <Typography.Text>Regression R<sup>2</sup> = {`${Math.round(pricingData.r2 * 100) / 100}`}</Typography.Text>
          </Typography.Paragraph>
        </>}

        {forecastPlot && <>
          <Typography.Title level={5}>Sales Forecast</Typography.Title>
          <Typography.Paragraph>
            <Plot
              data={forecastPlot}
              layout={{
                autosize: true, 
                title: '5-day sales forecast',
              }}
              style={{ width: '80%', height: '50%' }}
            />
          </Typography.Paragraph>
        </>}

        <Typography.Title level={5}>Recommended Features</Typography.Title>
        <Typography.Paragraph>
          
        </Typography.Paragraph>
      </Layout.Content>
    </PageHeader>

    <PageHeader
      title="Reference data"
    >
      <List
        header={<div>Relevant products</div>}
        itemLayout="horizontal"
        bordered
        style={{ maxHeight: 320, overflowY: 'scroll' }}
        dataSource={searchResults}
        rowKey={item => item.id}
        renderItem={(item) =>
          <List.Item>
            <List.Item.Meta
              avatar={<Avatar src={item.image} />}
              title={<>
                {item.name}
                <img src={siteIcons[item.from]} style={{ maxWidth: 16, maxHeight: 16, marginLeft: 12 }} />
              </>}
              description={item.price ? `$ ${item.price}` : ''}
            />
          </List.Item>
        }
      />
      <div style={{ height: 20 }} />
      <List
        header={<div>User reviews</div>}
        itemLayout="horizontal"
        bordered
        style={{ maxHeight: 320, overflowY: 'scroll' }}
        dataSource={reviewResults}
        rowKey={item => item.id}
        renderItem={(item) =>
          <List.Item>
            <List.Item.Meta
              avatar={<Avatar src={siteIcons[item.from]} />}
              description={item.text}
            />
          </List.Item>
        }
      />
    </PageHeader>
  </>
}