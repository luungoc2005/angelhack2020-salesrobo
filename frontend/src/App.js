import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import { PageLayout } from 'components/PageLayout';
import { HomePage } from 'pages/HomePage';
import { ProductSearch } from 'pages/ProductSearch';
import { ProductPage } from 'pages/ProductPage';

import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <PageLayout>
          <Switch>
            <Route exact path="/">
              <HomePage />
            </Route>
            <Route exact path="/search">
              <ProductSearch />
            </Route>
            <Route exact path="/products/:id">
              <ProductPage />
            </Route>
          </Switch>
        </PageLayout>
      </Router>
    </div>
  );
}

export default App;
