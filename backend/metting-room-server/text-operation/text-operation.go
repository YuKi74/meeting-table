package textoperation

import "unicode/utf8"

type Operation struct {
	BaseLength   int
	TargetLength int
	Ops          []interface{}
}

func (operation *Operation) insert(op string) {
	if op == "" {
		return
	}
	operation.TargetLength += utf8.RuneCountInString(op)
	ops := operation.Ops
	if len(ops) > 0 && isInsert(ops[len(ops)-1]) {
		ops[len(ops)-1] = ops[len(ops)-1].(string) + op
	} else if len(ops) > 0 && isDelete(ops[len(ops)-1]) {
		if len(ops) > 1 && isInsert(ops[len(ops)-2]) {
			ops[len(ops)-2] = ops[len(ops)-1].(string) + op
		} else {
			ops = append(ops, ops[len(ops)-1])
			ops[len(ops)-2] = op
		}
	} else {
		ops = append(ops, op)
	}
	operation.Ops = ops
}

func (operation *Operation) delete(op int) {
	if op == 0 {
		return
	}
	if op > 0 {
		op = -op
	}
	operation.BaseLength -= op
	ops := operation.Ops
	if len(ops) > 0 && isDelete(ops[len(ops)-1]) {
		ops[len(ops)-1] = ops[len(ops)-1].(int) + op
	} else {
		ops = append(ops, op)
	}
	operation.Ops = ops
}

func (operation *Operation) retain(op int) {
	if op == 0 {
		return
	}
	operation.BaseLength += op
	operation.TargetLength += op
	ops := operation.Ops
	if len(ops) > 0 && isRetain(ops[len(ops)-1]) {
		ops[len(ops)-1] = ops[len(ops)-1].(int) + op
	} else {
		ops = append(ops, op)
	}
	operation.Ops = ops
}
