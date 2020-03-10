import React from "react";
import ReactDOM from "react-dom";
import Root from "./Root";
import * as serviceWorker from "./serviceWorker";
import {ApolloProvider} from 'react-apollo' // to inject apollo into all components with the help of React Context
import ApolloClient from 'apollo-boost'

// create apollo client
const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql/'
})

// wrap Root component inside ApolloClient and pass client into client prop
ReactDOM.render(
  <ApolloClient client={client}>
    <Root />
  </ApolloClient>,
  document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
