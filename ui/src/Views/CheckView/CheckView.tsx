
import { Typography } from '@mui/material';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import * as React from 'react';
import runService from '../../run.service.tsx';
import { withRouter } from '../../withRouter';


const columns: GridColDef[] = [
  {
    field: 'timestamp',
    headerName: 'timestamp',
    width: 200
  },
  {
    field: 'result',
    headerName: 'result',
    width: 400,
    valueGetter: (data) => {
      return data.row.result === true ? 'Success' : data.row.result === false ? 'Failed' : 'Running'}
    }
];

class CheckView extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      runs: []
    };
    this.retrieveRuns = this.retrieveRuns.bind(this);
  }

  componentDidMount() {
    this.retrieveRuns();
  }

  retrieveRuns() {
    runService.getByCheck(this.props.match.checkName, this.props.match.environmentName).then((runRes) => {
      this.setState({
        runs: Object.keys(runRes.data).map((key) => {return {timestamp: key, result: runRes.data[key]}})
      });
      console.log(Object.keys(runRes.data).map((key) => {return {timestamp: key, result: runRes.data[key]}}));
    });
  }

  onRowClick(val: any) {
    console.log(val)
  }

  render() {
    console.log("rendering");
    return (
      <Container  maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Typography>
          {this.props.match.checkName} - {this.props.match.environmentName}
        </Typography>
        <Grid container spacing={3}>
          <Grid
            item
            xs={12} md={12} lg={10} xl={8}
            sx={{
              '& .check-result-row--success': {
                bgcolor: '#ccffcc'
              },
              '& .check-result-row--failed': {
                bgcolor: '#ffcccc'
              }
            }}
          >
            <div style={{ height: 400, width: '100%' }}>
              <DataGrid
                rows={this.state.runs}
                columns={columns}
                pageSize={100}
                rowsPerPageOptions={[5]}
                getRowId={(row: any) =>  row.timestamp}
                onRowClick={this.onRowClick}
                initialState={{
                  sorting: {
                    sortModel: [{ field: 'timestamp', sort: 'desc' }],
                  },
                }}
                getRowClassName={(params) => `check-result-row--${params.row.result === true ? 'success' : params.row.result === false ? 'failed' : 'running'}`}
              />
            </div>
          </Grid>
        </Grid>
      </Container>
    );
  }
}

export default withRouter(CheckView);
