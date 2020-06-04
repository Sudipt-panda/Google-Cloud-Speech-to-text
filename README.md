# Google-Cloud-Speech-to-text
Implementation of Google Cloud Speech to text on local machine

This repo contains the implementation of Google-cloud-speech-to-text API with speaker diarization.
The Dataset in use is AMI corpus which can be downloaded from [Here] (http://groups.inf.ed.ac.uk/ami/download/). Select all the AMI meetings, and download the "mix-headset" audio files. You can also use the files from the data folder (to update).
Then create your own GCP account, create a bucket to store the files on cloud, using the "cloud_multiple_upload.py" file.
Then enable the Google-cloud-speech-to-text API in your GCP account.
Then run the "stt_gcloud_final.py" to generate the transcripts.The transcripts are stored locally in the path provided by you. You can check the generated outputs in the output folder.
