export const SIGN_IN = 'SIGN_IN';
export const OPEN_NEW_BET_FORM = 'OPEN_NEW_BET_FORM';
export const CANCEL_NEW_BET_FORM = 'CANCEL_NEW_BET_FORM';
export const SUBMIT_NEW_BET = 'SUBMIT_NEW_BET';

export function signIn() {
  return {
    type: SIGN_IN
  }
};

export function openNewBetForm() {
  return {
    type: OPEN_NEW_BET_FORM
  }
};

export function cancelNewBetForm() {
  return {
    type: CANCEL_NEW_BET_FORM
  }
};

export function submitNewBet(title) {
  return {
    type: SUBMIT_NEW_BET,
    title: title,
  }
};
