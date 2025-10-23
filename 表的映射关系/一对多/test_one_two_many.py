""" 测试一对多关系映射 """
from employ import Employ
from dept import Dept
def test():
    #主函数测试
    #建立映射关系
    dept = Dept(16, '项目部', '美国波士顿')
    empA= Employ(1, '张三',21,  199999, '员工')
    empB= Employ(2, '王五', 22, 19999, '组长')
    empC= Employ(3, '李四', 23, 8000, '项目经理')

    empA.mgr = empB
    empB.mgr = empC

    empA.dept = dept
    empB.dept = dept
    empC.dept = dept

    dept.emps = [empA, empB, empC]

    print(dept.get_dept_info())
    for emp in dept.emps:
        print(emp.get_emp_info())
        if str(emp.job) in ['组长', '项目经理']:
            print(f'领导：{emp.get_emp_info()}')
if "__main__" == __name__:
    test()