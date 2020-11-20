import React, { useState } from 'react';
import {
  PageHeader,
  Layout,
  Input,
  Typography,
  Upload,
  Button,
  InputNumber,
} from 'antd';
import {
  UploadOutlined,
} from '@ant-design/icons';

export const ProductSearch = () => {
  const [ searchInput, setSearchInput ] = useState('');
  const [ marginalCost, setMarginalCost ] = useState(0);
  const [ searchResults, setSearchResults ] = useState([]);
  const onSearch = (value) => {
    
  };
  return (
    <>
      <PageHeader
        title="Product information"
        subTitle="Add relevant product information"
      >
        <Layout.Content>
          <Typography.Text>Keywords</Typography.Text>
          <Input.Search
            allowClear
            placeholder="cake, bookmark, smartphone..."
            value={searchInput}
            onChange={setSearchInput}
          />
          <div style={{ height: 20 }} />

          <Typography.Text style={{ marginRight: 20 }}>Product image</Typography.Text>
          <Upload>
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
          </Upload>
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