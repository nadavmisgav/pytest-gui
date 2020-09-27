import React from "react";
import { Row, Col, OverlayTrigger, Tooltip } from "react-bootstrap";

import "bootstrap/dist/css/bootstrap.min.css";
import "./Actions.css";

function ActionButton({ link, callback, description }) {
  return (
    <OverlayTrigger
      key={link}
      placement="top"
      overlay={<Tooltip id={"tooltip-top"}>{description}</Tooltip>}
    >
      <img
        src={link}
        width="92"
        height="92"
        className="d-inline-block"
        alt="Start tests"
      />
    </OverlayTrigger>
  );
}

function Actions() {
  return (
    <Row className="Actions mb-4">
      <Col className="filter"></Col>
      <Col className="action-buttons">
        <ActionButton link="/assets/play.svg" description="Start tests" />
        <ActionButton link="/assets/stop.svg" description="Stop tests" />
        <ActionButton link="/assets/refresh.svg" description="Discover tests" />
      </Col>
    </Row>
  );
}

export default Actions;
