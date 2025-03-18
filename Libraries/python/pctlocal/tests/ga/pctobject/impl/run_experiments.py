# create a function that loops through all the experiments for a comet_ml workspace and project and based on the score and the reward metrics downloads the artifact to the /tmp/artifacts directory and then runs the corresponding PCTHierarchy.run_from_file

import comet_ml
from comet_ml.query import Metric

# from pctlocal import PCTHierarchy

def run_experiments(workspace, project, score_metric, reward_metric):
    # get all the experiments
    api = comet_ml.API()
    # experiments = api.get_experiments(workspace, project)

    experiments = api.query(workspace, project, Metric("score") < 0.05)
    
    for apiexperiment in experiments:
        # name of experiment
        # get the experiment
        # experiment = api.get_experiment_by_key(apiexperiment.key)
        # get the metrics
        # metrics = apiexperiment.get_metrics()
        # for metric in metrics:
        #     if not metric['metricName'].startswith('sys'):
        #         print(metric)
        
        score_metric = apiexperiment.get_metrics("score")
        reward_metric = apiexperiment.get_metrics("reward")
        score = eval(score_metric[0]["metricValue"])
        reward = eval(reward_metric[0]["metricValue"])    
        print(f'{apiexperiment.name} {score:4.3f} {reward:4.3f}')

        # Download the artifact associated with the experiment
        artifact_list = apiexperiment.get_artifacts()
        for artifact in artifact_list:
            artifact.download(destination="/tmp/artifacts", overwrite=True)
            print(f"Downloaded artifact: {artifact.name}")

        pass
        # get the score and reward metrics
        # score = metrics[score_metric]
        # reward = metrics[reward_metric]
        # print(score, reward)

        # download the artifact
        # experiment.download_artifact()
        # # run the PCTHierarchy.run_from_file
        # PCTHierarchy.run_from_file('/tmp/artifacts/' + experiment.name)

run_experiments('lunarlandercontinuous-v2', 'refinputs-smooth', 'score', 'reward')






