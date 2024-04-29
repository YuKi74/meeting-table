const Operation = function (baseLength, targetLength, ops) {
    this.Ops = ops ? ops : [];
    this.BaseLength = baseLength ? baseLength : 0;
    this.TargetLength = targetLength ? targetLength : 0;
};

Operation.prototype.equals = function (other) {
    if (this.BaseLength !== other.BaseLength) {
        return false;
    }
    if (this.TargetLength !== other.TargetLength) {
        return false;
    }
    if (this.Ops.length !== other.Ops.length) {
        return false;
    }
    for (let i = 0; i < this.Ops.length; i++) {
        if (this.Ops[i] !== other.Ops[i]) {
            return false;
        }
    }
    return true;
};

const isRetain = function (op) {
    return typeof op === 'number' && op > 0;
};

const isInsert = function (op) {
    return typeof op === 'string';
};

const isDelete = function (op) {
    return typeof op === 'number' && op < 0;
};

Operation.prototype.retain = function (n) {
    if (n === 0) {
        return this;
    }
    this.BaseLength += n;
    this.TargetLength += n;
    if (isRetain(this.Ops[this.Ops.length - 1])) {
        this.Ops[this.Ops.length - 1] += n;
    } else {
        this.Ops.push(n);
    }
    return this;
};

Operation.prototype.insert = function (str) {
    if (str === '') {
        return this;
    }
    this.TargetLength += str.length;
    let ops = this.Ops;
    if (isInsert(ops[ops.length - 1])) {
        ops[ops.length - 1] += str;
    } else if (isDelete(ops[ops.length - 1])) {
        if (isInsert(ops[ops.length - 2])) {
            ops[ops.length - 2] += str;
        } else {
            ops[ops.length] = ops[ops.length - 1];
            ops[ops.length - 2] = str;
        }
    } else {
        ops.push(str);
    }
    return this;
};

Operation.prototype['delete'] = function (n) {
    if (n === 0) {
        return this;
    }
    if (n > 0) {
        n = -n;
    }
    this.BaseLength -= n;
    if (isDelete(this.Ops[this.Ops.length - 1])) {
        this.Ops[this.Ops.length - 1] += n;
    } else {
        this.Ops.push(n);
    }
    return this;
};

Operation.prototype.apply = function (str, oldOffset) {
    let newStr = [];
    let j = 0;
    let strIndex = 0;
    const ops = this.Ops;
    for (let i = 0, l = ops.length; i < l; i++) {
        let op = ops[i];
        if (isRetain(op)) {
            newStr[j++] = str.slice(strIndex, strIndex + op);
            strIndex += op;
        } else if (isInsert(op)) {
            newStr[j++] = op;
        } else {
            strIndex -= op;
        }
    }
    strIndex = 0;
    let newOffset = 0;
    for (let i = 0, l = ops.length; i < l; i++) {
        let op = ops[i];
        if (isRetain(op)) {
            strIndex += op;
            if (strIndex > oldOffset) {
                newOffset += oldOffset - (strIndex - op);
                break;
            } else {
                newOffset += op;
            }
        } else if (isDelete(op)) {
            strIndex -= op;
            if (strIndex > oldOffset) {
                break;
            }
        } else if (isInsert(op)) {
            newOffset += op.length;
        } else {
            throw new Error('未知operation: ' + JSON.stringify(op));
        }
    }
    return [newStr.join(''), newOffset];
};

const transform = function (operation1, operation2) {
    if (operation1.baseLength !== operation2.baseLength) {
        throw new Error('两个operation起点不一致');
    }

    let operation1prime = new Operation();
    let operation2prime = new Operation();
    let ops1 = operation1.Ops,
        ops2 = operation2.Ops;
    let i1 = 0,
        i2 = 0;
    let op1 = ops1[i1++],
        op2 = ops2[i2++];
    for (;;) {
        if (typeof op1 === 'undefined' && typeof op2 === 'undefined') {
            break;
        }
        if (isInsert(op1)) {
            operation1prime.insert(op1);
            operation2prime.retain(op1.length);
            op1 = ops1[i1++];
            continue;
        }
        if (isInsert(op2)) {
            operation1prime.retain(op2.length);
            operation2prime.insert(op2);
            op2 = ops2[i2++];
            continue;
        }

        if (typeof op1 === 'undefined') {
            throw new Error('两个operation不匹配,第一个Operation太短。');
        }
        if (typeof op2 === 'undefined') {
            throw new Error('两个operation不匹配,第一个Operation太长。');
        }

        let minl;
        if (isRetain(op1) && isRetain(op2)) {
            if (op1 > op2) {
                minl = op2;
                op1 = op1 - op2;
                op2 = ops2[i2++];
            } else if (op1 === op2) {
                minl = op2;
                op1 = ops1[i1++];
                op2 = ops2[i2++];
            } else {
                minl = op1;
                op2 = op2 - op1;
                op1 = ops1[i1++];
            }
            operation1prime.retain(minl);
            operation2prime.retain(minl);
        } else if (isDelete(op1) && isDelete(op2)) {
            if (-op1 > -op2) {
                op1 = op1 - op2;
                op2 = ops2[i2++];
            } else if (op1 === op2) {
                op1 = ops1[i1++];
                op2 = ops2[i2++];
            } else {
                op2 = op2 - op1;
                op1 = ops1[i1++];
            }
        } else if (isDelete(op1) && isRetain(op2)) {
            if (-op1 > op2) {
                minl = op2;
                op1 = op1 + op2;
                op2 = ops2[i2++];
            } else if (-op1 === op2) {
                minl = op2;
                op1 = ops1[i1++];
                op2 = ops2[i2++];
            } else {
                minl = -op1;
                op2 = op2 + op1;
                op1 = ops1[i1++];
            }
            operation1prime['delete'](minl);
        } else if (isRetain(op1) && isDelete(op2)) {
            if (op1 > -op2) {
                minl = -op2;
                op1 = op1 + op2;
                op2 = ops2[i2++];
            } else if (op1 === -op2) {
                minl = op1;
                op1 = ops1[i1++];
                op2 = ops2[i2++];
            } else {
                minl = op1;
                op2 = op2 + op1;
                op1 = ops1[i1++];
            }
            operation2prime['delete'](minl);
        }
    }

    return [operation1prime, operation2prime];
};

const regular = function (ops) {
    let o = new Operation();
    for (let i = 0, l = ops.length; i < l; i++) {
        let op = ops[i];
        if (op === 0) {
            continue;
        }
        if (isRetain(op)) {
            o.retain(op);
        } else if (isInsert(op)) {
            o.insert(op);
        } else if (isDelete(op)) {
            o['delete'](op);
        } else {
            throw new Error('未知operation: ' + JSON.stringify(op));
        }
    }
    return o;
};

export default Operation;
export { transform, regular };
