api_list = {
    "GET": {
        "/api": "显示API列表",
        '/api/get/public/list': "获取公共文件列表",
        '/api/get/pdf/list': "获取PDF文件列表",
        '/api/get/md/list': "获取Markdown文件列表",
        '/api/download/public/<string:file>': {
            "description": "下载公共文件",
            "parameters": {
                "file": "文件名"
            }
        }
    },
    "POST": {
        "/api/mdtranslate/<str:source>/<str:target>":{
            "description": "将Markdown文件中的文本翻译成指定语言",
            "parameters": {
                "source": "源语言",
                "target": "目标语言"
            },
            "response": {
                "status": "状态",
                "message": "消息"
            }
        },
        '/api/upload/<str:type>':{
            "description": "上传文件",
            "parameters": {
                "type": "文件类型"
            },
            "response": {
                "status": "状态",
                "message": "消息"
            }
        },
        '/api/sci_pdf2md':{
            "description": "将PDF文件转换为Markdown文件",
            "response": {
                "status": "状态",
                "message": "消息"
            }
        }
    },
    "DELETE": {
        '/api/delete/public/<string:file>': {
            "description": "删除公共文件",
            "parameters": {
                "file": "文件名"
            }
        },
        '/api/delete/pdf/<string:file>': {
            "description": "删除PDF文件",
            "parameters": {
                "file": "文件名"
            }
        },
        '/api/delete/md/<string:file>': {
            "description": "删除Markdown文件",
            "parameters": {
                "file": "文件名"
            }
        }
    },
    "Avaliable_languages": ["中文","英文","日文","韩文","法文","德文","俄文","西班牙文","葡萄牙文","或任何一种非小种语言"],
    "Avaliable_file_types": ["md","pdf"],
    "Avaliable_status": ["success","error"]
}