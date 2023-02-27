
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import * as React from 'react';
import checkService from '../../check.service.tsx';

import PageLayout from '../PageLayout/PageLayout.tsx';


const columns: GridColDef[] = [
  { field: 'environment', headerName: 'Environment', width: 200 },
  { field: 'name', headerName: 'Name', width: 400 },
  { field: 'average_success', headerName: 'Average Success', valueGetter: (data) => {return (data.row.average_success >= 0.99 ? '100' : (data.row.average_success * 100).toPrecision(2)) + '%';} },
  { field: 'latest_status', headerName: 'Latest Status', valueGetter: (data) => {return data.row.latest_status === true ? 'Success' : data.row.latest_status === false ? 'Failed' : 'Not run'} }
];

class CheckList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      checks: []
    };
    this.retrieveChecks = this.retrieveChecks.bind(this);
  }

  componentDidMount() {
    this.retrieveChecks();
  }

  retrieveChecks() {
    checkService.getAll().then((checksRes) => {
      let checks = checksRes.data;
      let checkData = [];
      checks.forEach((check) => {
        checkService.getResultsByCheckNameAndEnvironment(check.name, check.environment).then((statusRes) => {
          checkData.push({
            name: check.name,
            environment: check.environment,
            average_success: statusRes.data.average_success,
            latest_status: statusRes.data.latest_status
          });
        }).then(() => {
          this.setState({checks: checkData});
        });
      })
    })
  }

  onRowClick(val: any) {
    console.log(val)
  }

  render() {
    return (
        <PageLayout>
          <Container  maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={8} lg={8}>
                <div style={{ height: 400, width: '100%' }}>
                  <DataGrid
                    rows={this.state.checks}
                    columns={columns}
                    //pageSize={5}
                    //rowsPerPageOptions={[5]}
                    getRowId={(row: any) =>  row.name + row.environment}
                    onRowClick={this.onRowClick}
                    //checkboxSelection
                  />
                </div>
              </Grid>
            </Grid>
          </Container>
        </PageLayout>
    );
  }
}

export default CheckList;
