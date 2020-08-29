import SearchBar from "@/elements/SearchBar";
import {mount} from '@vue/test-utils'

test("search value emit", () => {
  const wrapper = mount(SearchBar);

  const input = wrapper.find("input");

  input.element.value = "query";
  input.trigger("input");

  expect(wrapper.vm.search).toBe("query");
});