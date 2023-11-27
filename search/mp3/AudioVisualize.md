# AudioVisualize

**AudioVisualize** is a 3 kB JavaScript module that leverages the power of the Web Audio API to visualize and analyze audio in your web applications. It provides an easy-to-use interface for loading audio, extracting audio data, and creating visualizations. Check out these [examples](#examples) to learn how to bring your audio data to life with some simple visuals.


## Possibilities

- **Real-time Visualization:** Create real-time visualizations of audio, including frequency spectrum analysis.
- **Customizable:** Adjust the audio analysis parameters to focus on the aspects that matter most to your application.

## Installation

Easily install **AudioVisualize** via npm…

```bash
npm i audiovisualize
```

…or import the script from a CDN.

```html
<script type="module">
import { AudioVisualize } from "https://unpkg.com/audiovisualize";
</script>
```
```html
<script type="module">
import { AudioVisualize } from "https://cdn.jsdelivr.net/npm/audiovisualize@1.1.1/audiovisualize.min.js"
</script>
```

## Usage

You can create an instance of the **AudioVisualize** object and use its methods to load, analyze, and visualize audio. Use the *loading* method to load an audio file and set up event listeners for loading progress and playback events. Call the *initialize* method to set up the audio nodes for analysis.

```javascript
// Create an instance of the AudioVisualize object.
const av = AudioVisualize;

av.loading(
  // Path to your audio file
  'path-to-your-audio-file.mp3',
  () => {
    // Audio loaded callback
    console.log('Audio loaded');
  },
  (event) => {
    // Progress update callback
    console.log('Update event:', event);
  },
  () => {
    // Audio ended callback
    console.log('Audio ended');
  }
);

// Create your custom audio visualizations here
```

When the **AudioVisualize** object is initialized, `av.element` is created as an instance of an HTML [`<audio>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio) that serves as the core component for loading, playing, and controlling audio files within a web page.

You can use the getFrequencies method to get the frequency data of the audio at any given moment. It returns an array of frequency values within a specified range.

```javascript
const lowFrequency = 20;  // Minimum frequency in Hz
const highFrequency = 20000;  // Maximum frequency in Hz

const frequencies = av.getFrequencies(lowFrequency, highFrequency); // `frequencies` is an array of frequency data.
```

If you want to get the average frequency range over the entire audio track, you can use the getAverageRange method. This method will analyze the audio frame by frame and calculate the average over the specified frequency range.

```javascript
const averageLowFrequency = 100;  // Minimum frequency in Hz
const averageHighFrequency = 2000;  // Maximum frequency in Hz

av.getAverageRange(averageLowFrequency, averageHighFrequency).then((average) => {
  console.log('Average range over time:', average);
});
```

Adjust the frequency resolution, the FFT size, used for audio analysis. Default value is *2048*

```javascript
av.fftSize = 512;
```

Retrieve the sample rate of the audio context used, providing essential information about the rate at which audio data is processed. This value can be used to ensure accurate audio analysis and visualizations in your web applications.

```javascript
console.log(av.audioContext.sampleRate);
```

## Examples

**Example 1**

```html
<canvas id="canvasElement"></canvas>

<script type="module">
import { AudioVisualize } from 'https://unpkg.com/audiovisualize';

const av = AudioVisualize;

av.loading(
  'path-to-your-audio-file.mp3',
  () => {
    console.log('Audio duration', av.element.duration);
    // Add the audio element to the body
    document.body.appendChild(av.element);
    av.element.setAttribute('controls', 'controls');
  },
  () => {
    console.log('Buffered', av.element.buffered);
    console.log('Current time', av.element.currentTime);
  },
  () => {
    console.log('Audio ended', av.element.currentTime, av.element.duration);
  }
);

const canvas = document.getElementById('canvasElement');
const ctx = canvas.getContext("2d");

function draw() {
  if(!av.element.paused){
    av.getFrequencies();
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw the waveform
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i < av.spectrum.length; i++) {
      const x = (canvas.width / av.spectrum.length) * i;
      const y = canvas.height - (canvas.height * av.spectrum[i]) / 255;
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.stroke();
  }
  // Request the next animation frame
  requestAnimationFrame(draw);
}

// Start the animation loop
draw();

</script>
```

**Example 2**

```html
<canvas id="canvasElement"></canvas>

<script type="module">
import { AudioVisualize } from 'https://unpkg.com/audiovisualize';

const av = AudioVisualize;

av.loading(
  'path-to-your-audio-file.mp3',
  () => {
    console.log('Audio duration', av.element.duration);
    // Add the audio element to the body
    document.body.appendChild(av.element);
    av.element.setAttribute('controls', 'controls');
  },
  () => {
    console.log('Buffered', av.element.buffered);
    console.log('Current time', av.element.currentTime);
  },
  () => {
    console.log('Audio ended', av.element.currentTime, av.element.duration);
  }
);

const canvas = document.getElementById('canvasElement');
const ctx = canvas.getContext("2d");

function draw() {
  if (!av.element.paused) {
    // Calculate the average frequencies for bass, mids, and treble
    const bassFrequency = av.getAverageBetweenFrequencies(20, 250); // Adjust the range for bass
    const midFrequency = av.getAverageBetweenFrequencies(250, 1500); // Adjust the range for mids
    const trebleFrequency = av.getAverageBetweenFrequencies(1500, 20000); // Adjust the range for treble

    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the bass line
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 1;
    ctx.beginPath();
    const x1 = canvas.width / 4; // Position for bass
    const y1 = canvas.height - (canvas.height * (bassFrequency / 255));
    ctx.moveTo(x1, canvas.height);
    ctx.lineTo(x1, y1);
    ctx.stroke();

    // Draw the mid line
    ctx.strokeStyle = "green";
    ctx.lineWidth = 1;
    ctx.beginPath();
    const x2 = canvas.width / 2; // Position for mids
    const y2 = canvas.height - (canvas.height * (midFrequency / 255));
    ctx.moveTo(x2, canvas.height);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // Draw the treble line
    ctx.strokeStyle = "red";
    ctx.lineWidth = 1;
    ctx.beginPath();
    const x3 = (canvas.width * 3) / 4; // Position for treble
    const y3 = canvas.height - (canvas.height * (trebleFrequency / 255));
    ctx.moveTo(x3, canvas.height);
    ctx.lineTo(x3, y3);
    ctx.stroke();
  }
  // Request the next animation frame
  requestAnimationFrame(draw);
}

// Start the animation loop
draw();

</script>
```
