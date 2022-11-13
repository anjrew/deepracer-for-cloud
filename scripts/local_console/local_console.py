from deepracer.logs import metrics
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import time
from deepracer.logs import \
    AnalysisUtils as au, \
    DeepRacerLog
from deepracer.logs import ( DeepRacerLog, S3FileHandler)
import logging




parser = ArgumentParser()

parser.add_argument("-r", "--refresh-time", dest="refresh_time",
                    help="The amount of time in seconds between the graph refreshing", type=int ,default=60)

parser.add_argument("-rav", "--rolling-average", dest="rolling_average",
                    help="The rolling average to use for the graph",  type=int)

parser.add_argument("-b", "--bucket", dest="bucket",
                    help="The name of the MinIO bucket",  type=str ,default="bucket")

parser.add_argument("-p", "--prefix", dest="prefix",
                    help="The name of the prefix where the model is stored in the MinIO bucket (The model name)",  type=str ,default="rl-deepracer-sagemaker")

parser.add_argument("-m", "--method", dest="method",
                    help="Statistical value to be calculated. Examples are 'mean', 'median','min' & 'max'. Default: 'mean'.",  type=str ,default="mean")

# SET MINIO ARG
# parser.add_argument("-m", "--method", dest="method",
#                     help="Statistical value to be calculated. Examples are 'mean', 'median','min' & 'max'. Default: 'mean'.",  type=str ,default="mean")


args = vars(parser.parse_args())


BUCKET=args['bucket']
PREFIX=args['prefix']
print('Showing logs for ', PREFIX)
ag_method = args['method']
refresh_time_s = args['refresh_time']
rolling_average = args['rolling_average']
linewidth = 2.0

plt.ion()
plt.show(block=False)

fh = S3FileHandler(bucket=BUCKET, prefix=PREFIX,
                   profile="minio", s3_endpoint_url="http://localhost:9000")
tm = metrics.TrainingMetrics(BUCKET, model_name=PREFIX, profile='minio', s3_endpoint_url='http://localhost:9000')

log = DeepRacerLog(filehandler=fh)


def show_stats(): 
  
    global rolling_average
  
    plt.clf()
    plt.cla()
    plt.close()

    try:
      log.load(force=True)

      df = log.dataframe()
      
      train=tm.getTraining()

      summary_df=tm.getSummary(method=ag_method, summary_index=['r-i','master_iteration'])

      fig, ((ax, ax2, ax7), (ax3, ax4, ax8), (ax5, ax6, ax9)) = plt.subplots(ncols=3, nrows=3, figsize=(20,10))
      episodes_text = "Episodes: %i" % len(train)
      iteration_text = "Latest iteration: %s / master %i" % (max(train['r-i']),max(train['master_iteration']))

      fig.suptitle(f'{episodes_text} / {iteration_text}', fontsize=16)
      fig.tight_layout(pad=5.0)
      
      master_iteration_values = summary_df.index.get_level_values('master_iteration')
      
      if rolling_average is None:
        amount_of_data_points = 5
        rolling_average = int(round(len(master_iteration_values) / amount_of_data_points, 0))

      print(f'Showing with rolling avarage {rolling_average} based on  master_iteration_values {len(master_iteration_values)} and {amount_of_data_points}')
      
      train_completion = summary_df['train_completion']
      eval_completion = summary_df['eval_completion']
      average_completion = summary_df[['train_completion','eval_completion']].mean(axis='columns')
      train_reward = summary_df['train_reward']
      eval_reward = summary_df['eval_reward']

      summary_df['train_reward_completion'] = (train_completion / 100) * train_reward
      summary_df['eval_reward_completion'] = (eval_completion / 100) * eval_reward


      ax.title.set_text('Completion per iteration')  # type: ignore
      
      training_method_completion_label = f'Training {ag_method} completion'
      eval_method_completion_label = f'Eval {ag_method} completion'
      av_method_label = f'Average {ag_method} completion'
      by_label = {
        training_method_completion_label: "blue",
        eval_method_completion_label:"orange",
        av_method_label: "purple"
      }
      
      ax.plot(master_iteration_values, train_completion.rolling(rolling_average).mean(), linewidth, label=training_method_completion_label, color=by_label[training_method_completion_label])
      ax.plot(master_iteration_values, eval_completion.rolling(rolling_average).mean(), linewidth, label=eval_method_completion_label, color=by_label[eval_method_completion_label])
      ax.plot(master_iteration_values, average_completion.rolling(rolling_average).mean(), linewidth, label=av_method_label, color=by_label[av_method_label])
      ax.set_xlabel('Interation')
      ax.set_ylabel('% Completion')
      
      ax.legend(by_label)

      ax2.title.set_text('Reward vs Completion')  # type: ignore
      ax2.scatter(train_completion, summary_df['train_reward'], linewidth=linewidth)
      ax2.scatter(eval_completion, summary_df['eval_reward'], linewidth=linewidth)
      ax2.legend(['Training', 'Evaluation'])
      ax2.set_ylabel('Reward')
      ax2.set_xlabel('% Completion')

      ax3.title.set_text('Reward/Completion per iteration')  # type: ignore
      ax3.plot(master_iteration_values, summary_df['train_reward_completion'].rolling(rolling_average).mean(), linewidth=linewidth)
      ax3.plot(master_iteration_values, summary_df['eval_reward_completion'].rolling(rolling_average).mean(), linewidth=linewidth)
      ax3.plot(master_iteration_values, summary_df[['train_reward_completion','eval_reward_completion']].mean(axis='columns').rolling(rolling_average).mean(), linewidth=linewidth)
      ax3.legend(['Train Reward/Completion', 'Eval Reward/Completion', 'Average Reward/Completion'])
      ax3.set_xlabel('Interation')
      ax3.set_ylabel('Reward/Completion')

      ax4.title.set_text('Reward per iteration')  # type: ignore
      ax4.plot(master_iteration_values, summary_df['train_reward'].rolling(rolling_average).mean(), linewidth=linewidth)
      ax4.plot(master_iteration_values, summary_df['eval_reward'].rolling(rolling_average).mean(), linewidth=linewidth)
      ax4.plot(master_iteration_values, summary_df[['train_reward','eval_reward']].mean(axis='columns').rolling(rolling_average).mean(), linewidth=linewidth)
      ax4.legend(['Train Reward/Completion', 'Eval Reward/Completion', 'Average Reward/Completion'])
      ax4.set_xlabel('Interation')
      ax4.set_ylabel('Reward')
      
      ax5.title.set_text('Completion per iteration')  # type: ignore
      ax5.plot(master_iteration_values, train_completion.rolling(rolling_average).mean(), linewidth=linewidth)
      ax5.plot(master_iteration_values, eval_completion.rolling(rolling_average).mean(), linewidth=linewidth)
      ax5.plot(master_iteration_values, summary_df[['train_completion','eval_completion']].mean(axis='columns').rolling(rolling_average).mean(), linewidth=linewidth)
      ax5.legend(['Train Iteration/Completion', 'Eval Iteration/Completion', 'Average Iteration/Completion'])
      ax5.set_xlabel('Interation')
      ax5.set_ylabel('Completion')

      simulation_agg = au.simulation_agg(df, secondgroup="unique_episode")
      complete_laps = simulation_agg[simulation_agg['progress']==100]

      ax6.title.set_text('Reward vs Time for completed laps')  # type: ignore
      ax6.scatter(complete_laps['time'], complete_laps['reward'], linewidth=linewidth)
      ax6.set_xlabel('Time')
      ax6.set_ylabel('Reward')
      
      
      time_complete_rolling_av = complete_laps['time'].rolling(rolling_average).mean()
      ax7.title.set_text('Completed lap times per unique episode')  # type: ignore
      ax7.plot(time_complete_rolling_av, linewidth=linewidth)
      ax7.set_xlabel('unique_episode')
      ax7.set_ylabel('time')
      
      fig.canvas.draw()
      fig.canvas.flush_events()
      
    except:
      print(f'Logs not found. Tring again after {refresh_time_s} seconds')
        
def view_stat_stream():
  while True:
    show_stats()
    time.sleep(refresh_time_s)


view_stat_stream()

