#!flask/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request
import TencentYoutuyun

appid = '10142343'
secret_id = 'AKIDfBWfdPIOcO4d5MzL3bx7A2Unvrb9thhc'
secret_key = 'uUwFMH0Xs32YyoX5TkrnX5RbdU9d3MTO'
userid = '916956726'

end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT

app = Flask(__name__)

youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

# 创建个体，此函数小程序暂不使用
@app.route('/face/api/newstu', methods=['POST'])
def NewStu():
    '''
    - student_id: 新建的个体id，用户指定，唯一，建议为学号或身份证
	- student_name: 个体对应的姓名
	- group_ids: 数组类型，用户指定（组默认创建）的个体存放的组id，可以指定多个组id，如班级，年级，校
	- image_path: 包含个体人脸的图片路径（暂时没想好怎么解决，先用模拟）
	- tag: 备注信息，用户自解释字段（没想好干啥用）
    - data_type: 用于表示image_path是图片还是url, 0代表图片，1代表url
    '''
    #if not request.json or not 'person_id' in request.json:
    #    abort(400)
    id = request.json['student_id']
    name = request.json['student_name']
    stu_class = request.json['stu_class']
    stu_grade = request.json['stu_grade']
    stu_school = request.json['stu_school']
    groups = [stu_class, stu_grade, stu_school] # 每个传入的字段不能有空格，否则不接收
    image = './images/test1.jpeg' # 暂时模拟
    tag = request.json['tag']

    r = youtu.NewPerson(id, image, groups, name, tag, data_type=0)
    return jsonify(r)

# 删除个体
@app.route('/face/api/delstu', methods=['POST'])
def DelStu():
    '''
    根据student_id删除个体
    ------------------------------------------------
    参数：
    ------------------------------------------------
        student_id	    String	待删除个体ID
    ------------------------------------------------
    返回值：
    ------------------------------------------------
        session_id	    Int	    保留字段，目前不使用
        person_id	    String	成功删除的person_id
        deleted	        Int	    成功删除的Person数量
        errorcode	    Int	    返回状态码
        errormsg	    String	返回错误消息
    ------------------------------------------------
    '''
    id = request.json['student_id']

    r = youtu.DelPerson(id)
    return jsonify(r)

# 获取个体信息
@app.route('/face/api/getinfo', methods=['POST'])
def GetInfo():
    '''
    根据student_id获取信息
    --------------------------------------------------------
    参数：
    --------------------------------------------------------
        student_id	    String	        个体ID
    --------------------------------------------------------
    返回值：
    --------------------------------------------------------
        person_name	    String	        相应person的name
        person_id	    String	        相应person的id
        face_ids	    Array(String)	包含的人脸列表
        group_ids	    Array(String)	包含此个体的组id
        tag	            String	        用户备注信息
        session_id	    String	        保留字段，目前不使用
        errorcode	    Int	            返回状态码
        errormsg	    String	        返回错误消息
    --------------------------------------------------------
    '''
    id = request.json['student_id']

    r = youtu.GetInfo(id)
    return jsonify(r)

# 重置个体信息：新的name和tag
@app.route('/face/api/setinfo', methods=['POST'])
def SetInfo():
    '''
    重置个体的name和tag，若为空则不变
    ------------------------------------------
    参数：
    ------------------------------------------
        student_id	String	相应person的id
        person_name	String	新的name
        tag	        String	备注信息
    ------------------------------------------
    返回值：
    ------------------------------------------
        session_id	Int	    保留字段，目前不使用
        person_id	String	相应person的id
        errorcode	Int	    返回状态码
        errormsg	String	返回错误消息
    ------------------------------------------
    '''
    id = request.json['student_id']
    new_name = request.json['new_name']
    new_tag = request.json['new_tag']

    r = youtu.SetInfo(id, new_name, new_tag)
    return jsonify(r)

# 获取组列表
@app.route('/face/api/getgroupids', methods=['POST'])
def GetGroupIds():
    '''
    获取所有分组列表
    ---------------------------------------------------------
    返回值：
    ---------------------------------------------------------
        group_ids	Array(String)	相应app_id的group_id列表
        errorcode	Int	            返回状态码
        errormsg	String	        返回错误消息
    ---------------------------------------------------------
    '''
    r = youtu.GetGroupIds()
    return jsonify(r)

# 获取分组中的个体列表
@app.route('/face/api/getstuids', methods=['POST'])
def GetStuIds():
    '''
    根据group_id获取分组中的id列表
    --------------------------------------------------
    参数：
    --------------------------------------------------
        group_id	String	        组id
    --------------------------------------------------
    返回值：
    ---------------------------------------------------
        person_ids	Array(String)	相应person的id列表
        errorcode	Int	            返回状态码
        errormsg	String	        返回错误消息
    ---------------------------------------------------
    '''
    group_id = request.json['group_id']

    r = youtu.GetPersonIds(group_id)
    return jsonify(r)

# 获取一个人的人脸列表
@app.route('/face/api/getfaceids', methods=['POST'])
def GetFaceIds():
    '''
    根据student_id获取人脸列表
    -------------------------------------------------
    参数：
    -------------------------------------------------
        student_id	String	        个体id
    -------------------------------------------------
    返回值：
    -------------------------------------------------
        face_ids	Array(String)	相应face的id列表
        errorcode	Int	            返回状态码
        errormsg	String	        返回错误消息
    -------------------------------------------------
    '''
    id = request.json['student_id']

    r = youtu.GetFaceIds(id)
    return jsonify(r)

# 获取人脸信息
@app.route('/face/api/getfaceinfo', methods=['POST'])
def GetFaceInfo():
    '''
    根据face_id获取人脸信息
    ---------------------------------------------------------------------
    参数：
    ---------------------------------------------------------------------
        face_id	        String	    人脸id
    ---------------------------------------------------------------------
    返回值：
    ---------------------------------------------------------------------
        face_info	    FaceItem	人脸信息
        errorcode	    Int	        返回状态码
        errormsg	    String	    返回错误消息
    ---------------------------------------------------------------------
    FaceItem:
    ---------------------------------------------------------------------
        face_id	        String	    人脸标识
        x	            Point	    人脸框左上角x
        y	            Point	    人脸框左上角y
        width	        Float	    人脸框宽度
        height	        Float	    人脸框高度
        gender	        Int	        性别 [0/(female)~100(male)]
        age	            Int	        年龄 [0~100]
        expression	    Int	        微笑[0(normal)~50(smile)~100(laugh)]
        glass	        Bool	    是否有眼镜 [true,false]
        pitch	        Int	        上下偏移[-30,30]
        yaw	            Int	        左右偏移[-30,30]
        roll	        Int	        平面旋转[-180,180]
    ---------------------------------------------------------------------
    '''
    face_id = request.json['face_id']

    r = youtu.GetFaceInfo(face_id)
    return jsonify(r)

# 人脸识别？
@app.route('/face/api/faceidentify', methods=['POST'])
def FaceIdentify():
    '''
    此功能文档上没有，但sdk上有，疑似单一识别
    '''
    # 获取请求文件
    imgfile = request.files.get('image')
    # 获取文件名
    imgname = imgfile.filename
    #获取文件字节流
    imgfilebinary = imgfile.read()

    out_path = './images/' + imgname

    imgout = open(out_path, 'wb')
    imgout.write(imgfilebinary)
    imgout.close()

    group_id = request.form.get('group_id')

    r = youtu.FaceIdentify(group_id, out_path, data_type=0)
    print(r, "type is ", type(jsonify(r)))
    return jsonify(r)

# 多人脸检索，要是上边的不能用就用这个
@app.route('/face/api/multifaceidentify', methods=['POST'])
def MultiFaceIdentify():
    pass

# --------------------------这里改错误处理---------------------------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=2333, 
        debug = 'True'
    )