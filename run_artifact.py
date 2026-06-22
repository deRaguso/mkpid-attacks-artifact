import argparse
from math import ceil
from time import time
from os import makedirs
from os.path import join, exists
import datetime

from measure_PSU import measure_PSU_PSUCA_experiments
from run_leakage_experiments import run_leakage_experiments


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-e", "--experiments_directory", required=True)
	parser.add_argument("-o", "--out_directory", required=True)
	parser.add_argument("-r", "--repetitions", required=True)
	parser.add_argument("-i", "--core_id", required=True)
	parser.add_argument("-c", "--num_cores", required=True)
	parser.add_argument("-s", "--silent", action="store_true")
	parser.add_argument("--omit_appendix", action="store_true")
	parser.add_argument("--m_PSU", required=True)
	parser.add_argument("--m_PSUCA", required=True)
	args = parser.parse_args()
	
	experiments_directory = args.experiments_directory
	out_directory = args.out_directory
	m_PSU = int(args.m_PSU)
	m_PSUCA = int(args.m_PSUCA)
	repetitions = int(args.repetitions)
	core_id = int(args.core_id)
	num_cores = int(args.num_cores)
	silent = args.silent
	omit_appendix=args.omit_appendix

	assert num_cores > 0

	if core_id < 0 or core_id >= num_cores:
		quit()

	if not exists(out_directory):
		makedirs(out_directory)

	log_file = join(join(out_directory, "cores.log"))
	with open(log_file, "a") as f:
			f.write(f"{datetime.datetime.now()}: \t core {core_id} starting\n")

	start_time = time()

	if num_cores == 1:
		print(f"core {core_id}: all experiments")
		run_leakage_experiments(experiments_directory, out_directory, repetitions, core_id, num_cores=num_cores, silent=silent, omit_appendix=omit_appendix)
		measure_PSU_PSUCA_experiments(out_directory, m_PSU, m_PSUCA, repetitions, core_id, num_cores, silent=silent, omit_appendix=omit_appendix)
	else:
		# distribute PSU/PSU-CA experiments among first 11 cores or all cores if less are available
		num_PSU_cores = min(11, num_cores)

		if core_id < num_PSU_cores:
			print(f"core {core_id}: PSU/PSU-CA experiments")
			measure_PSU_PSUCA_experiments(out_directory, m_PSU, m_PSUCA, repetitions, core_id, num_cores=num_PSU_cores, silent=silent, omit_appendix=omit_appendix)
		
		print(f"core {core_id}: leakage experiments")
		run_leakage_experiments(experiments_directory, out_directory, repetitions, core_id, silent=silent, num_cores=num_cores, omit_appendix=omit_appendix)

		end_time = time()
		with open(log_file, "a") as f:
			f.write(f"{datetime.datetime.now()}: \t core {core_id} done, runtime: {datetime.timedelta(seconds=(end_time-start_time))}\n")