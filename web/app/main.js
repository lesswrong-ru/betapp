import React from 'react';
import ReactDOM from 'react-dom';

import {Provider} from 'react-redux';
import {createStore, applyMiddleware} from 'redux';
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger';

import betApp from './reducers/index';
import Page from './containers/Page';

const loggerMiddleware = createLogger();

const createStoreWithMiddleware = applyMiddleware(
  thunkMiddleware,
  loggerMiddleware
)(createStore);
let store = createStoreWithMiddleware(betApp);

let rootElement = document.body.getElementsByTagName("main")[0];
ReactDOM.render(
  <Provider store={store}>
    <Page/>
  </Provider>,
  rootElement
);
