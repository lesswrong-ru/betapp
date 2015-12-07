import {combineReducers} from 'redux';

import signedIn from './signedIn';
import newBet from './newBet';
import bets from './bets';

export default combineReducers({
  signedIn,
  newBet,
  bets,
});

