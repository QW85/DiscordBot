import discord
from discord.ext import commands

# 인텐트 설정
intents = discord.Intents.default()
intents.members = True  # 서버 멤버 관련 이벤트 허용
intents.voice_states = True  # 음성 상태 업데이트 이벤트 허용
n
# 봇 초기화
bot = commands.Bot(command_prefix="!", intents=intents)

# 특정 음성 채널 ID와 특정 사용자 ID를 설정합니다
TARGET_CHANNEL_ID = 1359921515298295993  # 감시할 음성 채널의 ID를 입력하세요
NOTIFY_USER_ID = 285012671198265345  # 특정 알림을 받을 유저의 ID를 입력하세요


@bot.event
async def on_ready():
    print(f"봇이 실행되었습니다! 봇 이름: {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    try:
        notify_user = await bot.fetch_user(NOTIFY_USER_ID)
        if not notify_user:
            print(f"알림 유저(ID: {NOTIFY_USER_ID})를 찾을 수 없습니다.")
            return

        displayed_name = member.display_name

        # 음성 채널 입장 감지
        if before.channel is None and after.channel and after.channel.id == TARGET_CHANNEL_ID:
            await notify_user.send(f"🔔 **{displayed_name}**님이 **{after.channel.name}** 채널에 입장했습니다!")

        # 음성 채널 퇴장 감지
        elif before.channel and before.channel.id == TARGET_CHANNEL_ID and after.channel is None:
            await notify_user.send(f"❌ **{displayed_name}**님이 **{before.channel.name}** 채널에서 퇴장했습니다!")

    except Exception as e:
        print(f"on_voice_state_update 처리 중 오류 발생: {e}")


# 봇 실행
bot.run("MTM1OTkyMzc5MDE1MDExMTMwMg.G2yv38.OIqeh8BkXojrvUED-ITV7fCdbu5wLOaZo16OqY")
