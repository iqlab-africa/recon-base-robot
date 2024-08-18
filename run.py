import os, sys
import time
import subprocess
import shutil

from read_database import start_reading_database

COLLECTOR = 'rcc task run --robot robot.yaml  --account robocorp-code --task PlayerCollectorTask --controller RobocorpCode'
HANDLER = "rcc task run --robot robot.yaml  --account robocorp-code --task PlayerHandlerTask --controller RobocorpCode"
BESTPLAYER = "rcc task run --robot robot.yaml  --account robocorp-code --task BestPlayerTask --controller RobocorpCode"

command = sys.argv[1:]

tag = "🌺🌺🌺🌺🌺🌺 RobRunner 🌺"


def start():
    print(f"\n\n{tag} Robot automation script starting ...\n")

    start_time = time.time()

    subprocess.run(COLLECTOR, shell=True)
    print(f"\n\n\n{tag} PlayerCollectorRobot has completed, should copy workitems folder ...")

    copy_folder(collector_workitems_folder, handler_workitems_folder)
    print(
        f"\n\n{tag} PlayerCollectorRobot has completed, should start PlayerHandlerRobot\n"
    )

    subprocess.run(HANDLER, shell=True)
    print(f"\n\n{tag} PlayerHandlerRobot has completed, should start BestPlayerRobot")

    copy_folder(handler_workitems_folder, bestplayer_workitems_folder)

    subprocess.run(BESTPLAYER, shell=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    msg = 'Elapsed time: {:.1f} seconds'.format(elapsed_time)

    print(f"\n\n{tag} {msg} ")
    print(f"\n{tag} BestPlayerRobot has completed, work is finished, Boss!\n\n")
    
    start_reading_database()


def copy_folder(source_folder, destination_folder):
    print(f'\n\n{tag} copying folder {source_folder} to {destination_folder}')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(destination_folder, item)
        print(
            f"{tag} 🥦🥦 source_item: 🔵 {source_item} destination_item: 🔵 {destination_item}"
        )
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)


collector_workitems_folder = "output/collector"
handler_workitems_folder = "output/handler"
bestplayer_workitems_folder = "devdata/bestplayer"

# os.environ["RC_WORKITEM_INPUT_PATH"] = "devdata/bestplayer/work-items.json"


start()

import subprocess
