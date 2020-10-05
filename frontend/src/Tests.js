import React from "react";
import Collapsible from "react-collapsible";

import "bootstrap/dist/css/bootstrap.min.css";
import "./Tests.css";
import { Row, Col } from "react-bootstrap";

function Tests() {
  return (
    <React.Fragment>
      <Row className="title-row">
        <Col className="col-8">
          <span>Tests</span>
        </Col>
        <Col className="col-4">
          <span>Logs</span>
        </Col>
      </Row>
      <Row className="Tests mb-4">
        <Col className="tests col-8">
          <Collapsible trigger="Start here">
            <p>
              This is the collapsible content. It can be any element or React
              component you like.
            </p>
            <p>
              It can even be another Collapsible component. Check out the next
              section!
            </p>
          </Collapsible>
          <Collapsible trigger="Start here">
            <p>
              This is the collapsible content. It can be any element or React
              component you like.
            </p>
            <p>
              It can even be another Collapsible component. Check out the next
              section!
            </p>
          </Collapsible>
        </Col>
        <Col className="logs col-4">
          <p id="log-area">
            Labore ea ad et in. Sit occaecat deserunt exercitation id commodo
            commodo ullamco pariatur consectetur pariatur cupidatat ex. Sint
            nostrud quis consequat pariatur aliqua veniam reprehenderit
            proident. Minim est cillum ut nostrud ullamco. Cillum et aute labore
            est ad in commodo irure eiusmod. Labore id nostrud laboris non sint
            consectetur sunt. Irure ea qui laborum pariatur labore cupidatat
            reprehenderit eu est officia pariatur do sint. Aliquip qui magna
            anim ea qui aute aute sint sint non quis excepteur sit. Et nulla
            fugiat ea nisi laborum mollit aute mollit esse ex id veniam. Duis
            deserunt sunt consectetur et est amet magna incididunt duis mollit
            cupidatat cupidatat aute. Cupidatat sit cillum sunt reprehenderit
            quis. Elit labore aliquip excepteur ut dolor officia. Magna cillum
            excepteur ullamco magna non occaecat ut minim excepteur consequat
            incididunt. Exercitation in labore labore et nostrud esse minim eu
            exercitation incididunt aliquip anim. Id anim anim in id cupidatat
            labore. Mollit aliquip dolor veniam eiusmod consequat. Deserunt
            consectetur tempor aliqua eiusmod commodo commodo sint. Ex irure
            enim aliquip mollit dolor pariatur quis voluptate amet. Labore ea ad
            et in. Sit occaecat deserunt exercitation id commodo commodo ullamco
            pariatur consectetur pariatur cupidatat ex. Sint nostrud quis
            consequat pariatur aliqua veniam reprehenderit proident. Minim est
            cillum ut nostrud ullamco. Cillum et aute labore est ad in commodo
            irure eiusmod. Labore id nostrud laboris non sint consectetur sunt.
            Irure ea qui laborum pariatur labore cupidatat reprehenderit eu est
            officia pariatur do sint. Aliquip qui magna anim ea qui aute aute
            sint sint non quis excepteur sit. Et nulla fugiat ea nisi laborum
            mollit aute mollit esse ex id veniam. Duis deserunt sunt consectetur
            et est amet magna incididunt duis mollit cupidatat cupidatat aute.
            Cupidatat sit cillum sunt reprehenderit quis. Elit labore aliquip
            excepteur ut dolor officia. Magna cillum excepteur ullamco magna non
            occaecat ut minim excepteur consequat incididunt. Exercitation in
            labore labore et nostrud esse minim eu exercitation incididunt
            aliquip anim. Id anim anim in id cupidatat labore. Mollit aliquip
            dolor veniam eiusmod consequat. Deserunt consectetur tempor aliqua
            eiusmod commodo commodo sint. Ex irure enim aliquip mollit dolor
            pariatur quis voluptate amet.
          </p>
        </Col>
      </Row>
    </React.Fragment>
  );
}

export default Tests;
