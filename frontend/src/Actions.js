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

function ActionButton({ link, callback, description }) {
  return (
    <OverlayTrigger
      key={link}
      placement="top"
      overlay={<Tooltip id={"tooltip-top"}>{description}</Tooltip>}
    >
      <img
        className="action-img d-inline-block"
        src={link}
        alt={description}
        onClick={callback}
      />
    </OverlayTrigger>
  );
}

function ActionButtons() {
  return (
    <Col className="action-buttons">
      <ActionButton
        link="/assets/play.svg"
        description="Start tests"
        callback={notify}
      />
      <ActionButton
        link="/assets/stop.svg"
        description="Stop tests"
        callback={notify}
      />
      <ActionButton
        link="/assets/search.svg"
        description="Discover tests"
        callback={notify}
      />
    </Col>
  );
}

function Actions({ tests, useTests }) {
  return (
    <React.Fragment>
      <Row className="Actions mb-4">
        <Col className="filter">
          <Row>
            <span className="header">filter</span>
          </Row>
          <Row>
            <Col>
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
              <Button className="dark-button">select all</Button>
            </Col>
            <Col>
              <Button className="dark-button">clear all</Button>
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
