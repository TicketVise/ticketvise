import {shallowMount} from '@vue/test-utils'
import TicketCard from "../components/ticket_overview/TicketCard";

const ticketData = {
  "id": 22,
  "inbox": 1,
  "title": "How long should the demo be?",
  "ticket_inbox_id": 18,
  "author": {
    "first_name": "Bryan",
    "last_name": "Student",
    "email": "bryanstudent@ticketvise.com",
    "username": "bryanstudent",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 6
  },
  "content": "How long should the demo be?",
  "date_created": "2020-08-27T15:19:25.962725+02:00",
  "status": "PNDG",
  "labels": [{"name": "Assignment", "color": "#00ffcd", "id": 9}],
  "assignee": {
    "first_name": "Marco",
    "last_name": "Assistant",
    "email": "marcoassistant@ticketvise.com",
    "username": "marcoassistant",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 8
  },
  "shared_with": []
}


it("card content with assignee", () => {
  const wrapper = shallowMount(TicketCard, {propsData: {ticket: ticketData}});

  expect(wrapper.find("span").text()).toContain(ticketData.ticket_inbox_id);
  let headers = wrapper.findAll("h3");
  expect(headers.length).toBe(2);
  console.log(headers.at(1).text());
  // TODO: Test correct date displayed
  expect(headers[1].text()).toContain("Assignee:");
  expect(headers[1].text()).toContain(ticketData.assignee.first_name);
  expect(headers[1].text()).toContain(ticketData.assignee.last_name);
});