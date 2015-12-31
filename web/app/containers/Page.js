import React, {Component} from 'react';
import {connect} from 'react-redux';

import {signIn, openNewBetForm, cancelNewBetForm, removeBet, resolveBet, submitNewBet, fetchBets} from '../actions';

import Unsigned from '../components/Unsigned';
import MainHeader from '../components/MainHeader';
import BetList from '../components/BetList';
import NewBet from '../components/NewBet';

const CompletedBets = function (props) {
  return <h1>Completed bets (TODO)</h1>;
};

class Page extends Component {
  componentDidMount () {
    this.props.dispatch(fetchBets());
  }

  render () {
    const props = this.props;
    const { dispatch } = props;
    if (!props.signedIn) {
      return (
        <Unsigned
          signIn={() => dispatch(signIn())}
        />
      );
    }

    return (
      <div>
        <MainHeader/>
        <NewBet
          open={props.newBet.open}
          posting={props.newBet.posting}
          onOpen={() => dispatch(openNewBetForm())}
          onCancel={() => dispatch(cancelNewBetForm())}
          onSubmit={(title, confidence) => dispatch(submitNewBet(title, confidence))}
        />
        <div>
          <h1>Open bets</h1>
          <BetList
            loading={props.bets.fetching}
            bets={props.bets.items}
            onRemove={(id) => dispatch(removeBet(id))}
            onResolve={(id, outcome) => dispatch(resolveBet(id, outcome))}
          />
        </div>
        <div>
          <h1>Completed bets</h1>
          (TODO)
        </div>
      </div>
    );
  }
};

export default connect(state => state)(Page);
