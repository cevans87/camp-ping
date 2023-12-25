# Overview

Camp Ping should be run as a cron job to check all configured websites for new availability.

Camp Ping checks for new openings on specified sites. It is stateful. The results of the most recent execution
are [memoized](https://github.com/cevans87/atools/#memoize) to disk.

Example for checking [Middle Fork Of The Salmon (4 Rivers)](https://www.recreation.gov/permits/234623) and [Hells
Canyon - Snake River (4 Rivers)](https://www.recreation.gov/permits/234625):

```bash
camp-ping --ccs cevans87 --notify-threads cevans87/camp-ping/discussions/2 --permits recreation.gov:234623,234625
```

If any openings have appeared since last `run`, text notifications will be posted to the given github thread, cc'd 
to given `--cc` arguments.

## Minimum Viable Product (MVP)

### Installation

This is an example minimal workflow for this tool.

```bash
crontab -e
```

Create a cron job that runs every 5 minutes.

```text
*/5 * * * * camp-ping --notify-threads cevans87/camp-ping/discussions/2 --permits recreation.gov:234623,234625
```

This will cause Camp Ping to check given permits every five minutes.

## Structure

CLI commands will be laid out as follows.
```text
.
|- clean
|
|- get
|  |- grcariverpermits_nps_gov
|  |- parks_wa_gov
|  |- recreation_gov
|
|- list
|  |- grcariverpermits_nps_gov
|  |- parks_wa_gov
|  |- recreation_gov
|
|- log

```

## Stretch Goals

### Cloud Cron Job

Instead of running the script as a local cron job, run as
a [`schedule`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) GitHub Action.

### SMS Notification

Similar to the functionality of the `--notify-threads` flag, this will cause CampPing to post notifications for 
newly-available permits to the given phone number.

### SMS Interface

CLI commands may be invoked via a text message. Output of CLI commands is sent back via text response.

This requires an SMS bot to listen for text messages and transform them into 

### Email Notification

Similar to the functionality of the `--notify-threads` flag, this will cause CampPing to post notifications for
newly-available permits to the given email address.
