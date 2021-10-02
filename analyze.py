import json
from os import supports_dir_fd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
from seaborn.palettes import color_palette
import pandas as pd

sns.set_style('dark')

data_obj = json.loads(open("ps2.json", "r", encoding="utf-8").read())
CONTEST_START =  dt.datetime(2021, 9, 21, 17, 0, 0) 

student_submissions = []
for submission in data_obj["models"]:
    if(submission["time_from_start"] > 0):
        student_submissions.append(submission)
student_submissions = student_submissions[::-1]

fig, ax = plt.subplots(2, 2, figsize=(14, 8))
fig.tight_layout()
plt.subplots_adjust(top=0.95, hspace=0.3)

def stacked_status():
    hour_offset = [0]
    times = []
    ac = [0]
    wrong = [0]
    for sub in student_submissions:
        hour_offset.append(sub["time_from_start"]/60)
        ac.append(ac[-1] + (1 if sub["status"] == "Accepted" else 0))
        wrong.append(wrong[-1] + (1 if sub["status"] != "Accepted" else 0))
    
    for h in hour_offset:
        times.append(CONTEST_START + dt.timedelta(hours=h))
    

    date_form = DateFormatter("%a")
    locator = mdates.AutoDateLocator(minticks=10, maxticks=15)
    ax[0][0].xaxis.set_major_formatter(date_form)
    ax[0][0].xaxis.set_major_locator(locator)

    labels = ["Accepted", "Rejected"]
    ax[0][0].stackplot(times, ac, wrong, labels=labels, colors=["lime", "crimson"])
    ax[0][0].set_title("Accepted vs Rejected Submissions")
    ax[0][0].set_ylabel("Submissions")
    ax[0][0].legend(loc='upper left')

def submission_per_hour():
    delta_t = 60 # 60 minute interval
    buckets = [0 for _ in range(int(student_submissions[-1]["time_from_start"]//delta_t) + 1)]
    for sub in student_submissions:
        buckets[int(sub["time_from_start"]//delta_t)] += 1
    
    times = []
    for i in range(len(buckets)):
        times.append(CONTEST_START + dt.timedelta(hours=i))

    date_form = DateFormatter("%a")
    locator = mdates.AutoDateLocator(minticks=10, maxticks=15)
    ax[0][1].xaxis.set_major_formatter(date_form)
    ax[0][1].xaxis.set_major_locator(locator)

    ax[0][1].set_title("Submissions Over Time")
    ax[0][1].set_ylabel("Submissions/Hour")
    ax[0][1].plot(times, buckets)

def common_missed_cases():
    missed = {}
    for sub in student_submissions:
        for tc in range(len(sub["testcase_message"])):
            if(tc not in missed):
                missed[tc] = 0
            
            if(sub["testcase_message"][tc] != "Correctly found a solution!"):
                missed[tc] += 1
    
    colors = []
    for tc in missed:
        porp = missed[tc]/len(student_submissions)
        colors.append((min(1, 1.5*missed[tc] / len(student_submissions)), min(1, 0.05/porp), 0.3 ))

    ax[1][0].set_title("Most commonly failed testcases")
    ax[1][0].set_xticks(range(0, len(missed), 1))
    ax[1][0].bar(missed.keys(), missed.values(), color=colors, align="center")

def common_errors():
    err_count = {}
    for sub in student_submissions:
        for tc in range(len(sub["testcase_message"])):
            if(sub["testcase_message"][tc] not in err_count):
                err_count[sub["testcase_message"][tc]] = 0
            err_count[sub["testcase_message"][tc]] += 1

    ax[1][1].set_title("Result Frequency")
    patches, text = ax[1][1].pie(err_count.values())
    ax[1][1].legend(err_count.keys(), loc="upper left",fontsize=7)



stacked_status()
submission_per_hour()
common_missed_cases()
common_errors()

plt.show()