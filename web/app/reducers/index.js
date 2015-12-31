import {combineReducers} from 'redux';

import signedIn from './signedIn';
import newBet from './newBet';
import bets from './bets';
import internalError from './internalError';

export default combineReducers({
  internalError,
  signedIn,
  newBet,
  bets,
});

