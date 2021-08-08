package textoperation

import (
	"errors"
)

func Transform(operation1, operation2 Operation) (operation1Prime, operation2Prime Operation, err error) {
	if operation1.BaseLength != operation2.BaseLength {
		err = errors.New("输入的两个Operation的初始长度必须相同")
		return
	}
	operation1Prime = Operation{
		BaseLength:   0,
		TargetLength: 0,
		Ops:          make([]interface{}, 0),
	}
	operation2Prime = Operation{
		BaseLength:   0,
		TargetLength: 0,
		Ops:          make([]interface{}, 0),
	}
	ops1, ops2 := operation1.Ops, operation2.Ops
	ops1 = append(ops1, nil)
	ops2 = append(ops2, nil)
	i1, i2 := 0, 0
	op1, op2 := ops1[i1], ops2[i2]
	i1++
	i2++
	for op1 != nil || op2 != nil {

		if isInsert(op1) {
			str := op1.(string)
			operation1Prime.insert(str)
			operation2Prime.retain(len(str))
			op1 = ops1[i1]
			i1++
			continue
		}
		if isInsert(op2) {
			str := op2.(string)
			operation1Prime.retain(len(str))
			operation2Prime.insert(str)
			op2 = ops2[i2]
			i2++
			continue
		}

		if op1 == nil {
			err = errors.New("客户端传来的Operation太短")
			return
		}

		if op2 == nil {
			err = errors.New("客户端传来的Operation太长")
			return
		}

		var minl int
		n1, n2 := parseInt(op1), parseInt(op2)
		if isRetain(op1) && isRetain(op2) {
			if n1 > n2 {
				minl = n2
				op1 = n1 - n2
				op2 = ops2[i2]
				i2++
			} else if n1 == n2 {
				minl = n2
				op1, op2 = ops1[i1], ops2[i2]
				i1++
				i2++
			} else {
				minl = n1
				op2 = n2 - n1
				op1 = ops1[i1]
				i1++
			}
			operation1Prime.retain(minl)
			operation2Prime.retain(minl)
		} else if isDelete(op1) && isDelete(op2) {
			if -n1 > -n2 {
				op1 = n1 - n2
				op2 = ops2[i2]
				i2++
			} else if n1 == n2 {
				op1, op2 = ops1[i1], ops2[i2]
				i1++
				i2++
			} else {
				op2 = n2 - n1
				op1 = ops1[i1]
				i1++
			}
		} else if isDelete(op1) && isRetain(op2) {
			if -n1 > n2 {
				minl = n2
				op1 = n1 + n2
				op2 = ops2[i2]
				i2++
			} else if -n1 == n2 {
				minl = n2
				op1, op2 = ops1[i1], ops2[i2]
				i1++
				i2++
			} else {
				minl = -n1
				op2 = n1 + n2
				op1 = ops1[i1]
				i1++
			}
			operation1Prime.delete(minl)
		} else if isRetain(op1) && isDelete(op2) {
			if n1 > -n2 {
				minl = -n2
				op1 = n1 + n2
				op2 = ops2[i2]
				i2++
			} else if n1 == -n2 {
				minl = n1
				op1, op2 = ops1[i1], ops2[i2]
				i1++
				i2++
			} else {
				minl = n1
				op2 = n1 + n2
				op1 = ops1[i1]
				i1++
			}
			operation2Prime.delete(minl)
		} else {
			err = errors.New("这两个操作无法兼容")
			return
		}
	}
	return
}

func isInsert(op interface{}) bool {
	_, ok := op.(string)
	return ok
}

func isRetain(op interface{}) bool {
	if value, ok := op.(int); ok {
		return value > 0
	}
	if value, ok := op.(float64); ok {
		return value > 0
	}
	return false
}

func isDelete(op interface{}) bool {
	if value, ok := op.(int); ok {
		return value < 0
	}
	if value, ok := op.(float64); ok {
		return value < 0
	}
	return false
}

func (operation *Operation) Apply(content string) (newContent string) {
	newContent = ""
	strIndex := 0
	for _, op := range operation.Ops {
		if isRetain(op) {
			n := parseInt(op)
			newContent += content[strIndex : strIndex+n]
			strIndex += n
		} else if isInsert(op) {
			newContent += op.(string)
		} else {
			strIndex -= parseInt(op)
		}
	}
	return
}

func parseInt(value interface{}) int {
	if v, ok := value.(int); ok {
		return v
	}
	v := value.(float64)
	return int(v)
}
