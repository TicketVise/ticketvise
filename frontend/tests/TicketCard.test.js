import {shallowMount} from '@vue/test-utils'
import TicketCard from "@/ticket_overview/TicketCard";
import moment from "moment";

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
  "labels": [{"name": "Assignment", "color": "#00ffcd", "id": 9}, {"name": "second", "color": "#00ffcd", "id": 10}],
  "assignee": {
    "first_name": "Marco",
    "last_name": "Assistant",
    "email": "marcoassistant@ticketvise.com",
    "username": "marcoassistant",
    "avatar_url": "/static/img/avatars/default-avatar.png",
    "id": 8
  },
  "shared_with": []
};


it("card content with assignee", () => {
  const wrapper = shallowMount(TicketCard, {propsData: {ticket: ticketData}});

  expect(wrapper.find("span").text()).toContain(ticketData.ticket_inbox_id);
  let headers = wrapper.findAll("h3");
  expect(headers.length).toBe(2);
  expect(headers.at(0).text()).toContain(moment(ticketData.date_created).calendar());
  expect(headers.at(1).text()).toContain("Assignee:");
  expect(headers.at(1).text()).toContain(ticketData.assignee.first_name);
  expect(headers.at(1).text()).toContain(ticketData.assignee.last_name);

  expect(wrapper.find("a").text()).toBe(ticketData.title);
  expect(wrapper.find("a").attributes().href).toContain(window.location.href + '/' + ticketData.ticket_inbox_id);

  for (let i = 0; i < ticketData.labels.length; i++) {
    expect(wrapper.find("div").html()).toContain(ticketData.labels[i].name)
  }
});

ticketData.assignee = {"first_name": "", "last_name": "", "email": "", "username": "", "avatar_url": ""};

it("card content without assignee", () => {
  const wrapper = shallowMount(TicketCard, {propsData: {ticket: ticketData}});

  let headers = wrapper.findAll("h3");
  expect(headers.length).toBe(2);
  expect(headers.at(1).text()).toContain("Assignee: None");
});

ticketData.labels = [];

it("card content without labels", () => {
  const wrapper = shallowMount(TicketCard, {propsData: {ticket: ticketData}});

  expect(wrapper.find("div").html()).toBe("<div class=\"space-x-1 select-none\"></div>")
});

it("card content small", () => {
  const wrapper = shallowMount(TicketCard, {propsData: {ticket: ticketData, small: true}});

  expect(wrapper.find("span").text()).toBe(`#${ticketData.ticket_inbox_id}`);
  expect(wrapper.contains("div")).toBeFalsy()
});

