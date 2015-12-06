import React from 'react';

export default React.createClass({
  render () {
    return (
      <div>
        <h1>Please sign in</h1>
        <button onClick={this.handleClick}>Fake sign in</button>
      </div>
    );
  },

  handleClick (e) {
    this.props.signIn();
  },
});
