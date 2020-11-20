import React, { useState } from 'react';
import {
  Input,
} from 'antd';

export const ProductSearch = () => {
  const [ searchInput, setSearchInput ] = useState('');
  const [ searchResults, setSearchResults ] = useState([]);
  const onSearch = (value) => {
    
  };
  return (
    <>
      <Input.Search
        allowClear
        addonBefore="keywords:"
        placeholder="cake, bookmark, smartphone..."
        value={searchInput}
        onChange={setSearchInput}
      />
    </>
  )
}