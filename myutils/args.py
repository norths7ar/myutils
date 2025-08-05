import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run LLM benchmark or production mode.")
    parser.add_argument("-n", "--max_items", type=int, default=None,
                        help="Maximum number of items to process")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Overwrite output file if exists")
    return parser.parse_args()

def parse_args_benchmark():
    """Parse command line arguments for benchmark"""
    parser = argparse.ArgumentParser(description="Run LLM benchmark or production mode.")
    parser.add_argument("-n", "--sample_size", type=int, default=50,
                        help="Sample size for the benckmark")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Overwrite output file if exists")
    parser.add_argument("--task", type=str, default="q2",
                        help="Name of the test task to run (e.g., q1, q2...)")
    return parser.parse_args()
