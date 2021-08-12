import Chat from '../../../../src/components/meeting-room/Chat';
import { shallowMount } from '@vue/test-utils';

describe('Chat.vue', () => {
    const wrapper = shallowMount(Chat, {
        propsData: {
            content: '',
        },
    });
    it('check setPopContent', () => {
        wrapper.vm.setPopContent(true);
        expect(wrapper.vm.popContent).toBe('消息发送成功');
        wrapper.vm.setPopContent(false);
        expect(wrapper.vm.popContent).toBe('您有新的消息');
    });
});
