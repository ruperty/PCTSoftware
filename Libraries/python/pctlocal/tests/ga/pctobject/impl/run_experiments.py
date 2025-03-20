
import comet_ml
from comet_ml.query import Metric

from pct.experiments import CometExperimentManager

# from pctlocal import PCTHierarchy

def run_experiments(workspace, project, score_metric, reward_metric):
    # get all the experiments
    api = comet_ml.API()
    # experiments = api.get_experiments(workspace, project)

    experiments = api.query(workspace, project, Metric("score") < 0.05)
    
    for apiexperiment in experiments:
        
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

# run_experiments('lunarlandercontinuous-v2', 'refinputs-smooth', 'score', 'reward')


# Initialize the manager
workspace = 'lunarlandercontinuous-v2'
project_name = 'refinputs-smooth'
manager = CometExperimentManager(workspace=workspace)

# Test get_all_artifacts_sorted
artifacts = manager.get_all_artifacts_indexed()
# print("Artifacts sorted by source experiment key:", artifacts)

# Test get_experiments_by_metrics
# experiments = manager.get_experiments_by_metrics(
#     project_name=project_name,
#     score_threshold=0.05,
#     reward_threshold=10.0
# )
# print("Filtered experiments:", experiments)






