from google.cloud import speech_v1p1beta1
from google.cloud import storage
import io
import os
import pandas as pd

def sample_long_running_recognize(filename):
    """
    Print confidence level for individual words in a transcription of a short audio
    file
    Separating different speakers in an audio file recording
    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Sudipt Panda/Downloads/crafty-calling-274812-40d0f3d2adb9.json"

    client = speech_v1p1beta1.SpeechClient()

    transcripts = pd.DataFrame(columns = ['Transcripts'])
    word_speaker = pd.DataFrame(columns = ['Speaker','Word'])
    
    Speaker_Transcripts = pd.DataFrame(columns = ['Speaker','Transcripts'])

    storage_uri = 'gs://theseis_audio/' + str(filename)

    # local_file_path = 'resources/commercial_mono.wav'

    # If enabled, each word in the first alternative of each result will be
    # tagged with a speaker tag to identify the speaker.
    enable_speaker_diarization = True

    # Optional. Specifies the estimated number of speakers in the conversation.
    diarization_speaker_count = 4

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": diarization_speaker_count,
        "language_code": language_code,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        # First alternative has words tagged with speakers
        alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript))
        transcripts=transcripts.append({'Transcripts': str(alternative.transcript)},ignore_index = True)

        # Print the speaker_tag of each word
        for word in alternative.words:
            # print(u"Word: {}".format(word.word))
            # print(u"Speaker tag: {}".format(word.speaker_tag))
            word_speaker=word_speaker.append({'Speaker':word.speaker_tag,'Word':str(word.word)},ignore_index= True)
        sentence = ''
        # x= len(Speaker_Transcripts.index)
        speaker = str(word_speaker['Speaker'].iloc[0])

        for index, row in word_speaker.iterrows():  
            # if x == 0:
            #     speaker = str(row["Speaker"])
            # else:
            #     speaker = Speaker_Transcripts['Speaker'].iloc[x-1]
            
            # print(row['Speaker'])

            # print(speaker)

            if str(row['Speaker']) == speaker:
                sentence = sentence +' ' +str(row["Word"])
                # print('match')
            else:
                Speaker_Transcripts= Speaker_Transcripts.append({'Speaker': speaker , 'Transcripts':sentence},ignore_index=True)
                # x+=1
                sentence = str(row["Word"])
                speaker = str(row['Speaker'])
                # print('change')
    # print(Speaker_Transcripts)
    transcripts_path = 'C:/Users/Sudipt Panda/Downloads/thesis/Speaker_Transcripts/' + str(filename)[:-4]+ '.csv'
    Speaker_Transcripts.to_csv(transcripts_path,index=True)    

                
            


# [END speech_transcribe_diarization_beta]


def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Sudipt Panda/Downloads/crafty-calling-274812-40d0f3d2adb9.json"


    client1 = storage.Client()
    BUCKET_NAME = 'theseis_audio'
    bucket = client1.get_bucket(BUCKET_NAME)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name + ' starting')
        sample_long_running_recognize(blob.name)
        print('end')

    # sample_long_running_recognize('ES2002a.Mix-Headset.wav')

if __name__ == "__main__":

    main()