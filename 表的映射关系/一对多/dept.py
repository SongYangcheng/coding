""" 定义部门类 """
class Dept:
    def  __init__(self, deptno=None, dname=None, loc=None):
        self.deptno=deptno
        self.dname=dname
        self.loc=loc #部门位置
        self.emps=[] #【关键】，emps=[]表示初始化关联字段所属员工列表, 多对一
    def get_dept_info(self):
        return f"部门编号:{self.deptno},部门名称:{self.dname},部门人数:{len(self.emps)}"
    def __str__(self):
        return self.get_dept_info()
    def __repr__(self):
        return f"Dept({self.deptno},{self.dname},{self.loc})"