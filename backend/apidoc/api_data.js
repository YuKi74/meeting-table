define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "business-server/apidoc/main.js",
    "group": "C:\\Users\\fairy\\meeting-table\\backend\\business-server\\apidoc\\main.js",
    "groupTitle": "C:\\Users\\fairy\\meeting-table\\backend\\business-server\\apidoc\\main.js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/room/",
    "title": "创建会议室",
    "name": "create_new_room",
    "group": "Room",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[1..64]",
            "optional": false,
            "field": "name",
            "description": "<p>团队名</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Room"
  },
  {
    "type": "delete",
    "url": "/room/",
    "title": "创建人删除会议室",
    "name": "delete_room",
    "group": "Room",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>会议室id</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Room"
  },
  {
    "type": "patch",
    "url": "/room/",
    "title": "创建人编辑会议室信息",
    "name": "update_room_information",
    "group": "Room",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[1..64]",
            "optional": false,
            "field": "name",
            "description": "<p>会议室新名字</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>会议室id</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Room"
  },
  {
    "type": "get",
    "url": "/room/",
    "title": "获取会议室信息",
    "name": "update_room_information",
    "group": "Room",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "uuid",
            "description": "<p>会议室uuid</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "room_information",
            "description": "<p>会议室信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Room"
  },
  {
    "type": "post",
    "url": "/team/",
    "title": "创建团队",
    "name": "create_team",
    "group": "Team",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[1..64]",
            "optional": false,
            "field": "name",
            "description": "<p>团队名</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..255]",
            "optional": false,
            "field": "introduction",
            "description": "<p>团队介绍</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"name\":\"干完这单就回家\",\n    \"introduction\":\"这是团队介绍啊\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "delete",
    "url": "/team/",
    "title": "解散团队",
    "name": "delete_team",
    "group": "Team",
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "delete",
    "url": "/team/member/",
    "title": "团队创建者移出团队内成员",
    "name": "delete_team_member",
    "group": "Team",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "member_id",
            "description": "<p>团队成员id</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "get",
    "url": "/team/member/",
    "title": "查看用户所在团队内所有成员",
    "name": "get_all_team_members",
    "group": "Team",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "information",
            "description": "<p>团队内所有成员信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "get",
    "url": "/team/:uuid",
    "title": "获取团队信息",
    "name": "get_team_information",
    "group": "Team",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "team_information",
            "description": "<p>团队信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "get",
    "url": "/team/join/",
    "title": "团队创建者获取未处理的申请人名单",
    "name": "get_unsolved_applications",
    "group": "Team",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "unsolved_list",
            "description": "<p>未处理的申请人名单</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "post",
    "url": "/team/member/",
    "title": "团队创建者审核申请人",
    "name": "process_member_application",
    "group": "Team",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "application_id",
            "description": "<p>申请记录id</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "is_admitted",
            "description": "<p>申请是否同意</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "post",
    "url": "/team/quit/",
    "title": "用户退出团队",
    "name": "quit_team",
    "group": "Team",
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "post",
    "url": "/team/join/",
    "title": "申请人提交加入团队的申请",
    "name": "submit_application",
    "group": "Team",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "uuid",
            "description": "<p>申请团队uuid</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "patch",
    "url": "/team/",
    "title": "修改团队信息",
    "name": "update_team_information",
    "group": "Team",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[1..64]",
            "optional": true,
            "field": "name",
            "description": "<p>团队名</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..255]",
            "optional": true,
            "field": "introduction",
            "description": "<p>团队介绍</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/team/views.py",
    "groupTitle": "Team"
  },
  {
    "type": "patch",
    "url": "/user/",
    "title": "用户修改个人信息",
    "name": "update_information",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String[1..32]",
            "optional": true,
            "field": "name",
            "description": "<p>用户名</p>"
          },
          {
            "group": "Parameter",
            "type": "String[1..128]",
            "optional": true,
            "field": "password",
            "description": "<p>用户密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>后续发请求都要携带</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/",
    "title": "用户查看个人信息",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "optional": false,
            "field": "token",
            "description": "<p>发送请求时携带token</p>"
          }
        ]
      }
    },
    "name": "update_information",
    "group": "User",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "information",
            "description": "<p>用户个人信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/:id",
    "title": "用户获取其他用户信息",
    "examples": [
      {
        "title": "请求路径示例",
        "content": "http://localhost/api/user/1/",
        "type": "json"
      }
    ],
    "name": "user_information",
    "group": "User",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "user_information",
            "description": "<p>用户信息</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/user/login/",
    "title": "用户登录",
    "name": "user_login",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>用户邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>用户密码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"email\":\"test@qq.com\",\n    \"password\":\"123456\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>后续发请求都要携带</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/user/views.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/user/register/",
    "title": "用户注册",
    "name": "user_register",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>用户名</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>用户邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>用户密码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"name\":\"gan\",\n    \"email\":\"test@qq.com\",\n    \"password\":\"123456\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>后续发请求都要携带</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "business-server/user/views.py",
    "groupTitle": "User"
  }
] });
