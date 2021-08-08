import { transform } from './operation';

const LoopGap = 1;

const TextHandler = function (content, version, onChange, onSend) {
    this.content = content;
    this.version = version;
    this.onChange = onChange;
    this.onSend = onSend;
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
            that.content = operation.apply(that.content);
            that.version++;
        } else if (!that.isCompositionInput && that.receiveBuffer.length) {
            const operation = that.receiveBuffer.shift();
            if (!that.waiting) {
                that.content = operation.apply(that.content);
                that.version++;
                that.onChange(that.content);
            } else if (that.waiting.equals(operation)) {
                that.waiting = null;
            } else {
                let operationPrimes = transform(that.waiting, operation);
                that.waiting = operationPrimes[0];
                that.sendBuffer.forEach((operation1) => {
                    operationPrimes = transform(operation1, operationPrimes[1]);
                });
                that.content = operationPrimes[1].apply(that.content);
                that.version++;
                that.onChange(that.content);
            }
        }
        setTimeout(() => {
            loop();
        }, LoopGap);
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
