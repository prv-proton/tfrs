import React from 'react'
import PropTypes from 'prop-types'
import FontAwesomeIcon from '@fortawesome/react-fontawesome'

import SECURE_DOCUMENT_UPLOAD from '../../constants/routes/SecureDocumentUpload'
import * as Lang from '../../constants/langEnUs'
import PERMISSIONS_CREDIT_TRANSACTIONS from '../../constants/permissions/CreditTransactions'
import PERMISSIONS_SECURE_DOCUMENT_UPLOAD from '../../constants/permissions/SecureDocumentUpload'
import CREDIT_TRANSACTIONS from '../../constants/routes/CreditTransactions'
import SecureFileSubmissionTable from './SecureFileSubmissionTable'
import { useNavigate } from 'react-router'
import { transformDocumentTypeDescription } from '../../utils/functions'

const SecureFileSubmissionsPage = (props) => {
  const { isFetching, items, itemsCount } = props.documentUploads
  const isEmpty = items.length === 0
  const navigate = useNavigate()
  return (
    <div className="page_secure_document_upload">
      <h1>{props.title}</h1>
      {!props.loggedInUser.isGovernmentUser &&
      <p className="instructions">
        <h4>Securely submit files to the Government of British Columbia.</h4>
      </p>
      }
      {!props.loggedInUser.isGovernmentUser &&
        <>
          <dl className="instructions-list">
            <dt>Initiative Agreement: Application</dt>
            <dd>Use this attachment type to submit files related to an application for a new Initiative Agreement.</dd>
            <dt>Initiative Agreement: Evidence of Completion</dt>
            <dd>Use this attachment type to submit files related to demonstrating completion of a designated action under an existing Initiative Agreement.</dd>
            <dt>Other</dt>
            <dd>Use this attachment type to submit files related to compliance reports, transfers, carbon intensity applications, etc.</dd>
          </dl>
        </>
      }
      <div className="right-toolbar-container">
        <div className="actions-container">
          {props.loggedInUser.hasPermission(PERMISSIONS_CREDIT_TRANSACTIONS.PROPOSE) &&
          props.loggedInUser.isGovernmentUser &&
            <button
              id="credit-transfer-new-transfer"
              className="btn btn-primary"
              type="button"
              onClick={() => navigate(CREDIT_TRANSACTIONS.ADD)}
            >
              <FontAwesomeIcon icon="plus-circle" /> New Initiative Agreement Issuance
            </button>
          }

          {props.loggedInUser.hasPermission(PERMISSIONS_SECURE_DOCUMENT_UPLOAD.DRAFT) &&
          <div className="btn-group">
            <button
              id="new-submission"
              className="btn btn-primary"
              onClick={() => {
                const part3Category = props.categories.find(category => category.name === 'Part 3 Agreements')
                const evidence = part3Category.types.find(category => (category.theType === 'Evidence'))
                const route = SECURE_DOCUMENT_UPLOAD.ADD.replace(':type', evidence.id)

                navigate(route)
              }}
              type="button"
            >
              <FontAwesomeIcon icon="plus-circle" /> {Lang.BTN_NEW_SUBMISSION}
            </button>
            <button type="button" className="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <span className="caret" />
              <span className="sr-only">Toggle Dropdown</span>
            </button>
            <ul className="dropdown-menu">
              {props.categories &&
                props.categories.map(category => (
                  (category.types.map(t => (
                    <li key={t.id}>
                      <button
                        onClick={() => {
                          const route = SECURE_DOCUMENT_UPLOAD.ADD.replace(':type', t.id)

                          navigate(route)
                        }}
                        type="button"
                      >
                        {transformDocumentTypeDescription(t.description)}
                      </button>
                    </li>
                  )))
                ))}
            </ul>
          </div>
          }
        </div>
      </div>
      <SecureFileSubmissionTable
        items={items}
        isFetching={isFetching}
        itemsCount={itemsCount}
        isEmpty={isEmpty}
        page={props.page}
        pageSize={props.pageSize}
        filters={props.filters}
        sort={props.sort}
        handlePageChange={props.handlePageChange}
        handlePageSizeChange={props.handlePageSizeChange}
        handleFiltersChange={props.handleFiltersChange}
        handleSortChange={props.handleSortChange}
        loggedInUser={props.loggedInUser}
      />
    </div>
  )
}

SecureFileSubmissionsPage.defaultProps = {
}

SecureFileSubmissionsPage.propTypes = {
  categories: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  documentUploads: PropTypes.shape({
    isFetching: PropTypes.bool,
    items: PropTypes.arrayOf(PropTypes.shape),
    itemsCount: PropTypes.number
  }).isRequired,
  loggedInUser: PropTypes.shape({
    hasPermission: PropTypes.func,
    isGovernmentUser: PropTypes.bool
  }).isRequired,
  title: PropTypes.string.isRequired,
  page: PropTypes.number.isRequired,
  pageSize: PropTypes.number.isRequired,
  filters: PropTypes.arrayOf(PropTypes.object).isRequired,
  sort: PropTypes.arrayOf(PropTypes.object).isRequired,
  handlePageChange: PropTypes.func.isRequired,
  handlePageSizeChange: PropTypes.func.isRequired,
  handleFiltersChange: PropTypes.func.isRequired,
  handleSortChange: PropTypes.func.isRequired
}

export default SecureFileSubmissionsPage
