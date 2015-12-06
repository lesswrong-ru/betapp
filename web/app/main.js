import React from 'react';
import ReactDOM from 'react-dom';

import {Provider} from 'react-redux';
import {createStore} from 'redux';

import betApp from './reducers';
import Page from './containers/Page';

let store = createStore(betApp);

let rootElement = document.body.getElementsByTagName("main")[0];
ReactDOM.render(
  <Provider store={store}>
    <Page/>
  </Provider>,
  rootElement
);
