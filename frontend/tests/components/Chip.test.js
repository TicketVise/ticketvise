import Chip from "@/elements/chip/Chip";
import {mount} from '@vue/test-utils'

const source = "../../backend/ticketvise/static/img/avatars/default-avatar.png";

test("avatar is square", () => {
  const wrapper = mount(Avatar, {propsData: {source: source}});

});