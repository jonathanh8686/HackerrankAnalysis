import json
import matplotlib.pyplot as plt


data_obj = json.loads(open("ps2.json", "r", encoding="utf-8").read())

student_submissions = []
print(data_obj["models"][0])
for submission in data_obj["models"]:
    if(submission["time_from_start"] > 0):
        student_submissions.append(submission)
    

times = [0]
ac = [0]
wrong = [0]
for sub in student_submissions:
    times.append(sub["time_from_start"])
    ac.append(ac[-1] + (1 if sub["status"] == "Accepted" else 0))
    wrong.append(wrong[-1] + (1 if sub["status"] != "Accepted" else 0))

print(ac)

fig, ax = plt.subplots()
labels = ["Accepted ", "Processed"]
ax.stackplot(times, ac, wrong, labels=labels)
ax.legend(loc='upper left')
plt.show()