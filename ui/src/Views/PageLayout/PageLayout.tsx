
import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { AppBar, Badge, Box, CssBaseline, Divider, Drawer, IconButton, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import NotificationsIcon from '@mui/icons-material/Notifications';
import DashboardIcon from '@mui/icons-material/Dashboard';
import DomainIcon from '@mui/icons-material/Domain';

class PageLayout extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      open: false,
    };
    this.toggleDrawer = this.toggleDrawer.bind(this);
    this.mdTheme = createTheme();
  }

  toggleDrawer() {
    console.log(this.state);
    this.setState((state) => {return {open: !state.open};});
  };


  render() {
    return (
      <ThemeProvider theme={this.mdTheme}>
        <Box sx={{ display: 'flex' }}>

          <CssBaseline />
          <AppBar position="fixed">
            <Toolbar
              sx={{
                pr: '24px', // keep right padding when drawer closed
              }}
            >
              <Typography
                component="h1"
                variant="h6"
                color="inherit"
                noWrap
                sx={{ flexGrow: 1 }}
              >
                JMon
              </Typography>
              <Typography
                color="inherit"
                noWrap
                sx={{ flexGrow: 1 }}
              >
                Made with &lt;3 - github.com/matthewjohn/jmon
              </Typography>
            </Toolbar>
          </AppBar>
          <Box
            component="main"
            sx={{
              backgroundColor: (theme) =>
                theme.palette.mode === 'light'
                  ? theme.palette.grey[100]
                  : theme.palette.grey[900],
              flexGrow: 1,
              height: '100vh',
              overflow: 'auto',
            }}
          >
            <Toolbar />
            {this.props.children}

          </Box>
        </Box>
      </ThemeProvider>
    );
  }
}

export default PageLayout;
