import {shallowMount} from '@vue/test-utils'
import TicketColumn from "../components/inbox/TicketColumn";
import TicketCard from "../components/inbox/TicketCard";

const colorData = "#e9c46a";
const titleData = "Assigned";
const ticketListData = [{
  "id": 7,
  "inbox": 1,
  "title": "When is the next SWEBOK panel?",
  "ticket_inbox_id": 3,
  "author": {
    "first_name": "Ivan",
    "last_name": "Student",
    "email": "ivanstudent@ticketvise.com",
    "username": "ivanstudent",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 2,
    "is_superuser": false
  },
  "content": "On Canvas the times do not indicate the group.",
  "date_created": "2020-09-12T16:15:27.318349+02:00",
  "status": "ASGD",
  "labels": [{"name": "SWEBOK", "color": "#6B7280", "id": 4}],
  "assignee": {
    "first_name": "Ana",
    "last_name": "Coordinator",
    "email": "info@ticketvise.com",
    "username": "anacoordinator",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 5,
    "is_superuser": true
  },
  "shared_with": []
}, {
  "id": 16,
  "inbox": 1,
  "title": "Should the SWEBOK panel questions I answered in eJournal be in my individual report?",
  "ticket_inbox_id": 12,
  "author": {
    "first_name": "Bryan",
    "last_name": "Student",
    "email": "bryanstudent@ticketvise.com",
    "username": "bryanstudent",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 6,
    "is_superuser": true
  },
  "content": "Should the SWEBOK panel questions I answered in eJournal be in my individual report?",
  "date_created": "2020-09-12T15:32:27.409346+02:00",
  "status": "ASGD",
  "labels": [{"name": "SWEBOK", "color": "#6B7280", "id": 4}, {
    "name": "Individual Report",
    "color": "#F05252",
    "id": 5
  }, {"name": "E-Journal", "color": "#C27803", "id": 7}],
  "assignee": {
    "first_name": "Jelle",
    "last_name": "Assistant",
    "email": "jelleassistant@ticketvise.com",
    "username": "jelleassistant",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 4,
    "is_superuser": true
  },
  "shared_with": []
}, {
  "id": 15,
  "inbox": 1,
  "title": "Why are there no project proposals for eJournal?",
  "ticket_inbox_id": 11,
  "author": {
    "first_name": "Bryan",
    "last_name": "Student",
    "email": "bryanstudent@ticketvise.com",
    "username": "bryanstudent",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 6,
    "is_superuser": true
  },
  "content": "Why are there no project proposals for eJournal?",
  "date_created": "2020-09-12T14:52:27.396342+02:00",
  "status": "ASGD",
  "labels": [{"name": "Assignment", "color": "#0E9F6E", "id": 9}, {"name": "E-Journal", "color": "#C27803", "id": 7}],
  "assignee": {
    "first_name": "Tom",
    "last_name": "Assistant",
    "email": "tomassistant@ticketvise.com",
    "username": "tomassistant",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 7,
    "is_superuser": true
  },
  "shared_with": []
}, {
  "id": 14,
  "inbox": 1,
  "title": "Is there a lecture on the day of the demo?",
  "ticket_inbox_id": 10,
  "author": {
    "first_name": "Bryan",
    "last_name": "Student",
    "email": "bryanstudent@ticketvise.com",
    "username": "bryanstudent",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 6,
    "is_superuser": true
  },
  "content": "Is there a lecture on the day of the demo? I want to make my report!",
  "date_created": "2020-09-12T14:15:27.383346+02:00",
  "status": "ASGD",
  "labels": [{"name": "Lecture", "color": "#0694A2", "id": 6}, {
    "name": "Individual Report",
    "color": "#F05252",
    "id": 5
  }],
  "assignee": {
    "first_name": "Ana",
    "last_name": "Coordinator",
    "email": "info@ticketvise.com",
    "username": "anacoordinator",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 5,
    "is_superuser": true
  },
  "shared_with": []
}];

it("Column content", () => {
  const wrapper = shallowMount(TicketColumn, {
    propsData: {
      ticketList: ticketListData,
      title: titleData,
      color: colorData
    }
  });
  const header = wrapper.findAll("div").at(0);
  expect(header.text()).toContain(titleData);
  expect(header.text()).toContain(ticketListData.length);

  var cards = wrapper.findAllComponents(TicketCard);
  expect(cards.length).toBe(ticketListData.length)
});

it("Column no content", () => {
  const wrapper = shallowMount(TicketColumn, {
    propsData: {
      ticketList: [],
      title: titleData,
      color: colorData
    }
  });
  const header = wrapper.findAll("div").at(0);
  expect(header.text()).toContain(titleData);
  expect(header.text()).toContain(0);

  let cards = wrapper.findAllComponents(TicketCard);
  expect(cards.length).toBe(0)
});
