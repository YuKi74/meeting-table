/* eslint-disable no-magic-numbers */
import Doc from '../../../../src/components/meeting-room/Doc';
import { shallowMount } from '@vue/test-utils';

describe('Doc.vue', () => {
    const wrapper = shallowMount(Doc, {
        propsData: {
            content: {
                content: null,
                version: 0,
            },
            connection: {
                send: function () {},
                addMessageHandler: function () {},
            },
        },
    });
    it('check getOps method', () => {
        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        expect(wrapper.vm.getOps('a', 1, 1, 'insertText', 'a')).toStrictEqual([
            0,
            'a',
            0,
            0,
        ]);

        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        expect(wrapper.vm.getOps('\n', 1, 1, 'insertText', null)).toStrictEqual(
            [0, '\n', 0, 0]
        );

        wrapper.vm.lastValue = 'a';
        wrapper.vm.lastLength = 1;
        expect(wrapper.vm.getOps('', 0, 0, 'delete', null)).toStrictEqual([
            0,
            '',
            -1,
            0,
        ]);

        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        wrapper.vm.clipboardData = '';
        expect(wrapper.vm.getOps('', 0, 0, 'insertFromPaste', null)).toBe(null);

        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        wrapper.vm.clipboardData = 'a';
        expect(
            wrapper.vm.getOps('a', 1, 1, 'insertFromPaste', null)
        ).toStrictEqual([0, 'a', 0, 0]);

        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        expect(
            wrapper.vm.getOps('你', 1, 1, 'insertCompositionText', '你')
        ).toStrictEqual([0, '你', 0, 0]);

        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        expect(wrapper.vm.getOps('', 0, 0, 'insertCompositionText', null)).toBe(
            null
        );

        wrapper.vm.lastValue = '';
        wrapper.vm.lastLength = 0;
        expect(wrapper.vm.getOps('', 0, 0, 'insert', null)).toBe(null);
    });
});
