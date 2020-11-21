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
import { getHolidays } from 'apis/misc_data'
import { getSuggestions, searchProducts } from 'apis/search'
import amazonIcon from 'assets/amazon_favicon.ico'
import shopeeIcon from 'assets/shopee_favicon.ico'

const siteIcons = {
  'amazon': amazonIcon,
  'shopee': shopeeIcon,
}

export const ProductSearch = () => {
  const [ searchInput, setSearchInput ] = useState('');
  const [ marginalCost, setMarginalCost ] = useState(0);
  const [ affectedBy, setAffectedBy ] = useState(null);
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
  const handleSearch = async (option) => {
    const resp = await searchProducts(option);
    setSearchResults(resp.data);
  };
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
            onSelect={handleSearch}
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
          <Upload>
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
          </Upload>

          <div style={{ height: 20 }} />
          <Typography.Text style={{ marginRight: 20 }}>Product likely affected by</Typography.Text>
          <Select mode="multiple" style={{ width: 240 }} onChange={setAffectedBy}>
            {holidays && holidays.map(item => 
              <Select.Option key={item.id} value={item.id}>
                {item.name}
              </Select.Option>)}
          </Select>

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
          />
        </div>
        <div style={{ height: 20 }} />
        <div>
          <Typography.Text style={{ marginRight: 20 }}>Past sales data</Typography.Text>
          <Upload>
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