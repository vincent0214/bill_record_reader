## 简介
`bill_record_reader`项目是一个用于个人账单处理的项目.
可以用来合并某一年支付宝和微信的`支出收入账单`, 生成一个统一的Excel文件

## 如何运行?
1. 安装依赖
```python
pip install pandas
```
2. 从微信和支付宝APP中导出账单csv文件

3. 把`微信账单csv文件`和`支付宝账单csv文件`放入`source`文件夹

4. 执行代码,合并账单
```python
python main.py
```
5. 查看结果
   结果存放在`target`文件夹

## 如何修改输出的文件名称?
打开`main.py`文件,修改变量`output_file_name`

