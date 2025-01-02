---
title: "Syncing and Backups with Rsync and Borg"
description: "Creating a self-hosted remote backup for data recovery"
publish_date: 2025-01-02
tags: [blog, 100DaysToOffload]
---

![Borg And Rsync](../../images/borg_and_rsync.png)

# Syncing and Backups with Rsync and Borg
I have a relatively simple self-hosting setup at home. My biggest and most important service is [Nextcloud](https://nextcloud.com). For quite some time, I've been running this with basically no backup, which is super risky, and I was starting to fear the day when the SSD fails. So to save myself from worrying, and save my previous photos and documents at some future date of failure, I decided to take some action while I was home for the holidays and had a little free time.

## Cloud vs. Local
I considered a couple options for backups. One would be cloud provider solution, such as [BackBlaze](https://www.backblaze.com/) or [Rsync.net](https://www.rsync.net/),  but I didn't think that was a good fit for a couple reasons. First, it's expensive, BackBlaze would be $12/mo for 2TB, and then more money any time you need to recover your data. Micro Center was selling a [2TB Hard Drive for $80](https://www.microcenter.com/product/629580/toshiba-canvio-advance-2tb-usb-31-(gen-1-type-a)-25-portable-external-hard-drive-red), amortized over a year of use, that would come out to < $6/mo. So if I can get more than 6 months from a drive at that price point, it would be a better deal than BackBlaze already.

So with that knowledge, I purchased a Toshiba Canvio 2TB Hard Drive at an even better deal of $70 at a Micro Center brick-and-morter store. One of the reasons I wanted to do this while I was home for the holidays is so I could setup my backup device in a different location than my actual server to satisfy the "1 copy off-site" part of the [3-2-1 Rule](https://www.veeam.com/blog/321-backup-rule.html). 

I also picked up a Raspberry Pi 5 with 4GB of memory, and a couple accessories to get things fully set up.
## The Process

After doing a little research on file synchronization and backups, I came up with a two-step process to backup all my docker volumes. This way if something were to fail on my local device, I could restore it from the offsite backup, or even roll back to an old backup. The nice thing about having it all containerized is that, as long as I have my docker volumes and docker compose files, restoring the server should be fairly straightforward.

I'm relying on two neat utilities called [Rsync](https://rsync.samba.org/) and [Borg](https://www.borgbackup.org/) which provide file synchronization and backup tools respectively. I use Rsync to transfer files over ssh to my offsite machine, then Borg to create a snapshot every week.

## Backup Script
You can find the complete script [here](https://gist.github.com/momja/83531e6af416d2afd207eaa5fca2572d). Below is an illustrative version of the code.

```python
# ----------------------
# Abridged Backup Script
# ----------------------
remote_backup_dir = os.getenv("REMOTE_BACKUP_DIR")
local_backup_dir = os.getenv("LOCAL_BACKUP_DIR")
borg_repo_dir = os.getenv("BORG_REPO_DIR")
backup_drive = os.getenv("BACKUP_DRIVE")

def mount_drive():
    run_command("mount /dev/sda1 /mnt/backup")


def sync_files():
    rsync_command = (
        f"rsync -az --delete --exclude-from='/etc/backup-config/exclude-file.txt' -e 'ssh -c aes128-ctr' {remote_backup_dir} {local_backup_dir}"
    )
    output = run_command(rsync_command, False)
    logging.info(f"Rsync output:\n{output}")


def backup_files():
    logging.info("Backing up files...")
    borg_command = (
        f"borg create --stats --progress "
        f"{borg_repo_dir}::dockerData-{{now}} "
        f"{local_backup_dir}"
    )
    output = run_command(borg_command)
    logging.info(f"Borg output:\n{output}")


def unmount_drive():
    run_command("umount /mnt/backup")


def main():
    parser = # setup parser
    args = parser.parse_args()

    if not args.sync and not args.backup:
        logging.error('Either --sync, --backup, or both must be specified.')
        sys.exit(1)

    try:
        mount_drive()
        if args.sync:
            sync_files()
        if args.backup:
            backup_files()
    finally:
        unmount_drive()


if __name__ == "__main__":
    main()
```

In order for the backup script to work, you need to add some environment variables. I provide these in a `.env` file, but you could also add to a `.bashrc` file or just provide on each run.
```sh
REMOTE_BACKUP_DIR=you@computer:/path/to/data/
LOCAL_BACKUP_DIR=/mnt/backup/data
BORG_REPO_DIR=/mnt/backup/data_borg
BACKUP_DRIVE=/dev/sda1
```

Before running, make sure you set correct permissions on both servers, and configure an ssh key for the offsite machine to access the main server.

To automate the execution of the sync and backup, I've set up two cron jobs. One that runs on Sundays and performs synchronizations and snapshots. Then another that runs every other day and just performs synchronization. My idea is that if I were to break something on my primary server while doing some configuration or testing, the Rsync mirror will allow me to recover to a valid state, or repair accidentally deleted data. If something worse happens, like my SSD gets corrupted, I can restore from the Borg Snapshots, which is a little slower and a little more work.

## Conclusion

This is not a perfect solution, it's not even foolproof. But it seems to work OK now. I have a little more testing to do before I'm comfortable with it, but it does feel like I can breath a little easier knowing if I F\*\*k something up, I'll *probably* be able to recover from it. The next logical step would be to buy another drive so the offsite backup and synchronized repositories are on separate disks, then set up alerts to monitor for a failure so I don't need to manually check it. I'm not going to mess around with RAID right now, but maybe some day.

Now, going back to the provider solution for a second. I still think it's a good idea to store your data with a secure cloud for another layer of redundancy, it's just not my first choice. Part of the reason I'm trying to better protect my data is because my family is running into issues with Amazon Photos and the [lack of control](https://www.reddit.com/r/gsuitelegacymigration/comments/uhzseu/comment/i79p2sn/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) they give their users. So it just didn't feel right to rely on another cloud provider for a backup solution.
