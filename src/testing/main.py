import subprocess
import data_handler


if __name__ == "__main__":
    data_handler.setup_data()
    subprocess.run(['pytest', '-v', '-s', '--html=report.html'])
