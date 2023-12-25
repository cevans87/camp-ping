# CampPing

**NOTE** This is pre-emptinve documentation. None of this functionality exists. This documentation currently exists as a
way to direct development of the project.

## Usage

This is a bot. It won't work for you unless you know the bot's secret phone number and the bot knows your secret phone
number. Open an issue if you'd like the bot to notify you of openings on the supported reservable recreational sites.

All of these commands can be texted to the bot's phone number and 

### Subscribing

## Supported Sites

- TODO (whichever site is for Middle Fork of the Salmon River)
- TODO (whichever site is for Grand Canyon)
- TODO (whichever site is for Deception Pass)

## Developing

### Prerequisites

Install apt requirements.

```Bash
sudo apt update && cat apt_requirements.txt | xargs sudo apt install
```

Install pip requirements.

```Bash
python3 -m pip install .[base]
```

### Testing

```Bash
python3 -m pip install .[test]
python3 -m pytest
```
