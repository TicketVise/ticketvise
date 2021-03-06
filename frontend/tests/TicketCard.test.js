import {shallowMount} from '@vue/test-utils'
import TicketCard from "@/inbox/TicketCard";
import {calendarDate} from "../utils";

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
    const mockRoute = {
        params: {
            inboxId: 1
        }
    }
    const mockRouter = {
        push: jest.fn()
    }

    const wrapper = shallowMount(TicketCard, {
        mocks: {
            $route: mockRoute,
            $router: mockRouter
        }, propsData: {ticket: ticketData}
    });

    expect(wrapper.find("span").text()).toContain(ticketData.ticket_inbox_id);
    let headers = wrapper.findAll("h3");
    expect(headers.length).toBe(2);
    expect(headers.at(0).text()).toContain(calendarDate(ticketData.date_created));
    expect(headers.at(1).text()).toContain("Assignee:");
    expect(headers.at(1).text()).toContain(ticketData.assignee.first_name);
    expect(headers.at(1).text()).toContain(ticketData.assignee.last_name);

    expect(wrapper.find("router-link").text()).toBe(ticketData.title);

    for (let i = 0; i < ticketData.labels.length; i++) {
        expect(wrapper.find("div").html()).toContain(ticketData.labels[i].name)
    }
});

it("card content without assignee", () => {
      const mockRoute = {
        params: {
            inboxId: 1
        }
    }
    const mockRouter = {
        push: jest.fn()
    }

    ticketData.assignee = null;
    const wrapper = shallowMount(TicketCard, {        mocks: {
            $route: mockRoute,
            $router: mockRouter
        }, propsData: {ticket: ticketData}});

    let headers = wrapper.findAll("h3");
    expect(headers.length).toBe(1);
});

ticketData.labels = [];

it("card content without labels", () => {
        const mockRoute = {
        params: {
            inboxId: 1
        }
    }
    const mockRouter = {
        push: jest.fn()
    }
    const wrapper = shallowMount(TicketCard, {        mocks: {
            $route: mockRoute,
            $router: mockRouter
        },propsData: {ticket: ticketData}});

    expect(wrapper.find("div").html()).toBe("<div class=\"space-x-1 select-none\"></div>")
});

it("card content small", () => {
        const mockRoute = {
        params: {
            inboxId: 1
        }
    }
    const mockRouter = {
        push: jest.fn()
    }
    const wrapper = shallowMount(TicketCard, {
      mocks: {
        $route: mockRoute,
        $router: mockRouter
      }
    ,propsData: {ticket: ticketData, small: true}});

    expect(wrapper.find("span").text()).toBe(`#${ticketData.ticket_inbox_id}`);
    expect(wrapper.find("div").exists()).toBeFalsy()
});

