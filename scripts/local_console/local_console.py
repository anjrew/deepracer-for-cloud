from deepracer.logs import metrics
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import time


parser = ArgumentParser()

parser.add_argument("-r", "--refresh-time", dest="refresh_time",
                    help="The amount of time in seconds between the graph refreshing", type=int ,default=60)

parser.add_argument("-rav", "--rolling-average", dest="rolling_average",
                    help="The rolling average to use for the graph",  type=int ,default=20)

parser.add_argument("-b", "--bucket", dest="bucket",
                    help="The name of the MinIO bucket",  type=str ,default="bucket")

parser.add_argument("-p", "--prefix", dest="prefix",
                    help="The name of the prefix where the model is stored in the MinIO bucket (The model name)",  type=str ,default="rl-deepracer-sagemaker")

parser.add_argument("-m", "--method", dest="method",
                    help="Statistical value to be calculated. Examples are 'mean', 'median','min' & 'max'. Default: 'mean'.",  type=str ,default="mean")


args = vars(parser.parse_args())


BUCKET=args['bucket']
PREFIX=args['prefix']

ag_method = args['method']
refresh_time = args['refresh_time']
rolling_average = args['rolling_average']
linewidth = 2.0

plt.ion()
plt.show(block=False)

def show_stats(): 
    plt.clf()
    plt.cla()
    plt.close()

        
    tm = metrics.TrainingMetrics(BUCKET, model_name=PREFIX, profile='minio', s3_endpoint_url='http://localhost:9000')

    train=tm.getTraining()

    summary_df=tm.getSummary(method=ag_method, summary_index=['r-i','master_iteration'])

    fig, ((ax, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2, figsize=(20,10))
    episodes_text = "Episodes: %i" % len(train)
    iteration_text = "Latest iteration: %s / master %i" % (max(train['r-i']),max(train['master_iteration']))

    fig.suptitle(f'{episodes_text} / {iteration_text}', fontsize=16)
    master_iteration_values = summary_df.index.get_level_values('master_iteration')
    train_completion = summary_df['train_completion']
    eval_completion = summary_df['eval_completion']
    average_completion = summary_df[['train_completion','eval_completion']].mean(axis='columns')
    completion_max = max([train_completion.max(), eval_completion.max()])
    completion_min = min([train_completion.min(), eval_completion.min()])
    train_reward = summary_df['train_reward']
    eval_reward = summary_df['eval_reward']

    summary_df['train_reward_completion'] = (train_completion / 100) * train_reward
    summary_df['eval_reward_completion'] = (eval_completion / 100) * eval_reward


    ax.title.set_text('Completion per iteration')
    ax.plot(master_iteration_values, train_completion.rolling(rolling_average).mean(), linewidth)
    ax.plot(master_iteration_values, eval_completion.rolling(rolling_average).mean(), linewidth)
    ax.plot(master_iteration_values, average_completion.rolling(rolling_average).mean(), linewidth)
    ax.legend([f'Training {ag_method} completion', f'Eval {ag_method} completion', f'Average {ag_method} completion'])
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
    ax3.plot(master_iteration_values, summary_df[['train_reward_completion','eval_reward_completion']].mean(axis='columns').rolling(rolling_average).mean(), linewidth=2.0)
    ax3.legend(['Train Reward/Completion', 'Eval Reward/Completion', 'Average Reward/Completion'])
    ax3.set_xlabel('Interation')
    ax3.set_ylabel('Reward/Completion')

    fig.canvas.draw()
    fig.canvas.flush_events()
    
def view_stat_stream():
  while True:
    show_stats()
    time.sleep(refresh_time)


view_stat_stream()

