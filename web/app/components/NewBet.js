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
    this.props.onSubmit(title);
  }

  render() {
    if (this.props.open) {
      return (
        <div>
          <input type='text' ref='title'/>
          <button onClick={this.submitForm}>Submit</button>
          <button onClick={this.props.onCancel}>Cancel</button>
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
