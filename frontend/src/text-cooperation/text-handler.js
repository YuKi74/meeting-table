import { transform } from './operation';

const TextHandler = function (version, onChange, onSend, setReadOnly) {
    this.version = version;
    this.onChange = onChange;
    this.onSend = onSend;
    this.setReadOnly = setReadOnly;
    this.sendBuffer = [];
    this.receiveBuffer = [];
    this.waiting = null;
    this.closed = false;
    this.isCompositionInput = false;
};

TextHandler.prototype.start = async function () {
    const that = this;
    const loop = function () {
        if (that.closed) {
            return;
        }
        if (!that.waiting && that.sendBuffer.length) {
            const operation = that.sendBuffer.shift();
            that.onSend({
                version: that.version,
                operation: operation,
            });
            that.waiting = operation;
            that.version++;
        } else if (!that.isCompositionInput && that.receiveBuffer.length) {
            const operation = that.receiveBuffer.shift();
            if (!that.waiting) {
                that.version++;
                if (that.setReadOnly) {
                    that.setReadOnly();
                }
                that.onChange(operation);
            } else if (that.waiting.equals(operation)) {
                that.waiting = null;
            } else {
                let operationPrimes = transform(that.waiting, operation);
                that.waiting = operationPrimes[0];
                that.sendBuffer.forEach((operation1, index) => {
                    operationPrimes = transform(operation1, operationPrimes[1]);
                    that.sendBuffer[index] = operationPrimes[0];
                });
                that.version++;
                if (that.setReadOnly) {
                    that.setReadOnly();
                }
                that.onChange(operationPrimes[1]);
            }
        }
        // 由于JavaScript是单线程语言(对用户开放的部分)，无限循环会阻塞用户界面。
        // 不断将function推到任务队列中，让其自行争抢时间片，实现接近协程的效果。
        setTimeout(() => {
            loop();
        }, 0);
    };
    loop();
};

TextHandler.prototype.close = function () {
    this.closed = true;
};

TextHandler.prototype.startCompositionInput = function () {
    this.isCompositionInput = true;
};

TextHandler.prototype.finishCompositionInput = function () {
    this.isCompositionInput = false;
};

export default TextHandler;
