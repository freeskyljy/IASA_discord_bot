from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import asyncio
import time

# 필요한 것들 불러오기
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

klist = open("temp/important_data.txt", "r").readlines()
token = klist[0].strip()
user_id = klist[1].strip()
user_pw = klist[2].strip()
link = klist[3].strip()

today = date.today().isoformat()  # 20XX-XX-XX꼴로 출력됨
new = []
links = []
links_list = open("temp/links.txt", "r").readlines()
for link_ in links_list:
    links.append(link_.strip())
subject = ['공지사항', '소집교육', '수학', '물리', '화학', '생명과학', '지구과학', '영어', '독서과제']

스크래핑
browser = webdriver.Chrome('temp/chromedriver.exe')
browser.get(link)
time.sleep(3)
elem = browser.find_element(By.XPATH, "//a[@title='새창이동']")
elem.click()
time.sleep(2)

browser.find_element(By.ID, "usrID").send_keys(user_id)
browser.find_element(By.ID, "usrPass").send_keys(user_pw)
browser.find_element(By.ID, "loginbtn").click()
time.sleep(2)
# 필요한 정보만 추출
for i in range(9):
    browser.get(links[i])

    soup = BeautifulSoup(browser.page_source, "html.parser")

    inform = soup.select('tr')

    for inf in inform[1:11]:
        number, name, writer, views, date_ = inf.select('td')
        if date_.get_text() == today:
            new.append([number.get_text(), name.get_text(), writer.get_text(),
                        views.get_text(), date_.get_text(), links[i], subject[i]])
    time.sleep(2)
browser.quit()

new = [['1', '2', '3', '4', 'https://www.naver.com', 'afsd', 'asdf', 'as']]
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@bot.event
async def on_ready():  # 봇이 시작할 때 한번 실행
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("작동"))  # 봇 상태 메시지 바꾸기
    for j in new:
        embed = discord.Embed(title=j[1], description=j[6], color=discord.Color.from_rgb(241, 196, 15))
        embed.add_field(name=j[2], value="조회수:" + j[3], inline=False)
        embed.add_field(name='링크:', value=j[5])
        embed.set_footer(text=today, icon_url=j[5])
        for guild in bot.guilds:  # 이거 찾느라 고생함.. ㅋㅋ
            for channel in guild.channels:
                if isinstance(channel,
                              discord.TextChannel) and channel.name == '봇':  # 텍스트 채널, 채널 이름 확인
                    await bot.change_presence(status=discord.Status.online, activity=discord.Game("작동"))

    await bot.close()

bot.run(token)

