import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

def get_data():
    # 设置浏览器驱动路径
    driver_path = './msedgedriver.exe'  # 当前驱动版本适用于 Microsoft Edge Stable 139.0.3405.125
    service = Service(driver_path)

    # 设置 Edge 浏览器的选项
    options = Options()
    options.add_argument("--headless")  # 启用 headless 模式，不弹出浏览器界面

    # 创建浏览器实例
    driver = webdriver.Edge(service=service, options=options)

    # 打开目标网页
    driver.get('https://www.chinamoney.com.cn/english/bdInfo/')

    # 等待页面加载完成
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'Bond_Type_select')))
    except:
        print("等待超时，未找到Bond_Type_select元素！")
        driver.quit()
        return

    # 输入选择条件：选择 "Treasury Bond"
    bond_type_select = driver.find_element(By.ID, 'Bond_Type_select')
    bond_type_select.send_keys('Treasury Bond')

    # 输入选择条件：选择 "2023" 年
    issue_year_select = driver.find_element(By.ID, 'Issue_Year_select')
    issue_year_select.send_keys('2023')

    # 点击搜索按钮
    search_button = driver.find_element(By.XPATH, "//a[text()='Search']")
    search_button.click()

    # 等待页面数据加载
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='san-sheet-alternating']")))

    # 创建列表存储所有页面的数据
    all_data = []

    # 获取页面总页数
    while True:
        # 获取页面内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 解析表格数据
        table = soup.find('table', class_='san-sheet-alternating')  # 查找表格
        if not table:
            print("没有找到表格！")
            break

        rows = table.find_all('tr')  # 获取所有表格行

        # 提取表格列标题
        if len(all_data) == 0:  # 只需要在第一页提取列标题
            columns = [col.text.strip() for col in rows[0].find_all('td')]

        # 提取表格中的数据行
        data = []
        for row in rows[1:]:  # 跳过标题行
            cols = row.find_all('td')
            # 获取每列的文本并去掉多余的空格
            data_row = [col.text.strip() for col in cols]
            if len(data_row) == len(columns):  # 确保列数一致
                data.append(data_row)

        all_data.extend(data)  # 将当前页的数据添加到 all_data 中

        # 等待确保“Next”按钮加载完
        try:
            next_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='page-btn page-next']/a"))
            )
        except:
            print("无法找到下一页按钮，结束爬取！")
            break

        # 判断是否有下一页，如果有，则点击“Next”按钮
        if "disabled" in next_button.get_attribute("class"):
            break  # 如果下一页按钮被禁用，说明已经是最后一页，跳出循环
        else:
            next_button.click()  # 点击下一页
            time.sleep(2)  # 等待页面加载

    # 关闭浏览器
    driver.quit()

    # 保存数据为CSV文件
    df = pd.DataFrame(all_data, columns=columns)
    df.to_csv('bond_data_all.csv', index=False)
    print('所有数据已保存到 bond_data_all.csv')

if __name__ == '__main__':
    # 调用函数执行抓取和保存操作
    get_data()
