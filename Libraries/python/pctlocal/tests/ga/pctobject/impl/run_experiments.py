


from pct.experiments import CometExperimentManager
import os

"""

python -m impl.run_experiments

"""


# Initialize the manager
workspace = 'lunarlandercontinuous-v2'

manager = CometExperimentManager(workspace=workspace)

projects = manager.get_workspace_projects()
print(f"Projects in workspace '{workspace}':", projects)

# project_name = 'refinputs-currentrms'
# score_threshold=0.05
# project_name = 'reward-summed'
# project_name = 'inputs-rms'
# project_name = 'refinputs-smooth'

num_runs=100

for project_name in projects:
    if project_name == 'general' or project_name == 'test':
        continue
    
    max = False
    score_threshold=0.05

    if project_name == 'reward-summed' or project_name == 'opt-reward-summed':
        score_threshold=100
        max = True

    # Test get_all_artifacts_sorted
    artifact_results = manager.get_all_artifacts_indexed()
    # print("Artifacts sorted by source experiment key:", artifacts)

    # Test get_experiments_by_metrics
    experiments = manager.get_experiments_by_metrics(project_name=project_name, score_threshold=score_threshold, reward_threshold=10.0, max=max)
    # print("Filtered experiments:", experiments)

    output_csv = f'/tmp/artifacts/experiment_results_{project_name}.csv'
    if os.path.exists(output_csv):
        print(f"{output_csv} already exists, skipping...")
        continue
    manager.run_experiments_and_record_results(experiments=experiments, project_name=project_name, artifact_results=artifact_results, num_runs=num_runs, output_csv=output_csv)
    print(f"Results saved to {output_csv}")




