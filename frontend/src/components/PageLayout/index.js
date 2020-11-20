import React, { useState } from 'react';
import { 
  Layout,
  Menu,
} from 'antd';
import {
  PlusOutlined,
  UnorderedListOutlined,
} from '@ant-design/icons';
import {
  Link
} from 'react-router-dom';

export const PageLayout = ({
  children,
}) => {
  const [ collapsed, setCollapsed ] = useState(false);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Layout.Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ color: "#fff", padding: collapsed ? '10px 34px' : '10px 22px' }}>
          <h1 style={{ color: "#fff", fontWeight: 600, fontSize: 18 }}>
            {collapsed ? 't' : 'tobtob'}
          </h1>
        </div>
        <Menu theme="dark" mode="inline">
          <Menu.Item icon={<UnorderedListOutlined />} key="1">
            <Link to="/">My Products</Link>
          </Menu.Item>
          <Menu.Item icon={<PlusOutlined />} key="2">
            <Link to="/search">Add New Product</Link>
          </Menu.Item>
        </Menu>
      </Layout.Sider>
      <Layout style={{ padding: '24px 0' }}>
        <Layout.Content style={{ margin: '0 16px', minHeight: 280 }}>
          {children}
        </Layout.Content>
      </Layout>
    </Layout>
  )
}