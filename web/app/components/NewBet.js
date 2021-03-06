import React, { Component, PropTypes } from 'react';

export default class NewBet extends Component {
  constructor(props) {
    super(props);
    ['submitForm'].forEach(
      (method) => this[method] = this[method].bind(this)
    );
  }

  submitForm() {
    const title = this.refs.title.value.trim();
    const confidence = this.refs.confidence.value.trim();
    this.props.onSubmit(title, confidence);
  }

  render() {
    if (this.props.open) {
      return (
        <div>
          <input type='text' ref='title' disabled={this.props.posting} />
          <input type='text' ref='confidence' disabled={this.props.posting} />
          <button onClick={this.submitForm} disabled={this.props.posting}>
            Submit
          </button>
          <button onClick={this.props.onCancel} disabled={this.props.posting}>
            Cancel
          </button>
        </div>
      );
    }
    return (
      <button onClick={this.props.onOpen}>
        New bet
      </button>
    );
  }
}

NewBet.propTypes = {
  onOpen: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
};
