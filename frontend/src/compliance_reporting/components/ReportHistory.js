/*
 * Container component
 * All data handling & manipulation should be handled here.
 */

import React, {Component} from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import 'react-table/react-table.css';
import ReactJson from 'react-json-view';
import Select from "../../app/components/Spreadsheet/Select";
import ComplianceReportingStatusHistory from "./ComplianceReportingStatusHistory";
import SnapshotDisplay from "./SnapshotDisplay";

class Delta extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const valueRenderer = row => {
      if (row.value === null) {
        return (<em>null</em>)
      }
      if (row.value instanceof Object) {
        return (
          <ReactJson
            src={row.value}
            theme="grayscale:inverted"
            iconStyle="triangle"
            style={{
              fontFamily: ['Source Code Pro', 'monospace'],
              fontSize: '10px'
            }}
            displayDataTypes={false}
            enableClipboard={false}
            sortKeys
          />
        )
      }
      return (<span>{row.value}</span>);
    };

    const columns =
      [
        {
          id: 'field',
          Header: 'Field',
          accessor: item => {
            let result;
            if (Number.isInteger(item.field)) {
              result = '[' + item.field + ']';
            } else {
              result = '.' + item.field
            }
            if (item.path !== null && item.path !== '') {
              return item.path + result;
            } else {
              return item.field;
            }
          },
        },
        {
          id: 'action',
          Header: 'Action',
          accessor: item => (item.action),
        },
        {
          id: 'oldvalue',
          Header: 'Old Value',
          accessor: item => (item.oldValue),
          Cell: valueRenderer
        },
        {
          id: 'newvalue',
          Header: 'New Value',
          accessor: item => (item.newValue),
          Cell: valueRenderer
        },
        {
          id: 'delta',
          Header: 'Delta',
          accessor: item => {
            const ov = Number.parseFloat(item.oldValue);
            const nv = Number.parseFloat(item.newValue);
            if (Number.isNaN(ov) || Number.isNaN(nv)) {
              return 'N/A'
            }
            return nv - ov;

          }
        }
      ];

    let content = null;
    switch (this.props.activeTab) {
      case 'snapshot':
        content = (
          <SnapshotDisplay
            snapshot={this.props.snapshot.data}
            showHeaders={false}
            computedWarning={this.props.snapshot.computed}
          />);

        break;
      case 'delta':
        content = (
          (this.props.delta.length === 0) &&
          <p>No changes</p> ||
          <ReactTable
            columns={columns}
            data={this.props.delta}
            filterable
            sortable
            defaultPageSize={this.props.delta.length}
          />
        );
        break;
    }
    return (
      <div>
        {content}
      </div>
    )
  }
}

class Current extends Component {
  render() {
    return (
      <div>
        <SnapshotDisplay
          snapshot={this.props.snapshot}
          computedWarning={this.props.computedWarning}
          showHeaders={false}
        />
      </div>
    );
  }
}

class ReportHistory extends Component {

  constructor(props) {
    super(props);
    this.state = {
      activeReport: -1,
      activeTab: 'snapshot'
    };
    this.handleHistorySelection = this.handleHistorySelection.bind(this);
  }

  handleHistorySelection(id, tab) {
    this.setState({
      activeReport: id,
      activeTab: tab
    });

  }

  render() {
    const {deltas} = this.props;
    const {activeReport, activeTab} = this.state;

    let currentSnapshot = this.props.snapshot;
    let currentSnapshotComputed = false;
    if (!currentSnapshot) {
      currentSnapshotComputed = true;
      currentSnapshot = this.props.recomputedTotals || this.props.complianceReport;
    }

    let title;
    switch (String(activeReport)) {
      case '-1':
        title = this.props.complianceReport.displayName;
        break;
      default:
        try {
          title = this.props.deltas.find(x => (String(x.ancestorId) === String(activeReport))).ancestorDisplayName;
        } catch (e) {
          title = "Current Report";
        }
    }

    return (
      <div id="deltas" className="deltas">

        <h1>Report History</h1>

        <ComplianceReportingStatusHistory
          complianceReport={this.props.complianceReport}
          onSwitchHandler={this.handleHistorySelection}
        />

        <div className="history-content panel">
          <div className="panel-body">
            <h1>{title}</h1>
            {(String(activeReport) === '-1') &&
            <Current snapshot={currentSnapshot}
                     computedWarning={currentSnapshotComputed}
                     complianceReport={this.props.complianceReport}
            />

            || deltas.map(d => {

                if (String(activeReport) === String(d.ancestorId)) {
                  return (
                    <Delta
                      key={d.ancestorId}
                      delta={d.delta}
                      snapshot={d.snapshot}
                      activeTab={activeTab}
                    />
                  )
                } else {
                  return null;
                }
              }
            )
            }
          </div>
        </div>
      </div>
    );
  }
}

ReportHistory.defaultProps = {
  deltas: []
};

ReportHistory.propTypes = {
  deltas: PropTypes.array
};

const mapStateToProps = state => ({});

const mapDispatchToProps = {};

export default connect(mapStateToProps, mapDispatchToProps)(ReportHistory);
