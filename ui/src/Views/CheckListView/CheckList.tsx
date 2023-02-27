
import { Table } from '@mui/material';
import * as React from 'react';
import checkService from '../../check.service.tsx';

import PageLayout from '../PageLayout/PageLayout.tsx';

type Check = {
  name: string;
  environment: string;
}

class CheckList extends React.Component {

  constructor(props) {
    super(props);
    this.retrieveChecks = this.retrieveChecks.bind(this);

    this.state = {
      checks: [],
    };
  }

  componentDidMount() {
    this.retrieveChecks();
  }

  retrieveChecks() {
    checkService.getAll().then((res) => {
      let checks = res.data;
      this.setState((state) => {
        let newState = Object.assign(state);
        newState.checks = checks;
        return newState;
      });
    })
  }

  render() {
    return (
        <PageLayout>
            <Table>
              <tr>
                <th>Name</th>
                <th>Environment</th>
              </tr>
              {
                this.state.checks.map((value) => {
                  return (<tr><td>{value.name}</td><td>{value.environment}</td></tr>)
                })
              }
            </Table>
        </PageLayout>
    );
  }
}

export default CheckList;
