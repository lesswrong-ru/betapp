import { SIGN_IN, OPEN_NEW_BET_FORM, CANCEL_NEW_BET_FORM, SUBMIT_NEW_BET, FETCH_BETS } from './actions';

const mockState = {
  signedIn: false,
  newBet: {
    open: false,
  },
  bets: [],
  betsFetching: false,
};

export default function (state=mockState, action) {
  switch (action.type) {
    case SIGN_IN:
      return {
        ...state,
        signedIn: true
      };
    case FETCH_BETS:
      switch (action.status) {
        case 'success':
          return {
            ...state,
            bets: action.bets,
            betsFetching: false,
          };
        case 'initiated':
          return {
            ...state,
            betsFetching: true,
          };
        default:
          return state;
      }
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
      switch (action.status) {
        case 'initiated':
          return state; // TODO - disable form
        case 'success':
          return {
            ...state,
            newBet: {
              open: false,
            }
          }
        default:
          return state;
      }
    default:
      return state;
  }
};
