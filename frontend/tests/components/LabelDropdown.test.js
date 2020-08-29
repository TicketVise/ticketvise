import LabelDropdown from "@/elements/dropdown/LabelDropdown";
import {shallowMount} from '@vue/test-utils'

const labelsData = [
  {"name": "SWEBOK", "color": "#ff0000", "id": 4},
  {"name": "Individual Report", "color": "#29ff00", "id": 5},
  {"name": "Lecture", "color": "#0090ff", "id": 6},
  {"name": "E-Journal", "color": "#fbf06d", "id": 7},
  {"name": "Laptop", "color": "#150a1a", "id": 8},
  {"name": "Assignment", "color": "#00ffcd", "id": 9}
];

const selected = [
  {"name": "E-Journal", "color": "#fbf06d", "id": 7},
  {"name": "Laptop", "color": "#150a1a", "id": 8}
];

test("Labeldropdown displays data and opens", async () => {
  const wrapper = shallowMount(LabelDropdown, {
    propsData: {values: labelsData, selected: selected},
    data() {
      return {open: false}
    }
  });

  const title = wrapper.find("span");

  expect(title.html()).toContain("Select labels");
  expect(wrapper.find("ul").exists()).toBeFalsy();

  // Check if opening the dropdown shows the items
  await title.trigger("click");
  await wrapper.vm.$nextTick();

  let options = wrapper.findAll("li");

  expect(options.length).toBe(labelsData.length);
  let option = options.at(0);

  // Test label attributes
  expect(option.text()).toContain(labelsData[0].name);
  expect(option.html()).toContain("class=\"w-2 h-2 rounded-full\" style=\"background-color: rgb(255, 0, 0)");
});

test("Labeldropdown adds and removes labels on click", async () => {
  const wrapper = shallowMount(LabelDropdown, {
    propsData: {values: labelsData, selected: selected},
    data() {
      return {open: true}
    }
  });
  let options = wrapper.findAll("li");
  let option = options.at(0);

  // Check click adds from list and emits
  await option.trigger("click");
  await wrapper.vm.$nextTick();

  expect(selected).toContain(labelsData[0]);
  expect(selected.length).toBe(3);
  expect(wrapper.emitted().input).toBeTruthy();

  // Test selected label attributes
  expect(option.html()).toContain("font-semibold");
  expect(option.html()).toContain("svg");

  // Check click removes from list and emits
  await option.trigger("click");
  await wrapper.vm.$nextTick();

  expect(selected.length).toBe(2);
  expect(wrapper.emitted().input).toBeTruthy();

});