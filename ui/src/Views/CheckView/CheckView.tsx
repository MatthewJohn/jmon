
import { Paper, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Table from '@mui/material/Table';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import * as React from 'react';
import runService from '../../run.service.tsx';
import checkService from '../../check.service.tsx';
import { withRouter } from '../../withRouter';


const columns: GridColDef[] = [
  {
    field: 'timestamp',
    headerName: 'Timestamp',
    width: 200
  },
  {
    field: 'result',
    headerName: 'Result',
    width: 400,
    valueGetter: (data) => {
      return data.row.result === true ? 'Success' : data.row.result === false ? 'Failed' : 'Running'}
    }
];

class CheckView extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      runs: [],
      detailsRows: []
    };
    this.retrieveRuns = this.retrieveRuns.bind(this);
    this.getRunDetails = this.getRunDetails.bind(this);
    this.onRowClick = this.onRowClick.bind(this);
  }

  componentDidMount() {
    this.retrieveRuns();
    this.getRunDetails();
  }

  retrieveRuns() {
    new runService().listByCheck(this.props.match.checkName, this.props.match.environmentName).then((runRes) => {
      this.setState((state) => {
        return {
          runs: Object.keys(runRes.data).map((key) => {return {timestamp: key, result: runRes.data[key]}}),
          detailsRows: state.detailsRows
        };
      });
    });
  }

  getRunDetails() {
    new checkService().getByNameAndEnvironment(
      this.props.match.checkName,
      this.props.match.environmentName
    ).then((checkRes) => {
      this.setState((state) => {
        return {
          runs: state.runs,
          detailsRows: [
            {name: 'Name', value: this.props.match.checkName},
            {name: 'Environment', value: this.props.match.environmentName},
            {name: 'State', value: checkRes.data.enable ? 'Enabled' : 'Disabled'},
            {name: 'Interval', value: checkRes.data.calculated_interval + 's ' + (checkRes.data.interval == 0 ? '(default)' : '')},
            {name: 'Client Pinning', value: checkRes.data.client ? checkRes.data.client : 'None'},
            {name: 'Supported Clients', value: checkRes.data.supported_clients.join(', ')},
            {name: 'Number of Steps', value: checkRes.data.step_count},
          ]
        }
      })
    })
  }

  onRowClick(val: any) {
    this.props.navigate(`/checks/${this.props.match.checkName}/environments/${this.props.match.environmentName}/runs/${val.row.timestamp}`);
  }

  render() {
    return (
      <Container  maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid
            item
            xs={12} md={8} lg={6} xl={4}
          >
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 250 }} aria-label="Check details">
                <TableBody>
                  {this.state.detailsRows.map((row) => (
                    <TableRow
                      key={row.name}
                      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {row.name}
                      </TableCell>
                      <TableCell align="right">{row.value}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>

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
            <div style={{ height: 800, width: '100%' }}>
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
