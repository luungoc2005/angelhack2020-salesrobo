import React, { useEffect, useState } from 'react';
import {
  PageHeader,
  Layout,
  Input,
  Typography,
  Upload,
  Button,
  InputNumber,
  Select,
  List,
  AutoComplete,
  Avatar,
} from 'antd';
import {
  UploadOutlined,
} from '@ant-design/icons';

import { getHolidays } from 'apis/misc_data';
import { uploadSalesData } from 'apis/sales_data';
import { getSuggestions, searchProducts, uploadProductImage } from 'apis/search'

import amazonIcon from 'assets/amazon_favicon.ico';
import shopeeIcon from 'assets/shopee_favicon.ico';

const siteIcons = {
  'amazon': amazonIcon,
  'shopee': shopeeIcon,
}

export const ProductSearch = () => {
  const [ searchInput, setSearchInput ] = useState('');
  const [ productImageFile, setProductImageFile ] = useState('');
  const [ affectedBy, setAffectedBy ] = useState(null);
  const [ priceFrom, setPriceFrom ] = useState(0);
  const [ priceTo, setPriceTo ] = useState(0);

  const [ marginalCost, setMarginalCost ] = useState(0);
  const [ salesDataFile, setSalesDataFile ] = useState('');
  
  const [ searchResults, setSearchResults ] = useState([]);
  const [ searchSuggestions, setSearchSuggestions ] = useState([]);
  const [ holidays, setHolidays ] = useState([]);
  
  useEffect(() => {
    const fetchHolidays = async () => {
      const resp = await getHolidays();
      setHolidays(resp.data);
    }
    const fetchSearchSuggestions = async () => {
      const resp = await getSuggestions();
      setSearchSuggestions(resp.data.map(item => ({ value: item, label: item })));
    }
    fetchHolidays();
    fetchSearchSuggestions();
  }, [])
  const handleSearch = async (
    keyword, argProductImage, argPriceFrom, argPriceTo
  ) => {
    const resp = await searchProducts(
      keyword || searchInput, 
      argProductImage || productImageFile, 
      argPriceFrom || priceFrom, 
      argPriceTo || priceTo,
    );
    setSearchResults(resp.data);
    setMarginalCost(
      Math.max(...resp.data.map(item => item.price ? item.price : 0))
    )
  };
  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file)
    const resp = await uploadProductImage(formData);
    setProductImageFile(resp.data.name);
    await handleSearch(searchInput, resp.data.name, priceFrom, priceTo);
  }
  useEffect(() => {
    handleSearch(null, null, priceFrom, priceTo);
  }, [priceFrom, priceTo])

  const handleUploadSalesData = async (file) => {
    const formData = new FormData();
    formData.append('file', file)
    const resp = await uploadSalesData(formData);
    setSalesDataFile(resp.data.name);
  }

  return (
    <>
      <PageHeader
        title="Product information"
        subTitle="Add relevant product information"
      >
        <Layout.Content>
          <Typography.Text style={{ display: 'block' }}>Keywords</Typography.Text>
          <AutoComplete
            options={searchSuggestions}
            value={searchInput}
            onChange={setSearchInput}
            onSelect={(value) => handleSearch(value, productImageFile)}
            style={{ width: '100%', marginTop: 4 }}
          >
            <Input.Search
              size="large" 
              placeholder="cake, bookmark, smartphone..." 
              enterButton
              allowClear
            />
          </AutoComplete>
          <div style={{ height: 20 }} />

          <Typography.Text style={{ marginRight: 20 }}>Product image</Typography.Text>
          <Upload
            action={handleUpload}
            multiple={false}
            listType="picture"
          >
            <Button 
              icon={<UploadOutlined />}
            >
              Click to Upload
            </Button>
          </Upload>

          <div style={{ height: 20 }} />
          <div>
            <Typography.Text style={{ marginRight: 20 }}>Price</Typography.Text>
            <InputNumber
              defaultValue={0}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value.replace(/\$\s?|(,*)/g, '')}
              onChange={setPriceFrom}
              value={priceFrom}
            />
            <Typography.Text style={{ marginRight: 10, marginLeft: 10 }}>-</Typography.Text>
            <InputNumber
              defaultValue={0}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value.replace(/\$\s?|(,*)/g, '')}
              onChange={setPriceTo}
              value={priceTo}
            />
          </div>

          <div style={{ height: 20 }} />
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
          <Typography.Text style={{ marginRight: 20 }}>Product likely affected by</Typography.Text>
          <Select mode="multiple" style={{ width: 240 }} onChange={setAffectedBy}>
            {holidays && holidays.map(item => 
              <Select.Option key={item.id} value={item.id}>
                {item.name}
              </Select.Option>)}
          </Select>
        </Layout.Content>
      </PageHeader>

      <PageHeader
        title="Sales data"
        subTitle="Your sales data until this point"
      >
        <div>
          <Typography.Text style={{ marginRight: 20 }}>Marginal cost per unit</Typography.Text>
          <InputNumber
            defaultValue={0}
            formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
            parser={value => value.replace(/\$\s?|(,*)/g, '')}
            onChange={setMarginalCost}
            value={marginalCost}
          />
        </div>
        <div style={{ height: 20 }} />
        <div>
          <Typography.Text style={{ marginRight: 20 }}>Past sales data</Typography.Text>
          <Upload
            action={handleUploadSalesData}
            multiple={false}
          >
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
          </Upload>
        </div>
      </PageHeader>

      <Button
        block 
        type="primary"
        size="large"
      >
        Finish
      </Button>
    </>
  )
}