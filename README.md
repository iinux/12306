12306 车票查询通知程序
======================
#### 安装和使用
  1. 安装 Python 2.7 或更高版本
  1. `git clone https://github.com/iinux/12306`
  1. 修改 config 和 ticket info 设置接收邮箱，出发地，目的地，日期，席别，出发时间限制，到达时间限制，
  1. `python main.py` 运行程序

#### 可能的问题
  1. 因为 12306 的保护策略，会定期更新 API 接口地址，如果连续出现 urllib2.HTTPError 或 urllib2.URLError 可能是因为地址换了，按照图片 ![find_random_letter.png](http://zhangqun.site/images/find_random_letter.png) 的指示查找新的随机字母（A-Z），当然，也可能是因为你的IP被加入黑名单了，停止若干天就会解除黑名单
  1. 程序进行了异常捕获，但仍可能是异常退出，可以用 supervisord 对本程序进行托管
