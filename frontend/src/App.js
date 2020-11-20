import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import { HomePage } from 'pages/HomePage';
import { ProductSearch } from 'pages/ProductSearch';

import { Button } from 'antd';
import './App.css';

function App() {
  return (
    <div className="App">
      <Button type="primary">Button</Button>
      <Router>
        <Switch>
          <Route path="/">
            <HomePage />
          </Route>
          <Route path="/search">
            <ProductSearch />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
