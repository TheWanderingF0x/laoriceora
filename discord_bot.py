import discord
from discord.ext import commands, tasks
import schedule
import time
import asyncio
from datetime import datetime
import pytz

TOKEN = 'MTI0Mzg0MTA4MzAzNzcxNjUwMQ.GC4QTt.qn797KRJLTOR10M6tJt_99JQZSkhFx80feY5jA'  # Replace with your actual token
CHANNEL_ID = 1244388639652446299
CHANNEL_ID_2 = 1133382109986312283

intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content

bot = commands.Bot(command_prefix='/', intents=intents)

ROMANIA_TZ = pytz.timezone('Europe/Bucharest')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    schedule_tasks()
    check_schedule.start()

async def post_message(time_str):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f'{time_str} pwp :heart:')
        print(f"Posted message for time {time_str} (Romanian Time)")
    else:
        print(f"Channel with ID {CHANNEL_ID} not found")

def schedule_tasks():
    times = [
                "00:00", "01:00", "01:01", "01:11", "02:00", "02:22", "02:02", "03:00", "03:03", "03:33", "04:00", "04:04", "04:44", 
                "05:00", "05:05", "05:55", "06:00", "06:06", "07:00", "07:07", "08:00", "08:08", "09:00", "09:09", "10:00", "10:10",
                "11:00", "11:11", "12:00", "12:12", "12:21", "12:34", "13:00", "13:13", "13:31", "14:00", "14:14", "14:41", "15:00",
                "15:15", "15:51", "16:00", "16:16", "17:00", "17:17", "18:00", "18:18", "19:00", "19:19", "20:00", "20:02", "20:20",
                "21:00", "21:12", "21:21", "22:00", "22:22", "23:00", "23:23", "23:32",
            ]
    for t in times:
        schedule.every().day.at(t).do(lambda time_str=t: asyncio.run_coroutine_threadsafe(post_message(time_str), bot.loop))
        print(f"Scheduled task for {t} (Romanian Time)")

def print_scheduled_tasks():
    jobs = schedule.get_jobs()
    print("Scheduled Tasks:")
    for job in jobs:
        print(f"Time: {job.at_time}, Function: {job.job_func}")

@tasks.loop(seconds=30)  # Run every 30 seconds
async def check_schedule():
    print(f"Checking for pending scheduled tasks at {datetime.now(ROMANIA_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}...")
    schedule.run_pending()

@bot.command(name='tiime')
async def tiime(ctx):
    current_time = datetime.now(ROMANIA_TZ).strftime('%Y-%m-%d %H:%M:%S')
    await ctx.send(f'Current timestamp (Romanian Time): {current_time}')

@bot.command(name='scheduled_tasks')
async def scheduled_tasks(ctx):
    jobs = schedule.get_jobs()
    tasks_list = [f"Time: {job.at_time.strftime('%H:%M')}" for job in jobs]

    # Split the message into chunks if it exceeds 2000 characters
    chunk_size = 2000
    message_parts = []
    current_message = ""

    for task in tasks_list:
        if len(current_message) + len(task) + 1 > chunk_size:
            message_parts.append(current_message)
            current_message = task
        else:
            current_message += "\n" + task

    message_parts.append(current_message)

    for part in message_parts:
        await ctx.send(part)

@bot.command(name='schedule_task')
async def schedule_task(ctx, task_number: int):
    times = [
                "00:00", "01:00", "01:01", "01:11", "02:00", "02:22", "02:02", "03:00", "03:03", "03:33", "04:00", "04:04", "04:44", 
                "05:00", "05:05", "05:55", "06:00", "06:06", "07:00", "07:07", "08:00", "08:08", "09:00", "09:09", "10:00", "10:10",
                "11:00", "11:11", "12:00", "12:12", "12:21", "12:34", "13:00", "13:13", "13:31", "14:00", "14:14", "14:41", "15:00",
                "15:15", "15:51", "16:00", "16:16", "17:00", "17:17", "18:00", "18:18", "19:00", "19:19", "20:00", "20:02", "20:20",
                "21:00", "21:12", "21:21", "22:00", "22:22", "23:00", "23:23", "23:32",
            ]
    if 0 <= task_number < len(times):
        selected_time = times[task_number]
        await post_message(selected_time)
    else:
        await ctx.send("Invalid task number. Please provide a number between 0 and 59.")

if __name__ == "__main__":
    print_scheduled_tasks()  # Print scheduled tasks when the bot starts
    bot.run(TOKEN)