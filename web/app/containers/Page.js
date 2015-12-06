import React from 'react';
import {connect} from 'react-redux';

import {signIn, openNewBetForm, cancelNewBetForm, submitNewBet} from '../actions';

import Unsigned from '../components/Unsigned';
import MainHeader from '../components/MainHeader';
import BetList from '../components/BetList';
import NewBet from '../components/NewBet';

const CompletedBets = function (props) {
  return <h1>Completed bets (TODO)</h1>;
};

const Page = function (props) {
  const { dispatch, signedIn, newBet } = props;
  if (!signedIn) {
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
        open={newBet.open}
        onOpen={() => dispatch(openNewBetForm())}
        onCancel={() => dispatch(cancelNewBetForm())}
        onSubmit={(title) => dispatch(submitNewBet(title))}
      />
      <div>
        <h1>Open bets</h1>
        <BetList
          bets={
            [
              {
                title: '2+2=4'
              },
              {
                title: 'CRISPR will kill everyone in 10 years'
              }
            ]
          }
        />
      </div>
      <div>
        <h1>Completed bets</h1>
        (TODO)
      </div>
    </div>
  );
};

function select(state) {
  const {signedIn, newBet} = state;
  return {
    signedIn,
    newBet
  };
}

export default connect(select)(Page);
