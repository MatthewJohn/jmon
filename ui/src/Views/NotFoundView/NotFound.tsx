
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import * as React from 'react';


class NotFound extends React.Component {

  render() {
    return (
      <Container  maxWidth="xl" sx={{ mt: 10, mb: 10 }}>
        <Grid container>
          <Grid item xs={12} md={12} lg={12} xl={12}>
            404 - Not found
          </Grid>
        </Grid>
      </Container>
    );
  }
}

export default NotFound;
