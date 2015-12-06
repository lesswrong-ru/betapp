import { SIGN_IN, OPEN_NEW_BET_FORM, CANCEL_NEW_BET_FORM, SUBMIT_NEW_BET } from './actions';

const mockState = {
  signedIn: false,
  newBet: {
    open: false,
  },
  open: [],
  completed: [],
};

export default function (state=mockState, action) {
  switch (action.type) {
    case SIGN_IN:
      return {
        ...state,
        signedIn: true
      };
    case OPEN_NEW_BET_FORM:
      return {
        ...state,
        newBet: {
          ...state.newBet,
          open: true,
        }
      };
    case CANCEL_NEW_BET_FORM:
      return {
        ...state,
        newBet: {
          ...state.newBet,
          open: false,
        }
      };
    case SUBMIT_NEW_BET:
      console.log('SUBMIT_NEW_BET: ' + action.title);
      return state;
    default:
      return state;
  }
};
