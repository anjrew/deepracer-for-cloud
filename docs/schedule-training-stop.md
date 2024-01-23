# Schedule Training Stop

Schedule a Task as Root:

To schedule a task, you need to switch to the root user or use sudo to run the at command. For example, to schedule a task to run 30 minutes from now, you would use:
```bash
sudo at now + 30 minutes
```

After entering this command, you'll get a prompt where you can enter the command(s) you want to run. Once you've entered your commands, press Ctrl+D to save the scheduled task.

Verify Scheduled Jobs:
You can list all scheduled at jobs by running:

```bash
sudo atq
```

View the Content of a Scheduled Job:
To see what commands are scheduled in a job, use at -c followed by the job number. For example:

```bash
sudo at -c [job number]
```

Tip:

Example commands to stop training and shutdown after 6 hours:

```bash
sudo at now + 8 hours

dr-stop-training 
shutdown +2
```