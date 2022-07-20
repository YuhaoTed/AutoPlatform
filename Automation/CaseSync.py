def Get_Val(case_detail,key,step):
    if not (key + str(step)) in case_detail.keys():
        return None
    if case_detail[key + str(step)]==None:
        return None
    else:
        return int(case_detail[key + str(step)])



def CaseCreate(case_detail,step_num,case_id,filename,casename):
    #
    # 先生成一个文件存储简单的内容
    msg = {}
    print(case_detail.keys())
    with open(filename, 'w+') as f:
        step = 1

        #添加函数名
        f.write('class Unit_'+casename+':')
        while step <= int(step_num):
            # 开始编写文件
            step_msg = []
            manu_val = Get_Val(case_detail,'manu_sel_',step)
            rec_val = Get_Val(case_detail,'rec_sel_',step)
            mid_val = Get_Val(case_detail,'mid_sel_',step)
            mid_comp = Get_Val(case_detail,'mid_comp_',step)

            if Get_Val(case_detail,'loop_type_',step)==2:
                #等待until
                UntilPrep(f,'\t')
                if manu_val>0:
                    ret = manu(f, case_detail, step,manu_val,'\t\t')
                    step_msg.append(ret)
                if mid_val > 0:
                    ret = mid(f, case_detail, step, mid_val,'\t\t')
                    step_msg.append(ret)
                # 判断检测值
                if rec_val > 0:
                    ret = rec_until(f, case_detail, step, rec_val,'\t\t')
                    step_msg.append(ret)
                if mid_comp > 0:
                    ret = comp_until(f, case_detail, step, mid_comp,'\t\t')
                    step_msg.append(ret)
                UntilEnd(f,'\t')
            else:
                # 不存在循环
                # 判断操作值
                if manu_val>0:
                    ret = manu(f, case_detail, step,manu_val,'\t')
                    step_msg.append(ret)
                # 判断检测值
                if rec_val>0:
                    ret = rec(f, case_detail, step, rec_val,'\t')
                    step_msg.append(ret)
                if mid_val>0:
                    ret = mid(f, case_detail, step, mid_val,'\t')
                    step_msg.append(ret)
                if mid_comp > 0:
                    ret = comp(f, case_detail, step, mid_comp,'\t')
                    step_msg.append(ret)
            step += 1

def UntilPrep(f,pretext=''):
    f.write(pretext+'tmp = 0\n')
    f.write(pretext+'ret = True\n')
    f.write(pretext+'while tmp<20 and ret:\n')
    pass

def UntilEnd(f,pretext=''):
    f.write(pretext + '\ttmp+=1\n')
    f.write(pretext + '\ttime.sleep(1)\n')
    f.write(pretext + 'self.assertFalse(ret)\n')
    pass

def manu_slide(f, start_x, start_y, end_x, end_y,pretext=''):
    # 判断坐标值是否合法
    if start_x > 0 and start_y > 0 and end_x>0 and end_y>0:
        f.write(pretext+'Test_Util1.Touch.Slide(%d,%d,%d,%d)\n' % (start_x, start_y,end_x,end_y))
        return '点击操作同步'
    else:
        return '点击操作同步失败'


def manu_enterapp(f, app_name,pretext=''):
    if app_name != None:
        f.write(pretext+'Test_Util1.Enter_app(%s)\n' % (app_name))
        return '进入应用操作同步'
    else:
        return '进入应用操作同步失败'


def manu_menu(f,pretext=''):
    f.write(pretext+'Test_Util1.Touch.Touch_main()\n')
    return '进入应用操作同步'


def manu_wait(f, wait_second,pretext=''):
    if wait_second >0:
        f.write(pretext+'time.sleep(%d)\n' % (wait_second))
        return '等待操作同步成功'
    else:
        return '等待操作同步失败'


def manu_sds(f, sds,pretext=''):
    if sds != None:
        sds_content = '/SDS/'+sds.split('-')[1]+'.m4a'
        f.write(pretext+'Test_Util1.Play_SDS(%s)\n' % (sds_content))
        return '语音操作同步'
    else:
        return '语音应用操作同步失败'


def manu_pos_text(f, pos_text,pretext=''):
    '''
    点击文字位置
    '''
    if pos_text!=None:
        f.write(pretext+'ret,msg=Test_Util1.Point_Word(%s.split(\'/\'))\n'%(pos_text))
        return '点击文字同步'
    else:
        return '点击文字同步失败'


def manu_pos_icon(f, pos_icon,pretext=''):
    '''
    点击图片位置
    :param f:
    :param pos_icon: 图标位置
    :return:操作结果
    '''
    if pos_icon != None:
        f.write(pretext+"ret,msg=Test_Util1.Point_Icon(/%s)\n" % (pos_icon.split('-')[1]))
        return '点击模板同步'
    else:
        return '点击模板同步失败'


def manu(f,case_detail,step,manu_val,pretext = ''):
    if manu_val == 1:
        '''选择的是点击坐标'''
        point_x = int(case_detail['point_x_' + str(step)])
        point_y = int(case_detail['point_y_' + str(step)])
        ret = manu_touch(f, point_x, point_y,pretext)
        return ret
    if manu_val==2:
        '''滑动坐标'''
        start_x = int(case_detail['start_x_' + str(step)])
        start_y = int(case_detail['start_y_' + str(step)])
        end_x = int(case_detail['end_x_' + str(step)])
        end_y = int(case_detail['end_y_' + str(step)])
        ret = manu_slide(f, start_x, start_y,end_x,end_y,pretext)
        return ret
    if manu_val==4:
        ''' enter app'''
        app_name = case_detail['appname_' + str(step)]
        ret = manu_enterapp(f,app_name,pretext)
        return ret
    if manu_val==3:
        '''点击Menu'''
        ret = manu_menu(f,pretext)
        return ret
    if manu_val==6:
        '''等待xx s'''
        wait_second = int(case_detail['wait' + str(step)])
        ret = manu_wait(f, wait_second,pretext)
        return ret
    if manu_val==5:
        '''sds操作'''
        sds = case_detail['sds_' + str(step)]
        ret = manu_sds(f, sds,pretext)
        return ret
    if manu_val==7:
        '''点击文字位置/图片位置'''
        kind = case_detail['manu_pos_kind_' + str(step)]
        if kind==1:
            #文字位置
            pos_text = case_detail['manu_pos_text_' + str(step)]
            ret = manu_pos_text(f, pos_text,pretext)
        else:
            #图片位置
            
            pos_icon = case_detail['manu_pos_text_' + str(step)]
            ret = manu_pos_icon(f, pos_icon,pretext)
            
        
        return ret

def manu_touch(f,point_x,point_y,pretext=''):

    # 判断坐标值是否合法
    if point_x > 0 and point_y > 0:
        f.write(pretext+'Test_Util1.Touch.Send_Touch_Command(%d,%d)\n' % (point_x, point_y))
        return '点击操作同步'
    else:
        return '点击操作同步失败'


def rec_text(f, left_x, left_y, right_x, right_y, contain, text, pretext):
    if text==None:
        return '识别文字失败'
    else:
        if left_x>0 and left_y>0 and right_x>0 and right_y>0:
            #固定区域识别
            text_ret = text.split('/')
            area = '[['+str(left_x)+','+str(left_y)+'],['+str(right_x)+','+str(right_y)+']]'

            if contain=='1':
                f.write(pretext+'self.assertIsNotNone(Test_Util1.Find_Word(%s,%s))\n'%(text_ret,area))
            else:
                f.write(pretext + 'self.assertIsNone(Test_Util1.Find_Word(%s,%s))\n' % (text_ret, area))
        elif (left_x==None and left_y==None and right_x==None and right_y==None) or (left_x==0 and left_y==0 and right_x==0 and right_y==0):
            #全图识别
            text_ret = text.split('/')

            if contain == '1':
                f.write(pretext + 'self.assertIsNotNone(Test_Util1.Find_Word(%s))\n' % (text_ret))
            else:
                f.write(pretext + 'self.assertIsNone(Test_Util1.Find_Word(%s))\n' % (text_ret))
        return '识别文字成功'


def rec_icon(f, contain, icon, pretext):
    if contain=='1':
        icon_ret = icon.split('-')[1]
        f.write(pretext+'self.assertIsNotNone(Test_Util1.Pic.Pic_Icon(/%s))\n'%(icon_ret))
    else:
        icon_ret = icon.split('-')[1]
        f.write(pretext + 'self.assertIsNone(Test_Util1.Pic.Pic_Icon(/%s))\n' % (icon_ret))
    return '识别图标成功'


def rec_QR(f, pretext):
    f.write(pretext + 'self.assertTrue(Test_Util1.Pic.Find_QR())\n')
    return '识别二维码成功'


def rec_POPUP(f, popup_action, pretext):
    if popup_action!=None:
        f.write(pretext + 'self.assertTrue(Test_Util1.Find_Pop(%s))\n'%(popup_action))
    else:
        f.write(pretext + 'self.assertTrue(Test_Util1.Find_Pop())\n' )
    return '识别popup成功'


def rec(f, case_detail, step, manu_val,pretext=''):
    if manu_val==1:
        #文字检测
        left_x = Get_Val(case_detail,'left_x_',step)
        left_y = Get_Val(case_detail,'left_y_',step)
        right_x = Get_Val(case_detail,'right_x_',step)
        right_y = Get_Val(case_detail,'right_y_',step)
        contain = Get_Val(case_detail,'text_recognize_contain_',step)
        text = case_detail['text_recognize_comp_' + str(step)]
        ret = rec_text(f,left_x,left_y,right_x,right_y,contain,text,pretext)
    if manu_val==2:
        contain = Get_Val(case_detail,'icon_recognize_contain_',step)#icon_recognize_contain_1
        #icon = Get_Val(case_detail,'icon_recognize_',step)#icon_recognize_1
        icon = Get_Val(case_detail,'icon_recognize_',step)#case_detail['icon_recognize_' + str(step)]
        ret = rec_icon(f,contain,icon,pretext)
    if manu_val==3:
        ret = rec_QR(f,pretext)
    if manu_val == 4:
        popup_action =  Get_Val(case_detail,'popup_action_',step)#case_detail['popup_action_' + str(step)]#popup_action_1
        ret = rec_POPUP(f,popup_action, pretext)
    return ret

def rec_text_until(f, left_x, left_y, right_x, right_y, contain, text, pretext):
    if text==None:
        return '识别文字失败'
    else:
        if left_x>0 and left_y>0 and right_x>0 and right_y>0:
            #固定区域识别
            text_ret = text.split('/')
            area = '[['+str(left_x)+','+str(left_y)+'],['+str(right_x)+','+str(right_y)+']]'

            if contain=='1':
                #包含这个文字
                f.write(pretext+'if Test_Util1.Find_Word(%s,%s)==None:\n'%(text_ret,area))
                f.write(pretext+'\t'+'ret=True\n')
                f.write(pretext + 'else:\n' )
                f.write(pretext + '\t' + 'ret=False\n')
            else:
                # 不包含这个文字
                f.write(pretext + 'if Test_Util1.Find_Word(%s,%s)==None:\n' % (text_ret, area))
                f.write(pretext + '\t' + 'ret=False\n')
                f.write(pretext + 'else:\n')
                f.write(pretext + '\t' + 'ret=True\n')
        elif (left_x==None and left_y==None and right_x==None and right_y==None) or (left_x==0 and left_y==0 and right_x==0 and right_y==0):
            #全图识别
            text_ret = text.split('/')

            if contain == '1':
                # 包含这个文字
                f.write(pretext + 'if Test_Util1.Find_Word(%s)==None:\n' % (text_ret))
                f.write(pretext + '\t' + 'ret=True\n')
                f.write(pretext + 'else:\n')
                f.write(pretext + '\t' + 'ret=False\n')
            else:
                # 不包含这个文字
                f.write(pretext + 'if Test_Util1.Find_Word(%s)==None:\n' % (text_ret))
                f.write(pretext + '\t' + 'ret=False\n')
                f.write(pretext + 'else:\n')
                f.write(pretext + '\t' + 'ret=True\n')
        return '识别文字成功'

def rec_icon_until(f, contain, icon, pretext):
    if contain=='1':
        icon_ret = icon.split('-')[1]
        f.write(pretext+'if Test_Util1.Pic.Pic_Icon(/%s)==None:\n'%(icon_ret))
        f.write(pretext + '\t' + 'ret=True\n')
        f.write(pretext + 'else:\n')
        f.write(pretext + '\t' + 'ret=False\n')
    else:
        icon_ret = icon.split('-')[1]
        f.write(pretext + 'if Test_Util1.Pic.Pic_Icon(/%s)==None:\n' % (icon_ret))
        f.write(pretext + '\t' + 'ret=False\n')
        f.write(pretext + 'else:\n')
        f.write(pretext + '\t' + 'ret=True\n')
    return '识别图标成功'


def rec_QR_until(f, pretext):
    f.write(pretext + 'if Test_Util1.Pic.Find_QR():\n')
    f.write(pretext + '\t' + 'ret=False\n')
    f.write(pretext + 'else:\n')
    f.write(pretext + '\t' + 'ret=True\n')
    return '识别二维码成功'


def rec_POPUP_until(f, popup_action, pretext):
    if popup_action!=None:
        f.write(pretext + 'if Test_Util1.Find_Pop(%s):\n'%(popup_action))
        f.write(pretext + '\t' + 'ret=False\n')
        f.write(pretext + 'else:\n')
        f.write(pretext + '\t' + 'ret=True\n')
    else:
        f.write(pretext + 'if Test_Util1.Find_Pop():\n' )
        f.write(pretext + '\t' + 'ret=False\n')
        f.write(pretext + 'else:\n')
        f.write(pretext + '\t' + 'ret=True\n')
    return '识别popup成功'



def rec_until(f, case_detail, step, manu_val,pretext=''):
    if manu_val == 1:
        # 文字检测
        left_x = Get_Val(case_detail, 'left_x_', step)
        left_y = Get_Val(case_detail, 'left_y_', step)
        right_x = Get_Val(case_detail, 'right_x_', step)
        right_y = Get_Val(case_detail, 'right_y', step)
        contain = Get_Val(case_detail, 'text_recognize_contain_', step)
        text = case_detail['text_recognize_comp_' + str(step)]
        ret = rec_text_until(f, left_x, left_y, right_x, right_y, contain, text, pretext)
    if manu_val == 2:
        contain = Get_Val(case_detail, 'icon_recognize_contain_', step)  # icon_recognize_contain_1
        # icon = Get_Val(case_detail,'icon_recognize_',step)#icon_recognize_1
        icon = case_detail['icon_recognize_' + str(step)]
        ret = rec_icon_until(f, contain, icon, pretext)
    if manu_val == 3:
        ret = rec_QR_until(f, pretext)
    if manu_val == 4:
        popup_action = case_detail['popup_action_' + str(step)]  # popup_action_1
        ret = rec_POPUP_until(f, popup_action, pretext)
    return ret

def rec_mid_text(f, step,rec_left_x, rec_left_y, rec_right_x, rec_right_y, pretext):
    if rec_left_x>0 and rec_left_y>0 and rec_right_x>0 and rec_right_y>0:
        f.write(pretext+'text_mid_%d=Test_Util1.Pic.Pic_OCR([[%d,%d],[%d,%d]])\n'%(step,rec_left_x,rec_left_y,rec_right_x,rec_right_y))
        return '记录文字成功'
    elif rec_left_x==None and rec_left_y==None and rec_right_x==None and rec_right_y==None:
        f.write(pretext + 'text_mid_%d=Test_Util1.Pic.Pic_OCR()\n' % (step))
        return '记录文字成功'
    else:
        return '记录失败，坐标不合法'


def rec_mid_text_pos(f, step,rec_pos_text, pretext):
    if rec_pos_text==None:
        return '记录失败，文字不合法'
    else:
        f.write(pretext + 'text_mid_pos_%d=Test_Util1.Find_Word(%s)\n' % (step,rec_pos_text.split('/')))
        return '记录文字成功'


def rec_mid_icon_pos(f, step, rec_pos_icon, pretext):
    rec_pos_icon_ret = rec_pos_icon.split('-')[1]
    f.write(pretext + 'text_mid_pos_%d=Test_Util1.Pic.Pic_Icon(/%s)\n' % (step,rec_pos_icon_ret))
    return '记录图片位置成功'


def mid(f, case_detail, step, mid_val,pretext = ''):
    if mid_val==1:
        #rec_left_x_1
        rec_left_x = Get_Val(case_detail,'rec_left_x_',step)
        rec_left_y = Get_Val(case_detail,'rec_left_y_',step)
        rec_right_x = Get_Val(case_detail,'rec_right_x_',step)
        rec_right_y = Get_Val(case_detail,'rec_right_y_',step)
        ret = rec_mid_text(f,step,rec_left_x,rec_left_y,rec_right_x,rec_right_y,pretext = '')
    if mid_val==2:
        #rec_pos_kind_1
        rec_pos_kind = Get_Val(case_detail,'rec_pos_kind_',step)
        if rec_pos_kind==1:
            #文字识别
            #rec_pos_text_1
            rec_pos_text = case_detail['rec_pos_text_' + str(step)]
            ret = rec_mid_text_pos(f,step,rec_pos_text,pretext = '')
        else:
            #图片识别
            #rec_pos_icon_
            rec_pos_icon = case_detail['rec_pos_icon_' + str(step)]
            ret = rec_mid_icon_pos(f, step, rec_pos_icon, pretext='')

    return ret


def comp(f, case_detail, step, rec_val, pretext=''):
    if rec_val==1:
        #文字比较
        text_comp_step = Get_Val(case_detail,'text_comp_step_',step)
        if text_comp_step>0:
            contain = Get_Val(case_detail,'text_comp_contain_',step)
            f.write(pretext +'self.assertTrue(Test_Util1.text_comp(text_mid_pos_%d,text_mid_pos_%d,%s))\n'%(text_comp_step,step,contain))
            return '文字比较成功'
        else:
            return '文字比较失败'

    if rec_val==2:
        #位置比较 pos_comp_step_3

        pos_comp_step = Get_Val(case_detail, 'pos_comp_step_', step)
        if pos_comp_step>0:
            contain = Get_Val(case_detail,'icon_comp_contain_',step)
            f.write(pretext +'self.assertTrue(Test_Util1.icon_comp(text_mid_pos_%d,text_mid_pos_%d,%s))\n'%(step,pos_comp_step,contain))
            return '图片比较成功'
        else:
            return '图片比较失败'

    pass

def comp_until(f, case_detail, step, rec_val, pretext=''):
    if rec_val==1:
        #文字比较
        text_comp_step = Get_Val(case_detail,'text_comp_step_',step)
        if text_comp_step>0:
            contain = Get_Val(case_detail,'text_comp_contain_',step)
            f.write(pretext +'if Test_Util1.text_comp(text_mid_pos_%d,text_mid_pos_%d,%s):\n'%(text_comp_step,step,contain))
            f.write(pretext + '\t' + 'ret=False\n')
            f.write(pretext + 'else:')
            f.write(pretext + '\t' + 'ret=True\n')
            return '文字比较成功'
        else:
            return '文字比较失败'

    if rec_val==2:
        #位置比较 pos_comp_step_3

        pos_comp_step = Get_Val(case_detail, 'pos_comp_step_', step)
        if pos_comp_step>0:
            contain = Get_Val(case_detail,'icon_comp_contain_',step)
            f.write(pretext +'if Test_Util1.icon_comp(text_mid_pos_%d,text_mid_pos_%d,%s):\n'%(step,pos_comp_step,contain))
            f.write(pretext + '\t' + 'ret=False\n')
            f.write(pretext + 'else:\n')
            f.write(pretext + '\t' + 'ret=True\n')
            return '图片比较成功'
        else:
            return '图片比较失败'

    pass

