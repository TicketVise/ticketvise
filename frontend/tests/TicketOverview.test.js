import {mount, shallowMount} from "@vue/test-utils";
import TicketOverview from "../components/inbox/TicketOverview";
import SearchBar from "../components/elements/SearchBar";
import LabelDropdown from "../components/elements/dropdown/LabelDropdown";
import SubmitButton from "../components/elements/buttons/SubmitButton";

const colorData = ["#e76f51", "#e9c46a", "#2a9d8f", "#264653"];
const inboxLabelsData = [{"name": "Assignment", "color": "#00ffcd", "id": 9}, {
  "name": "E-Journal",
  "color": "#fbf06d",
  "id": 7
}, {"name": "Individual Report", "color": "#29ff00", "id": 5}, {
  "name": "Laptop",
  "color": "#150a1a",
  "id": 8
}, {"name": "Lecture", "color": "#0090ff", "id": 6}, {"name": "SWEBOK", "color": "#ff0000", "id": 4}];
const ticketsData = [{"label": "Pending", "tickets": []}, {
  "label": "Assigned",
  "tickets": [{
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
    "date_created": "2020-08-26T14:06:40.763865+02:00",
    "status": "ASGD",
    "labels": [{"name": "SWEBOK", "color": "#ff0000", "id": 4}],
    "assignee": {
      "first_name": "Ana",
      "last_name": "Coordinator",
      "email": "anacoordinator@ticketvise.com",
      "username": "anacoordinator",
      "avatar_url": "/static/img/avatars/default-avatar.png",
      "id": 5,
      "is_superuser": false
    },
    "shared_with": []
  }, {
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
      "id": 6,
      "is_superuser": false
    },
    "content": "How long should the demo be?",
    "date_created": "2020-08-26T14:01:41.067229+02:00",
    "status": "ASGD",
    "labels": [{"name": "Assignment", "color": "#00ffcd", "id": 9}],
    "assignee": {
      "first_name": "Ana",
      "last_name": "Coordinator",
      "email": "anacoordinator@ticketvise.com",
      "username": "anacoordinator",
      "avatar_url": "/static/img/avatars/default-avatar.png",
      "id": 5,
      "is_superuser": false
    }
  }]
}];
const userData = {
  "first_name": "Ana",
  "last_name": "Coordinator",
  "email": "anacoordinator@ticketvise.com",
  "username": "anacoordinator",
  "avatar_url": "/static/img/avatars/default-avatar.png",
  "id": 5,
  "is_superuser": false,
};

it("Ticket Overview navigation", async () => {
  const wrapper = mount(TicketOverview, {
    data () {
      return {
      color: colorData,
      inbox_id: "1",
      inbox_labels: inboxLabelsData,
      is_staff: true,
      showPersonal: false,
      tickets: ticketsData,
      user: userData,
      search: null,
      labels: [],
      label: null,}
    }
  });

  expect(wrapper.findAllComponents(SearchBar).length).toBe(1);
  expect(wrapper.findAllComponents(LabelDropdown).length).toBe(1);

  let test = wrapper.vm.is_staff;
  let myTicketsButton = wrapper.findAllComponents(SubmitButton);
  expect(myTicketsButton.length).toBe(1);

  // Test toggle my tickets
  expect(wrapper.vm.showPersonal).toBeFalsy();
  await myTicketsButton.trigger("click");
  await wrapper.vm.$nextTick();
  expect(wrapper.vm.showPersonal).toBeTruthy();
});
