import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import StatusGraphsGrid from "./StatusGraphsGrid";

class HostStatus extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hostData: {status: [], summary: [], host: {},},
            isLoading: false,
            dashboard: props.dashboard,
            hostname: props.hostname,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };

    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchHostStatusData()
        }
    }

    componentDidMount() {
        this.fetchHostStatusData()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchHostStatusData() {

        const hostname = this.state.hostname;

        this.setState({isLoading: true});
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/host/status?hostname='
                                   + hostname + '&datapoints=' + process.env.REACT_APP_NUM_DATAPOINTS;

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({hostData: data, isLoading: false});
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });

    }

    renderHosts(dashboard) {
        dashboard.setState({show: "hosts"})
    }

    render() {

        return (
            <Grid container direction="column">
                <Grid container direction="row" style={{paddingTop: '10px'}}>
                    <Grid item style={{width: '15%', paddingLeft: '10px'}}>
                        <b>HOST NAME</b>:<br />{this.state.hostData.host.hostname}
                        <br /><br />
                        <b>IP address</b>:<br />{this.state.hostData.host.ip_address}
                        <br /><br />
                        <b>MAC address</b>:<br />{this.state.hostData.host.mac_address}
                        <br /><br />
                        <b>Last heard</b>:<br />{this.state.hostData.host.last_heard}
                        <br /><br />  <br /><br />
                        <b>REFRESH IN</b>:<br/>{this.state.countdownValue} seconds
                        <br/><br/> <br/><br/>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderHosts(this.state.dashboard)}>Return to Hosts</Button>
                    </Grid>

                    <Grid item style={{width: '85%', paddingRight: '10px'}}>
                        <StatusGraphsGrid
                            data={this.state.hostData.status}
                            summary={this.state.hostData.summary} >
                        </StatusGraphsGrid>

                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default HostStatus

