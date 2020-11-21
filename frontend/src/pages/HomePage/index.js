import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  List,
  Layout,
  Typography,
  Avatar,
  Card,
} from 'antd';
import {
  getProducts,
} from 'apis/products'
import {
  BASE_URL,
} from 'apis'

export const HomePage = () => {
  const [ products, setProducts ] = useState([]);
  const history = useHistory();

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getProducts();
      setProducts(resp.data);
    }
    fetchData();
  }, []);
  const handleNavigate = (id) => {
    history.push(`/products/${id}`)
  }

  return (
    <>
      <List
        header={<div>My products</div>}
        bordered
        dataSource={products}
        rowKey={item => item.id}
        itemLayout="horizontal"
        style={{ padding: 12 }}
        renderItem={item =>
          <Card
            hoverable
            style={{ width: 240 }}
            cover={<div style={{ textAlign: 'center', paddingTop: 24 }}>
              <img 
                alt="Product Image"
                src={`${BASE_URL}/uploads/${item.product_image}`}
                style={{
                  maxWidth: 64,
                  maxHeight: 64,
                }} 
              />
            </div>}
            onClick={() => handleNavigate(item.id)}
          >
            <Card.Meta
              title={item.keyword}
              description={item.marginal_cost ? `$ ${item.marginal_cost}` : ''}
            />
          </Card>
        }
      />
    </>
  )
}