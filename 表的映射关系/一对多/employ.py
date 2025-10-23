""" 
员工类
 """
class Employ:
    def __init__(self, eid, name, age, salary, job):
        self.eid = eid #员工编号
        self.job = job #员工职位
        self.name = name
        self.age = age
        self.salary = salary
        self.dept = None #关键dept=None表示初始化关联字段所属部门
        self.mgr = None #关键mgr=None表示初始化关联字段所属经理
    def get_emp_info(self):
        return f"员工编号:{self.eid},姓名:{self.name},职位:{self.job},部门:{self.dept}"
    def __str__(self):
        return self.get_emp_info()
    def __repr__(self):
        return f"Employ({self.eid},{self.name},{self.age},{self.salary},{self.job})"