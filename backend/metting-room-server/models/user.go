package models

type User struct {
	ID     int64 `gorm:"column:id"`
	TeamID int64 `gorm:"column:team_id"`
}

func (User) TableName() string {
	return "user_user"
}
