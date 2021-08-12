import TeamDetail from '../../../../src/components/team/TeamDetail';
import { shallowMount } from '@vue/test-utils';

describe('TeamDetail.vue', () => {
    const wrapper = shallowMount(TeamDetail);
    it('test provideTitleAndMessage method', () => {
        expect(wrapper.vm.provideTitleAndMessage(true)).toStrictEqual({
            title: '确定要解散团队吗',
            message: '解散后不可恢复，且所有会议室文件都会丢失',
        });
        expect(wrapper.vm.provideTitleAndMessage(false)).toStrictEqual({
            title: '确定要退出团队吗',
            message: '',
        });
    });
    it('test showModal and handleCancel methods', () => {
        wrapper.vm.showModal();
        expect(wrapper.vm.visible).toBe(true);
        wrapper.vm.handleCancel();
        expect(wrapper.vm.visible).toBe(false);
        wrapper.vm.showModal();
        expect(wrapper.vm.visible).toBe(true);
    });
});
