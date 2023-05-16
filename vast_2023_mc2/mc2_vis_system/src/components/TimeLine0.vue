<template>
  <form ref="form" style="font-size: 12px; font-variant-numeric: tabular-nums; display: flex; height: 33px; align-items: center;">
    <button ref="button" name=b type=button style="margin-right: 0.4em; width: 5em;"></button>
    <label ref="label" style="display: flex; align-items: center;">
      <input ref="input" name=i type=range min=0 max={{times}} value=${initial} step=1 style="width: 180px;">
      <output ref="output" name=o style="margin-left: 0.4em;"></output>
    </label>
  </form>
</template>

<script>
import {ref, onMounted} from 'vue'
export default {
  name: "TimeLine",
  props: {
    times: {
      type: Array
    }
  },
  setup(){
    let timeValues;
    const form = ref( null);
    const button = ref();
    const label = ref();
    const input = ref();
    const output = ref();
    onMounted(() => {
      console.dir(form.value);
    });
    function Scrubber(values, {
      format = value => value,
      initial = 0,
      delay = null,
      autoplay = true,
      loop = true,
      loopDelay = null,
      alternate = false
    } = {}) {
      console.log('hey');
      timeValues = Array.from(values);
      let frame = null;
      let timer = null;
      let interval = null;
      let direction = 1;
      function start() {
        button.textContent = "Pause";
        if (delay === null) frame = requestAnimationFrame(tick);
        else interval = setInterval(tick, delay);
      }
      function stop() {
        button.textContent = "Play";
        if (frame !== null) cancelAnimationFrame(frame), frame = null;
        if (timer !== null) clearTimeout(timer), timer = null;
        if (interval !== null) clearInterval(interval), interval = null;
      }
      function running() {
        return frame !== null || timer !== null || interval !== null;
      }
      function tick() {
        if (input.valueAsNumber === (direction > 0 ? values.length - 1 : direction < 0 ? 0 : NaN)) {
          if (!loop) return stop();
          if (alternate) direction = -direction;
          if (loopDelay !== null) {
            if (frame !== null) cancelAnimationFrame(frame), frame = null;
            if (interval !== null) clearInterval(interval), interval = null;
            timer = setTimeout(() => (step(), start()), loopDelay);
            return;
          }
        }
        if (delay === null) frame = requestAnimationFrame(tick);
        step();
      }
      function step() {
        input.valueAsNumber = (input.valueAsNumber + direction + values.length) % values.length;
        // input.dispatchEvent(new CustomEvent("input", {bubbles: true}));
      }
      input.oninput = event => {
        if (event && event.isTrusted && running()) stop();
        form.value = values[input.valueAsNumber];
        output.value = format(form.value, input.valueAsNumber, values);
      };
      button.onclick = () => {
        if (running()) return stop();
        direction = alternate && input.valueAsNumber === values.length - 1 ? -1 : 1;
        input.valueAsNumber = (input.valueAsNumber + direction) % values.length;
        // input.dispatchEvent(new CustomEvent("input", {bubbles: true}));
        start();
      };
      input.oninput();
      if (autoplay) start();
      else stop();
      // Inputs.disposal(form).then(stop);
    }
    Scrubber([1,2,3,4,5,6,7,8,9]);
    return {form,button,label,input,output};
  },
}
</script>

<style scoped>

</style>
