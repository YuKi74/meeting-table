<template>
    <div>
        <modal title="音视频测试" :visible="isModal" @cancel="close">
            <div class="device-check-container">
                <h2>microphone</h2>
                <p>请发出声音测试音频是否正常</p>
                <div class="flex main-axis-between popContainer">
                    <popover
                        trigger="click"
                        v-model="isMicrophonePop"
                        placement="bottom"
                    >
                        <template slot="content" class="drop">
                            <div
                                v-for="(microphone, index) in microphones"
                                :key="index"
                            >
                                <a-button
                                    @click="changeMicrophone(index)"
                                    type="link"
                                    class="buttons"
                                >
                                    {{ microphone.label }}
                                </a-button>
                            </div>
                        </template>
                        <a-button icon="down">microphones</a-button>
                    </popover>
                    <span>{{ microphone }}</span>
                </div>
                <a-progress
                    :percent="testVolume"
                    size="small"
                    :showInfo="isShowInformation"
                    strokeColor="var(--primary-color-1)"
                />

                <h2>Cameras</h2>
                <p>请测试视频是否正常</p>
                <div class="flex main-axis-between popContainer">
                    <popover
                        trigger="click"
                        v-model="isCameraPop"
                        placement="bottom"
                    >
                        <template slot="content" class="drop">
                            <div
                                v-for="(camera, index) in cameras"
                                :key="index"
                            >
                                <a-button
                                    @click="changeCamera(index)"
                                    type="link"
                                    class="buttons"
                                >
                                    {{ camera.label }}
                                </a-button>
                            </div>
                        </template>
                        <a-button icon="down">cameras</a-button>
                    </popover>
                    <span>{{ camera }}</span>
                </div>
                <div id="pre-local-player" class="test"></div>
            </div>
            <template slot="footer">
                <a-button @click="join(false)">关闭摄像头及麦克风进入</a-button>
                <a-button @click="join(true)">进入会议室</a-button>
            </template>
        </modal>

        <div class="flex">
            <a-button
                @click="changeCameraStatus"
                icon="video-camera"
                :class="[isOpenCamera ? 'open' : 'close']"
                v-show="isStartVideo"
            >
            </a-button>
            <a-button
                @click="changeMicrophoneStatus"
                icon="audio"
                :class="[isOpenMicrophone ? 'open' : 'close']"
                v-show="isStartVideo"
            >
            </a-button>
            <a-button @click="leave" v-show="isStartVideo"> 离开 </a-button>
            <a-button @click="startTest" v-show="!isStartVideo"
                >加入音视频会议</a-button
            >
        </div>

        <div
            v-for="(item, index) in users"
            :key="index"
            ref="players"
            v-show="isStartVideo"
        >
            <div class="player" :id="item"></div>
        </div>
    </div>
</template>

<script>
import AgoraRTC from 'agora-rtc-sdk-ng';
import { Modal, Button, Popover, Progress, notification } from 'ant-design-vue';
import { HUNDRED } from '../../constants/meeting-room';
import Vue from 'vue';

Vue.use(Modal);

export default {
    props: ['userId', 'roomUuid', 'token'],
    components: {
        Modal,
        AButton: Button,
        Popover,
        AProgress: Progress,
    },
    data() {
        return {
            rtc: {
                client: null,
                localAudioTrack: null,
                localVideoTrack: null,
            },
            options: {
                appId: '52a942a5595e46d78af3ef7f60a8766d',
                channel: this.roomUuid,
                token: this.token,
            },
            users: [],
            microphones: [],
            cameras: [],
            microphone: null,
            camera: null,
            isOpenCamera: false,
            isOpenMicrophone: false,
            isModal: false,
            isCameraPop: false,
            isMicrophonePop: false,
            testVolume: 0,
            isShowInformation: false,
            interval: null,
            isStartVideo: false,
        };
    },
    methods: {
        startTest() {
            this.isModal = true;
            AgoraRTC.getDevices()
                .then((devices) => {
                    this.microphones = devices.filter(function (device) {
                        return device.kind === 'audioinput';
                    });
                    this.cameras = devices.filter(function (device) {
                        return device.kind === 'videoinput';
                    });
                    let selectedMicrophoneId = this.microphones[0].deviceId;
                    this.microphone = this.microphones[0].label;
                    let selectedCameraId = this.cameras[0].deviceId;
                    this.camera = this.cameras[0].label;
                    return Promise.all([
                        AgoraRTC.createCameraVideoTrack({
                            cameraId: selectedCameraId,
                        }),
                        AgoraRTC.createMicrophoneAudioTrack({
                            microphoneId: selectedMicrophoneId,
                        }),
                    ]);
                })
                .then(([videoTrack, audioTrack]) => {
                    this.rtc.localAudioTrack = audioTrack;
                    this.rtc.localVideoTrack = videoTrack;
                    setTimeout(() => {
                        videoTrack.play('pre-local-player');
                    }, 0);
                    this.interval = setInterval(() => {
                        this.getVol(this.rtc.localAudioTrack);
                    }, 0);
                });
        },
        getVol(audioTrack) {
            this.testVolume = audioTrack.getVolumeLevel() * HUNDRED;
        },
        start: async function () {
            this.rtc.client = AgoraRTC.createClient({
                mode: 'rtc',
                codec: 'vp8',
            });
            this.rtc.client.on('user-published', async (user, mediaType) => {
                await this.rtc.client.subscribe(user, mediaType);
                if (mediaType === 'video') {
                    const remoteVideoTrack = user.videoTrack;
                    this.users.append(user.uid);
                    remoteVideoTrack.play(user.uid);
                }
                if (mediaType === 'audio') {
                    const remoteAudioTrack = user.audioTrack;
                    remoteAudioTrack.play();
                }
            });
            this.rtc.client.on('user-unpublished', (user, mediaType) => {
                if (mediaType === 'video') {
                    const userIndex = this.users.indexOf(user.uid);
                    this.users = this.users
                        .slice(0, userIndex)
                        .concat(this.users.slice(userIndex + 1));
                }
                // audio不用处理？
            });
            await this.rtc.client.join(
                this.options.appId,
                this.options.channel,
                this.options.token,
                this.userId
            );
            await this.rtc.client.publish([
                this.rtc.localAudioTrack,
                this.rtc.localVideoTrack,
            ]);
            setTimeout(() => {
                this.rtc.localAudioTrack.play();
                this.rtc.localVideoTrack.play(this.userId);
            }, 0);
        },
        leave: async function () {
            if (this.isOpenMicrophone) this.rtc.localAudioTrack.close();
            if (this.isOpenCamera) this.rtc.localVideoTrack.close();
            await this.rtc.client.leave();
            this.users.length = 0;
            notification.open({
                message: '您已离开视频会议',
            });
            this.isStartVideo = false;
            this.isOpenCamera = false;
            this.isOpenMicrophone = false;
        },
        changeMicrophone: async function (index) {
            this.rtc.localAudioTrack =
                await AgoraRTC.createMicrophoneAudioTrack({
                    microphoneId: this.microphones[index].deviceId,
                });
            this.microphone = this.microphones[index].label;
            this.isMicrophonePop = false;
        },
        changeCamera: async function (index) {
            this.rtc.localVideoTrack = await AgoraRTC.createCameraVideoTrack({
                cameraId: this.cameras[index].deviceId,
            });
            this.camera = this.cameras[index].label;
            this.isCameraPop = false;
        },
        join: async function (isOpen) {
            this.start();
            if (isOpen === true) {
                this.users.unshift(this.userId);
            } else {
                this.rtc.localAudioTrack.close();
                this.rtc.localVideoTrack.close();
            }
            this.isOpenCamera = isOpen;
            this.isOpenMicrophone = isOpen;
            this.isStartVideo = true;
            this.isModal = false;
            clearInterval(this.interval);
            document.getElementById('pre-local-player').innerHTML = '';
        },
        changeCameraStatus: async function () {
            if (this.isOpenCamera === true) {
                this.isOpenCamera = false;
                this.rtc.localVideoTrack.close();
                const userIndex = this.users.indexOf(this.userId);
                this.users = this.users
                    .slice(0, userIndex)
                    .concat(this.users.slice(userIndex + 1));
                notification.open({
                    message: '您已关闭视频',
                });
            } else {
                this.isOpenCamera = true;
                this.users.unshift(this.userId);
                this.rtc.localVideoTrack =
                    await AgoraRTC.createCameraVideoTrack();
                setTimeout(() => {
                    this.rtc.localVideoTrack.play(this.userId);
                }, 0);
                notification.open({
                    message: '您已开启视频',
                });
            }
        },
        changeMicrophoneStatus: async function () {
            if (this.isOpenMicrophone === true) {
                this.isOpenMicrophone = false;
                this.rtc.localAudioTrack.close();
                notification.open({
                    message: '您已关闭音频',
                });
            } else {
                this.isOpenMicrophone = true;
                this.rtc.localAudioTrack =
                    await AgoraRTC.createMicrophoneAudioTrack();
                this.rtc.localAudioTrack.play();
                notification.open({
                    message: '您已开启音频',
                });
            }
        },
        close() {
            this.isModal = false;
            this.rtc.localAudioTrack.close();
            this.rtc.localVideoTrack.close();
            document.getElementById('pre-local-player').innerHTML = '';
        },
    },
};
</script>
<style scoped>
.player {
    width: 127px;
    height: 127px;
}
.device-check-container {
    width: 100%;
    height: 100%;
}
.test {
    width: 200px;
    height: 200px;
    margin: 20px 20px 20px 0;
}
.drop {
    background-color: var(--white);
}
.buttons {
    color: var(--black);
}
.popContainer {
    width: 100%;
}
.ant-modal-content {
    height: 500px;
}
.open {
    color: var(--primary-color-1);
}
.close {
    color: red;
}
</style>
