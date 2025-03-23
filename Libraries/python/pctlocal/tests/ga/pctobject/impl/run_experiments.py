


from pct.experiments import CometExperimentManager

"""

python -m impl.run_experiments

"""


# Initialize the manager
workspace = 'lunarlandercontinuous-v2'
	
project_name = 'refinputs-currentrms'
# project_name = 'refinputs-smooth'
num_runs=100

manager = CometExperimentManager(workspace=workspace)

# Test get_all_artifacts_sorted
artifact_results = manager.get_all_artifacts_indexed()
# print("Artifacts sorted by source experiment key:", artifacts)

# Test get_experiments_by_metrics
experiments = manager.get_experiments_by_metrics(project_name=project_name, score_threshold=0.05, reward_threshold=10.0)
# print("Filtered experiments:", experiments)


output_csv = f'/tmp/artifacts/experiment_results_{project_name}.csv'
manager.run_experiments_and_record_results(experiments=experiments, project_name=project_name, artifact_results=artifact_results, num_runs=num_runs, output_csv=output_csv)
print(f"Results saved to {output_csv}")




