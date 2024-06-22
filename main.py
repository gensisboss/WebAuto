import math
from pynput.keyboard import Listener, Key
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 创建一个新的Chrome实例，设置为无头模式（可选）
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 隐藏浏览器界面
# chrome_options.add_argument('--start-maximized')  # 自动最大化窗口


screen_width = 1920
screen_height = 1080
window_num = 2


def calWindSize():
    row = math.ceil(math.sqrt(window_num))
    col = math.floor(window_num / row)
    return [screen_width / row, screen_height / col]


def calWindPos(index):
    row = math.ceil(math.sqrt(window_num))
    col = math.floor(window_num / row)
    wid = screen_width / row
    heig = screen_height / col
    posX = index % row * wid
    posY = math.floor(index / row) * heig
    return [posX, posY]


# 启动多个浏览器窗口
windows = []


def openWindow(url):
    ind = 0
    while ind < window_num:
        driver = webdriver.Chrome(options=chrome_options)
        windows.append(driver)
        driver.get(url)
        driver.set_window_size(calWindSize()[0], calWindSize()[1])
        driver.set_window_position(calWindPos(ind)[0], calWindPos(ind)[1])
        ind += 1


def excuteWindow():
    # 在每个窗口执行任务，例如等待元素加载
    for window in windows:
        try:
            element = WebDriverWait(window, 10).until(
                EC.presence_of_element_located((By.ID, "your_element_id"))
            )
            print(f"Element found in {window.title}")
        except Exception as e:
            print(f"Error: {e}")


def closeWindow(key):
    if key == Key.esc:
        # 关闭所有窗口
        for window in windows:
            window.quit()


if __name__ == '__main__':
    openWindow("https://www.baidu.com")
    with Listener(on_press=closeWindow, on_release=None) as listener:
        listener.join()
