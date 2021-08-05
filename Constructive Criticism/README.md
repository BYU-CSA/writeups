# UIUCTF 2021 - Constructive Criticism Writeup

- Type - Misc
- Name - Constructive Criticism
- Points - 408

## Description

> Checkout this playlist from a new soundcloud artist I found: https://soundcloud.com/nick-carraway-43926894/sets/lofi-beats-to-hack-with/s-83uzJdlwz3H
>
> He made a mix of some good songs to vibe with while you hack away. Download the songs if you want to listen offline!
>
> author: Pranav Goel
>
> > Hint:
> > Stereo is pretty cool if you look into it...

## Writeup

### Listening to "Cursed Mode" Beats

We're given a link to a soundcloud playlist. The playlist contains 20 songs of lofi beats. Let's give them a listen.

Almost immediately, something seems wrong. With the first song, every few seconds or so, the audio will change to what I will refer to as "cursed mode", and then change back some seconds later. This had some fun effects on the people who listened to it. One told me it sounded like the sound was coming from six feet off to the left. Another said it just sounded louder in one ear than the other.

### Uncovering the Cause

Let's download these songs and see what's causing cursed mode.

Here's a view of the waveforms at a key point in the first song:

![Audacity shows the second channel flipping](#) <!-- TODO: Add screen grab -->

As we can see, at some point, the first two channels seem to be the same, then they abruptly switch to being opposite. Each of the switching points matches up with changing into and out of cursed mode.

### Viewing the Data

Using Python, we'll try and crack this cursed mode open.

```python
from scipy.io import wavfile

file_name = 'Ambulo x Kasper Lindmark – Pleasant_track_1.wav'
samplerate, samples = wavfile.read(file_name)
print(samples)
print(samples[4000:4005])
print(samples[200000:200005])
```

```
[[ 0  0  0]
 [ 0  0  0]
 [ 0  0  0]
 ...
 [ 0  0  0]
 [-1  1  1]
 [-1  1  1]]
[[ 151  151 -151]
 [ 157  157 -157]
 [ 162  162 -162]
 [ 169  169 -169]
 [ 178  178 -178]]
[[-5898  5898  5898]
 [-5819  5819  5819]
 [-5790  5790  5790]
 [-5835  5835  5835]
 [-5822  5822  5822]]
```

What we can see here is essentially the "heights" of the waveforms at each sample, which we saw visually in Audacity. The song starts out quiet, ends quiet, and has normal modes (first and second channel are equal) and cursed modes (first and second channel are opposite). Let's see if we can find where the first cursed mode starts, and how far it is through the file:

```python
from scipy.io import wavfile

file_name = 'Ambulo x Kasper Lindmark – Pleasant_track_1.wav'
samplerate, samples = wavfile.read(file_name)

for i, sample in enumerate(samples):
    if sample[0] != sample[1]:
        print(f'{i} : {len(samples)/i}')
        exit()
```

```
174576 : 24.001924663183942
```

That's a strange number, but it is about 1/24 of the way through the song. A bit too close for coincidence. In fact, looking at the next couple songs gives similarly strange numbers for "first cursed mode", but the numbers occur nearly 1/24 of the way through their songs.

### Piecing it together

It was at this point when we pieced it together: normal mode is a 1 or a 0, and cursed mode is the other. At this point, the challenge (with the benefit of hind sight) is merely scripting.


```python
from scipy.io import wavfile

def guess_bits(file):
    string_of_bits = ""
    samplerate, samples = wavfile.read(file)

    currently_same = True
    last_change = 0
    change_amount = 0
    for i, sample in enumerate(samples): # loop through each sample
        if sample[0] == 0:
            continue # we won't be able to tell inversion on zero
            # This is where hindsight comes in
        if currently_same and sample[0] != sample[1]:
            if change_amount == 0: # if this is the first change
                change_amount = i
            string_of_bits += "0" * ((i-last_change)//change_amount)
            currently_same = not currently_same
            last_change = i
            continue
        if not currently_same and sample[0] == sample[1]:
            string_of_bits += "1" * ((i-last_change)//change_amount)
            currently_same = not currently_same
            last_change = i
            continue

    string_of_bits += ("0" if currently_same else "1") * ((i-last_change)//change_amount)
    return string_of_bits

if __name__ == "__main__":
    print(guess_bits("Ambulo x Kasper Lindmark – Pleasant_track_1.wav"))
    print(guess_bits("BVG x møndberg – insomnia_track_2.wav"))
    print(guess_bits("Bcalm x Banks – Because_track_3.wav"))
    print(guess_bits("Dontcry x Glimlip x Sleepermane - Jiro Dreams_track_4.wav"))
    print(guess_bits("Flovry x tender spring - First Heartbreak_track_5.wav"))
    print(guess_bits("Hoogway – Everything (You are)_track_6.wav"))
    print(guess_bits("Ky akasha – Memory Within A Dream_track_7.wav"))
    print(guess_bits("Loafy Building x Hoffy Beats – Sleepless Wonder_track_8.wav"))
    print(guess_bits("Mila Coolness – Far Away_track_9.wav"))
    print(guess_bits("Miramare x Clément Matrat – Foam_track_10.wav"))
    print(guess_bits("S N U G – Dreams of You_track_11.wav"))
    print(guess_bits("Softy x Kaspa_track_12.wav"))
    print(guess_bits("Tenno – Daydreaming_track_13.wav"))
    print(guess_bits("WYS – Snowman_track_14.wav"))
    print(guess_bits("brillion_track_15.wav"))
    print(guess_bits("brillion_track_16.wav"))
    print(guess_bits("drkmnd - Satellite Nights_track_17.wav"))
    print(guess_bits("less_track_18.wav"))
    print(guess_bits("no one's perfect x Kanisan – Gentle Wind_track_19.wav"))
    print(guess_bits("tysu x Spencer Hunt – Rainy Day_track_20.wav"))
```

```
011101010110100101110101                        
011000110111010001100110                        
011110110110110001101111                        
011001100110100101011111                        
011000100110111101110000                        
011100110101111101100010                        
011101010111010001011111                        
011001010110111001100011                        
011100100111100101110000                        
011101000110100101101110                        
011001110101111101100001                        
011101010110010001101001                        
011011110101111101110101                        
011100110110100101101110                        
011001110101111101101001                        
011011100111010001100101                        
011100100110011001100101                        
011100100110010101101110                        
011000110110010101011111                        
011100110110110001100001011100000111001101111101
```

It's a small matter to guess that this is ASCII, and convert it into a flag.

### Not done yet!

This exploit runs in over 13 minutes. We can improve on that. We know these bits come at regular times, and the first two bits are always `01` for each file. We can leverage this to great effect:

```python
from scipy.io import wavfile

def guess_bits(file_name):
    string_of_bits = ""
    samplerate, samples = wavfile.read(file_name)

    change_amount = None
    for i, sample in enumerate(samples): # loop through each sample
        if sample[0] != sample[1]: # We found a jump
            change_amount = i
            break

    for i in range(0, len(samples) - change_amount, change_amount):
        string_of_bits += "0" if samples[i][0] == samples[i][1] else "1"

    return string_of_bits

if __name__ == "__main__":
    print(guess_bits("Ambulo x Kasper Lindmark – Pleasant_track_1.wav"))
    print(guess_bits("BVG x møndberg – insomnia_track_2.wav"))
    print(guess_bits("Bcalm x Banks – Because_track_3.wav"))
    print(guess_bits("Dontcry x Glimlip x Sleepermane - Jiro Dreams_track_4.wav"))
    print(guess_bits("Flovry x tender spring - First Heartbreak_track_5.wav"))
    print(guess_bits("Hoogway – Everything (You are)_track_6.wav"))
    print(guess_bits("Ky akasha – Memory Within A Dream_track_7.wav"))
    print(guess_bits("Loafy Building x Hoffy Beats – Sleepless Wonder_track_8.wav"))
    print(guess_bits("Mila Coolness – Far Away_track_9.wav"))
    print(guess_bits("Miramare x Clément Matrat – Foam_track_10.wav"))
    print(guess_bits("S N U G – Dreams of You_track_11.wav"))
    print(guess_bits("Softy x Kaspa_track_12.wav"))
    print(guess_bits("Tenno – Daydreaming_track_13.wav"))
    print(guess_bits("WYS – Snowman_track_14.wav"))
    print(guess_bits("brillion_track_15.wav"))
    print(guess_bits("brillion_track_16.wav"))
    print(guess_bits("drkmnd - Satellite Nights_track_17.wav"))
    print(guess_bits("less_track_18.wav"))
    print(guess_bits("no one's perfect x Kanisan – Gentle Wind_track_19.wav"))
    print(guess_bits("tysu x Spencer Hunt – Rainy Day_track_20.wav"))
    print()
```

```
011101010110100101110101011000110111010001100110011110110110110001101111011001100110100101011111011000100110111101110000011100110101111101100010011101010111010001011111011001010110111001100011011100100111100101110000011101000110100101101110011001110101111101100001011101010110010001101001011011110101111101110101011100110110100101101110011001110101111101101001011011100111010001100101011100100110011001100101011100100110010101101110011000110110010101011111011100110110110001100001011100000111001101111101
```

... runs in under 4 seconds.

## Real-World Application

Rather miscellaneous. As far as steganography goes, it's a bit obvious. It might be a bit more sutle to subtract a known amount from one channel to get the other. As far as a challenge goes, it's very cool to see a message hidden inside sound, and it felt good to have the very familiar ASCII encoding pop out in the end. I haven't done anything like this before.