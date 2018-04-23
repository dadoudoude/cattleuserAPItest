# coding:utf-8
import unittest
import HTMLTestRunner
import sys
sys.path.append('/var/lib/jenkins/workspace/birduserAPItest/report')
from send_email import main2
def all_case():
    #case_dir = "C:\\Users\\liugc\\PycharmProjects\\birddatacenter\\interface"
    case_dir = "/var/lib/jenkins/workspace/birduserAPItest/interface"
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
    # discover方法筛选出来的用例，循环添加到测试套件中
    #for test_suite in discover:
    #    for test_case in test_suite:
    #        #testunit.addTests(test_case)
    #       # print(testunit)
    print("discover",discover)
    testcase.addTests(discover)
    print("aa",testcase)
    return testcase
if __name__ == "__main__":

    #report_path="C:\\Users\\liugc\\PycharmProjects\\birddatacenter\\report\\result.html"
    report_path="/var/lib/jenkins/workspace/birduserAPItest/report/result.html"
    fp= open(report_path,"wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'鸟类数据中心API测试报告',
                                           description=u'用例执行结果')
    #runner = unittest.TextTestRunner()
    # run所有用例
    print(u"测试用例开始执行，请耐心等待")
    runner.run(all_case())
    print(u"测试用例执行已结束")
    fp.close()
    print(u"即将发送邮件，请稍等")
    main2()
    print(u"邮件发送成功，请注意查收")