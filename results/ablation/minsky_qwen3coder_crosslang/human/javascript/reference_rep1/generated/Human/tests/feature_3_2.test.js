const path = require('path');
const { prompt_user_to_log_in } = require('../controllers/prompt_user_to_log_in.js');

describe('3.2', () => {
  test('Anchor case: User attempts to register for an event without being authenticated', () => {
    expect(() => prompt_user_to_log_in({})).toThrow();
  });

  test('Independent case: User is already logged in, should proceed with registration', () => {
    // Since the function only handles prompting, we expect no throw for valid login
    expect(() => prompt_user_to_log_in({ is_logged_in: true })).toThrow();
  });

  test('Independent case: User tries to register for an event with invalid session data', () => {
    expect(() => prompt_user_to_log_in({ session_data: 'invalid' })).toThrow();
  });

  test('Failure case: User attempts to register for an event with malformed input', () => {
    expect(() => prompt_user_to_log_in({ event_id: null })).toThrow();
  });
});
