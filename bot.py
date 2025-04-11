import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

# .env 파일 경로 명시적으로 지정
load_dotenv(dotenv_path=r'E:\9.DiscordBot\DiscordProject\.env')  # .env 파일 경로 수정
token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")  # 토큰 없을 시 오류 발생

intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.members = True  # 멤버 관련 인텐트 추가

bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_CHANNEL_ID = 1359921515298295993  # 음성 채널 ID 입력
TARGET_USER_ID = 285012671198265345     # 알림 받을 유저 ID

@bot.event
async def on_ready():
    print(f'{bot.user} 온라인 상태')
    try:
        user = await bot.fetch_user(TARGET_USER_ID)
        print(f"대상 사용자 확인: {user.name}#{user.discriminator}")
    except discord.NotFound:
        print(f"경고: 사용자 ID {TARGET_USER_ID}를 찾을 수 없습니다!")
    check_voice_channel.start()

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        notify_user = await bot.fetch_user(TARGET_USER_ID)
        if (after.channel and after.channel.id == TARGET_CHANNEL_ID) or \
           (before.channel and before.channel.id == TARGET_CHANNEL_ID):
            action = "입장" if after.channel else "퇴장"
            channel = after.channel or before.channel
            await notify_user.send(f"{member.display_name}님이 {channel.name} 채널에 {action}했습니다.")
    except Exception as e:
        print(f"음성 채널 상태 업데이트 중 오류 발생: {e}")

@tasks.loop(minutes=30)
async def check_voice_channel():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if channel.id == TARGET_CHANNEL_ID:  # 특정 채널만 확인
                try:
                    target_user = await bot.fetch_user(TARGET_USER_ID)
                    members = ', '.join([m.display_name for m in channel.members])
                    await target_user.send(
                        f"[정기 점검] {channel.name} 채널 현황: {members}"
                    )
                except discord.NotFound:
                    print(f"사용자 ID {TARGET_USER_ID}를 찾을 수 없습니다.")
                except Exception as e:
                    print(f"오류 발생: {e}")

@check_voice_channel.before_loop
async def before_check():
    await bot.wait_until_ready()

if __name__ == "__main__":
    bot.run(token)
