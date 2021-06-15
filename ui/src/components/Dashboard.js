import React, {Component} from 'react';
import Grid from "@material-ui/core/Grid";
import DashboardAppBar from "./DashboardAppBar";
import Devices from "./Devices";
import Hosts from "./Hosts";
import Services from "./Services";
import HostStatus from "./HostStatus"
import ServiceStatus from "./ServiceStatus"
import DeviceStatus from "./DeviceStatus"
import Capture from "./Capture";
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline'

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            show: "devices",
        };
    }

    render() {
        const {show, ip, protocol, port, name} = this.state
        const darkTheme = createMuiTheme({palette: {type: 'dark',},});

        let info;

        if (show === "devices") {
            info = <Devices dashboard={this}/>;
        } else if (show === "hosts") {
            info = <Hosts dashboard={this}/>;
        } else if (show === "services") {
            info = <Services dashboard={this}/>;
        } else if (show === "capture") {
            info = <Capture dashboard={this} ip={ip} protocol={protocol} port={port} />;
        } else if (show === "hoststatus") {
            info = <HostStatus dashboard={this} hostname={name} />;
        } else if (show === "servicestatus") {
            info = <ServiceStatus dashboard={this} name={name} />;
        } else if (show === "devicestatus") {
            info = <DeviceStatus dashboard={this} name={name} />;
        }

        return (
            <Grid container direction="column">
                <ThemeProvider theme={darkTheme}>
                    <CssBaseline/>
                    <DashboardAppBar dashboard={this}/>
                    <Grid container direction="row" style={{paddingTop: "10px"}}>
                        <Grid item style={{width: '100%'}}>
                            {info}
                        </Grid>
                    </Grid>
                </ThemeProvider>
            </Grid>
        );
    }
}

export default Dashboard;
