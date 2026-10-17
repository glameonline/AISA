# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "soundfile"]
# ///
"""VO edit: keep the natural read, open a little air between problem / need / offer, and land
"Content" on the music's drop. Writes audio/vo.wav and vo_words.json (film-time word list)."""
import json, subprocess, numpy as np, soundfile as sf
from pathlib import Path
D = Path(__file__).parent
SR = 48000
src, tmp = D / 'vo' / 'altair2.mp3', D / 'vo' / 'altair2_48k.wav'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(src), '-ac', '1', '-ar', str(SR), '-af',
                'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2', str(tmp)], check=True)
x, _ = sf.read(tmp)
words = json.load(open(D / 'words_raw.json'))
B = json.load(open(D.parent / 'beats.json'))
P, OFF, DUR = B['period'], B['offset'], B['duration']
drop = next(s['beat'] for s in B['sections'] if s['name'] == 'main')
EXTRA = {'What': 0.55, "That's": 0.45}          # breathing room between the three acts
START = 0.12

# three acts cut at sentence starts; the read inside each act is left untouched
cuts = ['Running', 'What', "That's"]
acts, cur = [], []
for w in words:
    if w[0] in cuts and cur: acts.append(cur); cur = []
    cur.append(w)
acts.append(cur)
place, t = [], START - (acts[0][0][1] - 0.03)
for a in acts:
    t += EXTRA.get(a[0][0], 0); place.append(t)
cw = next(w for w in acts[-1] if w[0] == 'Content')
place[-1] = (OFF + drop * P) - cw[1]
print(f'drop beat {drop} at {OFF + drop * P:.2f}s')
out, new = np.zeros(int(DUR * SR) + SR), []
for i, (a, dt) in enumerate(zip(acts, place)):
    s0 = a[0][1] - 0.03
    s1 = min(a[-1][2] + 0.12, (acts[i + 1][0][1] - 0.02) if i + 1 < len(acts) else 1e9)
    seg = x[int(s0 * SR):int(s1 * SR)].copy()
    f, g = int(0.008 * SR), int(0.04 * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-g:] *= np.linspace(1, 0, g)
    i0 = int((s0 + dt) * SR); out[i0:i0 + len(seg)] += seg
    new += [{'w': w[0], 't0': round(w[1] + dt, 3), 't1': round(w[2] + dt, 3)} for w in a]
out = out[:int(DUR * SR)]
out = out / np.abs(out).max() * 0.89
sf.write(D / 'vo_dry.wav', np.stack([out, out], 1), SR)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(D / 'vo_dry.wav'), '-af',
                'acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90:makeup=2,alimiter=limit=0.9',
                '-ar', str(SR), str(D / 'vo.wav')], check=True)
json.dump(new, open(D.parent / 'vo_words.json', 'w'))
print('speech', new[0]['t0'], '->', new[-1]['t1'], ' film', DUR)
print(' '.join(f"{w['w']}@{w['t0']}" for w in new))
