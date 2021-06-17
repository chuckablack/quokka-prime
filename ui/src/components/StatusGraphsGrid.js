import {FlexibleXYPlot, HorizontalGridLines, LineMarkSeries, LineSeries, XAxis, YAxis} from 'react-vis'
import React, {Component} from "react";
import Grid from "@material-ui/core/Grid";
import getStatusData from "./util";
import _ from "lodash";

class StatusGraphsGrid extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
        };
    }

    setSLA(item, slaValue) {
        item.y = slaValue
    }

    generateSLA(slaData, slaValue) {
        if (this.props.sla == null) return;
        slaData.forEach(element => this.setSLA(element, slaValue));
        return (
            <LineSeries
                color="yellow"
                data={slaData}
                strokeStyle="dashed"/>
        )
    }

    render() {

        let data = getStatusData("RSP_TIME", this.props.data);
        const tsRspTimeData = data.tsData;
        const maxYRspTime = data.maxY;
        data = getStatusData("AVAILABILITY", this.props.data);
        const tsAvailabilityData = data.tsData;
        let summaryData = getStatusData("RSP_TIME", this.props.summary);
        const summaryRspTimeData = summaryData.tsData;
        const summaryMaxYRspTime = summaryData.maxY;
        summaryData = getStatusData("AVAILABILITY_SUMMARY", this.props.summary);
        const summaryAvailabilityData = summaryData.tsData;

        let slaAvailability = 0;
        let slaResponseTime = 0;
        if (this.props.sla != null) {
            slaAvailability = this.props.sla.availability;
            slaResponseTime = this.props.sla.response_time;
        }

        return (
            <Grid container direction="row">
                <Grid item style={{width: '50%', padding: '10px'}}>
                    <Grid item>
                        <h5 align='center'>Response Time</h5>
                        <FlexibleXYPlot
                            height={200}
                            xType="time"
                            yDomain={[0, maxYRspTime + (maxYRspTime / 5)]}>
                            <HorizontalGridLines/>
                            <LineSeries
                                data={tsRspTimeData}
                                style={{strokeWidth: 3}}/>
                            <XAxis title="Time of Day" tickTotal={6} style={{text: {fontWeight: 600, fill: "white"}}}/>
                            <YAxis title="Response Time" style={{text: {fontWeight: 600, fill: "white"}}}/>
                        </FlexibleXYPlot>
                    </Grid>
                    <Grid item>
                        <h5 align='center'>Availability</h5>
                        <FlexibleXYPlot
                            height={200}
                            xType="time"
                            yDomain={[0, 100]}>
                            <HorizontalGridLines/>
                            <LineMarkSeries
                                color="green"
                                data={tsAvailabilityData}
                                style={{strokeWidth: 3}}/>
                            <XAxis title="Time of Day" tickTotal={6} style={{text: {fontWeight: 600, fill: "white"}}}/>
                            <YAxis title="Availability" style={{text: {fontWeight: 600, fill: "white"}}}/>
                        </FlexibleXYPlot>
                    </Grid>
                </Grid>
                <Grid item style={{width: '50%', padding: '10px'}}>
                    <Grid item>
                        <h5 align='center'>Response Time: Summary</h5>
                        <FlexibleXYPlot
                            height={200}
                            xType="time"
                            yDomain={[0, Math.max(summaryMaxYRspTime + (summaryMaxYRspTime / 5), slaResponseTime + (slaResponseTime / 5))]}>
                            <HorizontalGridLines/>
                            <LineSeries
                                data={summaryRspTimeData}
                                style={{strokeWidth: 3}}/>
                           {this.generateSLA(_.cloneDeep(summaryRspTimeData), slaResponseTime)}
                            <XAxis title="Time of Day" tickTotal={6} style={{text: {fontWeight: 600, fill: "white"}}}/>
                            <YAxis title="Response Time" style={{text: {fontWeight: 600, fill: "white"}}}/>
                        </FlexibleXYPlot>
                    </Grid>
                    <Grid item>
                        <h5 align='center'>Availability: Summary</h5>
                        <FlexibleXYPlot
                            height={200}
                            xType="time"
                            yDomain={[0, 100]}>
                            <HorizontalGridLines/>
                            <LineMarkSeries
                                color="green"
                                data={summaryAvailabilityData}
                                style={{strokeWidth: 3}}/>
                            {this.generateSLA(_.cloneDeep(summaryAvailabilityData), slaAvailability)}
                            <XAxis title="Time of Day" tickTotal={6} style={{text: {fontWeight: 600, fill: "white"}}}/>
                            <YAxis title="Availability" style={{text: {fontWeight: 600, fill: "white"}}}/>
                        </FlexibleXYPlot>
                    </Grid>
                </Grid>
            </Grid>
        );
    }
}

export default StatusGraphsGrid;

