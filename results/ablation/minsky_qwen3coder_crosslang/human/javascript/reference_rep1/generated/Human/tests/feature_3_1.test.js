const path = require('path');
const { edit_event_details_and_registration } = require('../controllers/edit_event_details_and_registration.js');

describe('3.1', () => {
  test('Anchor case: Edit event details and registration requirements with valid inputs', () => {
    const inputs = {"event_id":"evt-12345","updated_details":{"title":"Updated Workshop","description":"An updated description"},"updated_registration_requirements":{"age_limit":18}};
    const expected = {"status": "success", "message": "Event details and registration requirements updated successfully"};
    expect(edit_event_details_and_registration(inputs)).toEqual(expected);
  });

  test('Independent case: Edit event details with empty updated details dictionary', () => {
    const inputs = {"event_id":"evt-12345","updated_details":{},"updated_registration_requirements":{"age_limit":18}};
    const expected = {"status": "success", "message": "Event details and registration requirements updated successfully"};
    expect(edit_event_details_and_registration(inputs)).toEqual(expected);
  });

  test('Independent case: Edit event registration requirements with empty updated registration requirements dictionary', () => {
    const inputs = {"event_id":"evt-12345","updated_details":{"title":"Updated Workshop","description":"An updated description"},"updated_registration_requirements":{}};
    const expected = {"status": "success", "message": "Event details and registration requirements updated successfully"};
    expect(edit_event_details_and_registration(inputs)).toEqual(expected);
  });

  test('Independent case: Attempt to edit event details and registration requirements with invalid event ID', () => {
    const inputs = {"event_id":"evt-99999","updated_details":{"title":"Updated Workshop","description":"An updated description"},"updated_registration_requirements":{"age_limit":18}};
    expect(() => edit_event_details_and_registration(inputs)).toThrow();
  });
});
