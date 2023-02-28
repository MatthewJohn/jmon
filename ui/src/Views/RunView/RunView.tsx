
import { Typography } from '@mui/material';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import * as React from 'react';
import client from '../../client.tsx';
import runService from '../../run.service.tsx';
import { withRouter } from '../../withRouter';


class RunView extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      run: {artifacts: [], status: undefined},
      log: ""
    };
    this.retrieveRun = this.retrieveRun.bind(this);
    this.screenshotFromArtifact = this.screenshotFromArtifact.bind(this);
  }

  componentDidMount() {
    this.retrieveRun();
  }

  retrieveRun() {
    new runService().getById(this.props.match.checkName, this.props.match.environmentName, this.props.match.runTimestamp).then((runRes) => {
      this.setState({
        run: runRes.data,
        log: this.state.log
      });
    });
    new runService().getLogById(this.props.match.checkName, this.props.match.environmentName, this.props.match.runTimestamp).then((runRes) => {
      this.setState({
        log: runRes.data,
        run: this.state.run
      });
    });
  }

  screenshotFromArtifact(artifactName) {
    if (artifactName.indexOf('.png', artifactName.length - 4) !== -1) {
      let imageUrl = (client.defaults.baseURL + "/checks/" +
        this.props.match.checkName +
        "/environments/" + this.props.match.environmentName +
        "/runs/" + this.props.match.runTimestamp + "/artifacts/" + artifactName);
      return (
        <a key={artifactName} href={imageUrl}>
          <span>{artifactName}</span>
          <img className='artifact-image' src={imageUrl} />
        </a>
      );
    } else {
      return <div key={artifactName}></div>;
    }
  }

  render() {
    return (
      <Container  maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Typography component="h2" variant="h5">
          {this.props.match.checkName} - {this.props.match.environmentName} - {this.props.match.runTimestamp}
        </Typography>
        <Grid container spacing={3}>
          <Grid
            item
            xs={12} md={12} lg={10} xl={8}
          >
            <Typography component="h4" variant="h5">
              Log
            </Typography>
            <div style={{ height: 800, width: '100%' }}>
                <code style={{textAlign: 'left'}}>
                  <pre>{this.state.log}</pre>
                </code>
            </div>
          </Grid>

          <Grid
            item
            xs={12} md={12} lg={10} xl={8}
            sx={{
              '& .artifact-image': {
                borderColor: 'black',
                borderStyle: 'solid',
                borderWidth: '1px',

                maxHeight: '400px',
                maxWidth: '30%'
              }
            }}
          >
            <Typography component="h4" variant="h5">
              Screenshots
            </Typography>
            <div style={{ height: 800, width: '100%' }}>
                {this.state.run.artifacts.map((val) => this.screenshotFromArtifact(val))}
            </div>
          </Grid>
        </Grid>
      </Container>
    );
  }
}

export default withRouter(RunView);
