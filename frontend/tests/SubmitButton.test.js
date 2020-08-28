import SubmitButton from "../components/elements/buttons/SubmitButton";
import {mount} from '@vue/test-utils'

test("submits click event on click", async () => {
  const button = mount(SubmitButton);
  await button.trigger("click");

  expect(button.emitted().click).toBeTruthy()
});