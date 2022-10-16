from deepracer.logs import metrics
import matplotlib.pyplot as plt
from threading import Timer
import threading 
import sched, time
import numpy as np

NUM_ROUNDS=1

BUCKET="bucket"
PREFIX="rl-deepracer-1"

refresh_time = 5.0
rolling_average = 10
linewidth = 2.0


def show_stats(): 
    plt.clf()
    plt.cla()
    plt.close()
    plt.show(block=False)
    plt.ion()
        
    tm = metrics.TrainingMetrics(BUCKET, model_name=PREFIX, profile='minio', s3_endpoint_url='http://localhost:9000')

    train=tm.getTraining()
    ev=tm.getEvaluation()

    summary_df=tm.getSummary(method='mean', summary_index=['r-i','master_iteration'])

    # print()
    # print("Episodes: %i" % len(train))

    fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2, figsize=(20,10))
    # fig.suptitle('Current session')
    fig.suptitle("Latest iteration: %s / master %i" % (max(train['r-i']),max(train['master_iteration'])), fontsize=16)

    master_iteration_values = summary_df.index.get_level_values('master_iteration')
    train_completion = summary_df['train_completion']
    eval_completion = summary_df['eval_completion']
    completion_max = max([train_completion.max(), eval_completion.max()])
    completion_min = min([train_completion.min(), eval_completion.min()])
    train_reward = summary_df['train_reward']
    eval_reward = summary_df['eval_reward']

    summary_df['train_reward_completion'] = train_completion * train_reward
    summary_df['eval_reward_completion'] = eval_completion * eval_reward


    ax.title.set_text('Completion per iteration')
    ax.plot(master_iteration_values, train_completion.rolling(10).mean(), linewidth)
    ax.plot(master_iteration_values, eval_completion.rolling(10).mean(), linewidth)
    ax.legend(['Training mean completion', 'Eval mean completion'])
    ax.set_xlabel('Interation')
    ax.set_ylabel('% completion')
    ax.set_ylim(completion_min,completion_max)

    ax2.title.set_text('Reward vs Completion')
    ax2.scatter(train_completion, summary_df['train_reward'], linewidth)
    ax2.scatter(eval_completion, summary_df['eval_reward'], linewidth)
    ax2.legend(['Training', 'Evaluation'])
    ax2.set_ylabel('Reward')
    ax2.set_xlabel('% completion')

    ax3.title.set_text('Reward/Completion per iteration')
    ax3.plot(master_iteration_values, summary_df['train_reward_completion'].rolling(rolling_average).mean(), linewidth=2.0)
    ax3.plot(master_iteration_values, summary_df['eval_reward_completion'].rolling(rolling_average).mean(), linewidth=2.0)
    ax3.legend(['Train Reward/Completion', 'Eval Reward/Completion'])
    ax3.set_xlabel('Interation')
    ax3.set_ylabel('Reward/Completion')
    # plt.ion()
    # plt.draw()
    # plt.show()
    plt.draw() 
    plt.pause(0.01)
    
def view_stat_stream():
  while True:
    show_stats()
    time.sleep(refresh_time)
#arguments: 
#how long to wait (in seconds), 
#what function to call, 
#what gets passed in
# r = Timer(refresh_time, show_stats())

# r.start()
view_stat_stream()

# t1 = threading.Thread(target=view_stat_stream)  

# t1.start()
