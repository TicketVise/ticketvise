import Chip from "@/elements/chip/Chip";
import {mount} from '@vue/test-utils'

test("chip has dot", () => {
  const wrapper = mount(Chip, {propsData: {background: "#FF6600"}});

  expect(wrapper.findAll("div").at(1).html()).toBe("<div class=\"w-2 h-2 rounded-full flex-col mr-1\" style=\"background-color: rgb(255, 102, 0);\"></div>")

});