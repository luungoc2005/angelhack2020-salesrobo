import React from 'react';
import { PageHeader } from 'antd';

export const PageHeader = ({ 
  title,
  onBack=undefined,
}) => {
  return (
    <PageHeader
      title="tobtob"
      subTitle={title}
      onBack={onBack}
    />
  )
}