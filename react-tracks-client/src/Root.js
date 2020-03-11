import React from "react";
import withRoot from "./withRoot";
import {Query} from 'react-apollo' // query component from react-apollo for easy querying and mutation
import {gql} from 'apollo-boost' // import query parser

const Root = () => (
  <Query query={GET_TRACK_QUERY}>
    {({data, loading, error}) => {
      if (loading) return <div>Loading...</div>
      if (error) return <div>There is an error</div>
      return <div>{JSON.stringify(data)}</div>
    }} // use a render prop
  </Query>
)

const GET_TRACK_QUERY = gql`
  {
    tracks{
      id
      title
      description
      url
    }
  }
`

export default withRoot(Root);
