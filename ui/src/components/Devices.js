import React, {Component} from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";
import {green, red} from "@material-ui/core/colors";
import CancelIcon from "@material-ui/icons/Cancel";
import MaterialTable from "material-table";
import AccountTreeRoundedIcon from '@material-ui/icons/AccountTreeRounded'
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";

class Devices extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: [],
            dashboard: props.dashboard,
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openTraceRouteDialog: false,
            target: '',
            traceRouteResults: {traceroute_img: ''},
            token: '',
        };
    }

    countdown() {
        this.setState({countdownValue: this.state.countdownValue-1})
        if (this.state.countdownValue === 0) {
            this.fetchDevices()
        }
    }

    fetchDevices() {

        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/devices'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({devices: data})
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            })
            .catch((e) => {
                console.log(e)
                this.setState({countdownValue: process.env.REACT_APP_REFRESH_RATE})
            });
    }

    initiateTraceRoute( target ) {

        this.setState({traceRouteResults: {result: "initiating trace route ...", traceroute_img: ""}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/traceroute?target=' + target
        const requestOptions = { method: 'POST'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({token: data.token})
                this.fetchTraceRouteResults(target)
                console.log(this.state.traceRouteResults)
            })
            .catch(console.log)
    }

    fetchTraceRouteResults( target ) {
        this.setState({traceRouteResults: {result: "fetching route results ...", traceroute_img: ""}})
        let requestUrl = process.env.REACT_APP_QUOKKA_HOST + '/traceroute?target=' + target + '&token=' + this.state.token
        const requestOptions = { method: 'GET'}
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({traceRouteResults: data})
                console.log(this.state.traceRouteResults)
            })
            .catch(console.log)

    }

    componentDidMount() {
        this.fetchDevices(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderCapture(ip) {
        this.state.dashboard.setState({ip: ip, protocol: null, port: null, show: "capture"})
    }

    renderTraceRouteDialog(target) {
        this.initiateTraceRoute(target)
        this.setState({openTraceRouteDialog: true, target: target})
    }

    handleCloseTraceRouteDialog(parent) {
        parent.setState({openTraceRouteDialog: false})
    }

    render() {

        const {devices} = this.state;

        return (
            <div className="container" style={{maxWidth: "100%"}}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Devices Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchDevices()
                    }}>Refresh Devices</Button>
                </Grid>
                <MaterialTable
                    title="Devices with Availability, Response Time, Model, Version"
                    columns={[
                        {
                            width: null,
                            title: 'Status',
                            render: rowData =>
                                rowData.availability ?
                                    <CheckCircleIcon style={{color: green[500]}}/>
                                    : <CancelIcon style={{color: red[500]}}/>,
                            customSort: (a, b) => {
                                if( a.availability && !b.availability ) return 1;
                                else if (a.availability === b.availability ) return 0
                                else return -1;
                            }
                        },
                        {   title: 'Name',
                            field: 'name',
                            defaultSort: 'asc',
                            customSort: (a, b) => {
                                if( a.name.toUpperCase() > b.name.toUpperCase() ) return 1;
                                else if( a.name.toUpperCase() < b.name.toUpperCase() ) return -1;
                                else return 0;
                            }
                        },
                        { title: 'Hostname', field: 'hostname', defaultSort: 'asc' },
                        { title: 'Vendor:OS', render: rowData => rowData.vendor + ":" + rowData.os},
                        { title: 'IP Address', field: 'ip_address' },
                        { title: 'Model', field: 'model' },
                        { title: 'Version', field: 'os_version' },
                        { title: 'Rsp Time', render: rowData =>  rowData.response_time.toFixed(3) },
                        { title: 'Last Checked', field: 'last_heard' },
                    ]}
                    data={  Object.values(devices) }
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                        rowStyle: (rowData) => {
                            if(!rowData.availability) {
                                return {color: 'red'};
                            }
                            else {
                                return {color: 'chartreuse'}
                            }
                        },
                        cellStyle: { fontSize: 14, }
                    }}
                    actions={[
                        {
                            icon: 'pageview',
                            tooltip: 'Capture packets for host',
                            onClick: (event, rowData) => {
                                this.renderCapture(rowData.ip_address)
                            }
                        },
                        {
                            icon: AccountTreeRoundedIcon,
                            tooltip: 'Trace-route to service',
                            onClick: (event, rowData) => {
                                this.renderTraceRouteDialog(rowData.ip_address)
                            }
                        }
                    ]}
                />
                <Dialog
                    open={this.state.openTraceRouteDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Trace Route Results: {this.state.target}</DialogTitle>
                    <DialogContent>
                        <b>Output from trace route:</b><br />
                        Result: {this.state.traceRouteResults.result}
                        <br /><br />
                        <img id="traceroute"
                             src={"data:image/png;base64," + this.state.traceRouteResults.traceroute_img}
                             alt="">
                        </img>
                        <br /><br />
                        <b>NOTE:</b><br />
                        Depending on the target, trace route may take up to a few minutes to complete
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleCloseTraceRouteDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default Devices;
