import MeetingRoomCreateInput from '../../../../src/components/team/MeetingRoomCreateInput';
import { shallowMount } from '@vue/test-utils';

describe('MeetingRoomCreateInput.vue', () => {
    const wrapper = shallowMount(MeetingRoomCreateInput);
    it('check confirmHitMessage method', () => {
        expect(wrapper.vm.confirmHintMessage(true)).toBe(true);
        expect(wrapper.vm.confirmHintMessage(false)).toBe(false);
    });
});
