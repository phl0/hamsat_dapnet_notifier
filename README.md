# hams.at DAPNET Notifier

This simple python script can be executed as a cronjob and pulls activations from [hams.at](https://hams.at/). Sends out a [DAPNET](https://hampager.de/#/) notification in case of new and workable activations.

# Requirements:

- [DAPNET-API by DO1FFE](https://github.com/DO1FFE/DAPNET-API)
- [hams.at](https://hams.at/) and [DAPNET](https://hampager.de/#/) account

Please limit the range for the sent DAPNET messages to as small transmitter groups as possible! Sending the notifications to all transmitters is wasting air time for all other users of DAPNET.
