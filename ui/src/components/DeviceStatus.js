import {FlexibleXYPlot, HorizontalGridLines, LineMarkSeries, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import StatusGraphsGrid from "./StatusGraphsGrid";

class DeviceStatus extends Component {

    constructor(props) {
        super(props);
        this.state = {
            name: props.name,
            deviceData: {status: [], summary: [], device: {}},
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };

    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchDeviceStatusData()
        }
    }

    componentDidMount() {
        this.fetchDeviceStatusData()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    fetchDeviceStatusData() {

        const name = this.state.name;

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/device/status?name='
                                   + name + '&datapoints=' + process.env.REACT_APP_NUM_DATAPOINTS

        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({deviceData: data});
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });

    }

    renderDevices(dashboard) {
        dashboard.setState({show: "devices"})
    }

    render() {

        return (
            <Grid container direction="column">
                <Grid container direction="row" style={{paddingTop: '10px'}}>
                    <Grid item style={{width: '15%', paddingLeft: '10px'}}>
                        <b>DEVICE NAME</b>:<br/>{this.state.deviceData.device.name}
                        <br/><br/>
                        <b>IP ADDRESS</b>:<br/>{this.state.deviceData.device.ip_address}
                        <br/><br/>
                        <b>LAST HEARD</b>:<br/>{this.state.deviceData.device.last_heard}
                        <br/><br/> <br/><br/>
                        <b>REFRESH IN</b>:<br/>{this.state.countdownValue} seconds
                        <br/><br/> <br/><br/>
                        <Button variant="contained" style={{width: '100%'}} onClick={() => this.renderDevices(this.state.dashboard)}>Return to
                            Devices</Button>
                    </Grid>

                    <Grid item style={{width: '85%', paddingRight: '10px'}}>
                        <StatusGraphsGrid
                            data={this.state.deviceData.status}
                            summary={this.state.deviceData.summary}
                            sla={{availability: this.state.deviceData.device.sla_availability,
                                  response_time: this.state.deviceData.device.sla_response_time}}>
                        </StatusGraphsGrid>
                    </Grid>

                </Grid>
            </Grid>
        );

    }
}

export default DeviceStatus

