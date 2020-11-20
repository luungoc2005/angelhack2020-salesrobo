import React, { useState, useEffect } from 'react';
import {
  List,
} from 'antd';

export const HomePage = () => {
  const [ products, setProducts ] = useState([]);
  useEffect(() => {

  }, []);
  return (
    <>
      <List
        header={<div>My products</div>}
        bordered
        dataSource={products}
        rowKey={item => item.id}
        renderItem={item =>
          <List.Item>
            
          </List.Item>
        }
      />
    </>
  )
}