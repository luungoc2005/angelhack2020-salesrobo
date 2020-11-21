import React, { useState, useEffect } from 'react';
import {
  PageHeader,
  Layout,
  Typography,
} from 'antd';
import {
  useParams,
} from 'react-router-dom';

export const ProductPage = () => {
  const { id: productId } = useParams();

  return <>
    <PageHeader
      title="Product information"
    >
      <Layout.Content>
        Keyword: smartphone
      </Layout.Content>
    </PageHeader>
    <PageHeader
      title="Recommendations"
    >
      <Layout.Content>
        <Typography.Title level={5}>Price:</Typography.Title>
        <Typography.Text>

        </Typography.Text>
        <Typography.Title level={5}>Forecast</Typography.Title>
        <Typography.Paragraph>
          
        </Typography.Paragraph>
        <Typography.Title level={5}>Recommended Features</Typography.Title>
        <Typography.Paragraph>
          
        </Typography.Paragraph>
      </Layout.Content>
    </PageHeader>
    <PageHeader
      title="Additional data"
    >

    </PageHeader>
  </>
}