import json
from os import supports_dir_fd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('dark')

data_obj = json.loads(open("ps2.json", "r", encoding="utf-8").read())

for k in data_obj["models"]:
    k["hacker_id"] = "redacted"
    k["hacker_username"] = "redacted"
open("ps2proc.json", "w").write(json.dumps(data_obj))

input()

student_submissions = []
print(data_obj["models"][0])
print(len(data_obj["models"]))
for submission in data_obj["models"]:
    if(submission["time_from_start"] > 0):
        student_submissions.append(submission)
student_submissions = student_submissions[::-1]

def stacked_status():
    times = [0]
    ac = [0]
    wrong = [0]
    for sub in student_submissions:
        times.append(sub["time_from_start"]/(60*24))
        ac.append(ac[-1] + (1 if sub["status"] == "Accepted" else 0))
        wrong.append(wrong[-1] + (1 if sub["status"] != "Accepted" else 0))

    fig, ax = plt.subplots()
    labels = ["Accepted", "Rejected"]
    ax.stackplot(times, ac, wrong, labels=labels, colors=["lime", "crimson"])
    ax.legend(loc='upper left')
    plt.show()

def submission_per_hour():
    delta_t = 60 # 60 minute interval
    buckets = [0 for _ in range(int(student_submissions[-1]["time_from_start"]//delta_t) + 1)]
    for sub in student_submissions:
        buckets[int(sub["time_from_start"]//delta_t)] += 1


    fig, ax = plt.subplots()
    ax.set_title("Submissions Per Hour")
    ax.set_xlabel("Hours since contest start")
    ax.set_ylabel("Submissions/Hour")
    ax.set_xticks(range(0, len(buckets), 20))
    ax.plot(buckets)
    plt.show()

def common_missed_cases():
    missed = {}
    for sub in student_submissions:
        for tc in range(len(sub["testcase_message"])):
            if(tc not in missed):
                missed[tc] = 0
            
            if(sub["testcase_message"][tc] != "Correctly found a solution!"):
                missed[tc] += 1

        
    
    fig, ax = plt.subplots()
    ax.set_title("Most commonly failed testcasese")
    ax.pie(missed.values(), labels=missed.keys())
    plt.show()



common_missed_cases()

