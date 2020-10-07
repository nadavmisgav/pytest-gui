import React from "react";
import {
  Row,
  Col,
  OverlayTrigger,
  Tooltip,
  Form,
  Button,
} from "react-bootstrap";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import "bootstrap/dist/css/bootstrap.min.css";
import "./Actions.css";

const notify = () => toast.success("Wow so easy !");

function ActionButton({ icon, onClick, description }) {
  const className = "fas action-img " + icon;
  console.log(className);
  return (
    <OverlayTrigger
      key={icon}
      placement="top"
      overlay={<Tooltip id={"tooltip-top"}>{description}</Tooltip>}
    >
      <i className={className} onClick={onClick}></i>
    </OverlayTrigger>
  );
}

function ActionButtons() {
  return (
    <Col>
      <Row className="action-buttons">
        <ActionButton
          icon="fa-play"
          description="Start tests"
          onClick={notify}
        />
        <ActionButton
          icon="fa-stop"
          description="Stop tests"
          onClick={notify}
        />
        <ActionButton
          icon="fa-search"
          description="Discover tests"
          onClick={notify}
        />
      </Row>
    </Col>
  );
}

function Actions({ tests, useTests }) {
  return (
    <React.Fragment>
      <Row className="Actions mb-4">
        <Col className="filter col-8">
          <Row>
            <span className="header">filter</span>
          </Row>
          <Row>
            <Col className="col-8">
              <Form>
                <Form.Group controlId="formFilter">
                  <Form.Control type="input" />
                  {/* <Form.Text className="text-muted">
                  Example
                </Form.Text> */}
                </Form.Group>
              </Form>
            </Col>
            <Col>
              <div className="dark-button">select all</div>
              <div className="dark-button">clear all</div>
            </Col>
          </Row>
        </Col>
        <ActionButtons />
      </Row>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss={false}
        draggable
        pauseOnHover={false}
      />
    </React.Fragment>
  );
}

export default Actions;
