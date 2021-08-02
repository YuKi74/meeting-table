package models

type MeetingRoom struct {
	ID     int64 `gorm:"column:id"`
	TeamID int64 `gorm:"column:team_id"`
}

func (MeetingRoom) TableName() string {
	return "team_meetingroom"
}
