from neutts import NeuTTS
import soundfile as sf
import torch

def main():

    # Determine device based on CUDA availability
    try:

        device = "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        device = "cpu"

    tts = NeuTTS(
        backbone_repo="neuphonic/neutts-air", backbone_device=device,
        codec_repo="neuphonic/neucodec",      codec_device=device,
    )

    ref_codes = tts.encode_reference("jo.wav")
    ref_text  = open("jo.txt").read().strip()

    wav = tts.infer("Hello I am saul. I am a helpful assistant.", ref_codes, ref_text)
    sf.write("jo-test.wav", wav, 24000)
    print("wrote jo-test.wav")

if __name__ == "__main__":
    main()
