<template>
  <div id="cursor-container">
    <div class="border"></div>
    <div class="dot"></div>
    <div id="overlay-box" v-if="showOverlay">
      <span></span>
      <div class="description"></div>
      <div class="value"></div>
    </div>
  </div>
</template>

<script>
import anime from "animejs/lib/anime.es.js";

export default {
  data() {
    return {
      mouseMoved: false,
      border: null,
      overlayBox: null,
      showOverlay: true,
      dot: null,
      speed: 0.2,
      cursor: { x: 0, y: 0 },
      velocity: { x: 0, y: 0 },
    };
  },
  computed: {
    computeSize: () => {
      return window.screen.availWidth * 0.015;
    },
  },
  mounted() {
    const container = document.getElementById("cursor-container");
    this.border = container.querySelector(".border");
    this.dot = container.querySelector(".dot");
    this.overlayBox = container.querySelector("#overlay-box");
    this.border.style.width = this.computeSize + "px";
    this.border.style.height = this.computeSize + "px";
    this.dot.style.width = this.computeSize * 0.2 + "px";
    this.dot.style.height = this.computeSize * 0.2 + "px";
    this.overlayBox.style.width = "min-content";

    this.dot.style.opacity = "0";
    this.border.style.opacity = "0";
    this.overlayBox.style.opacity = "0";
    this.animate();
    window.addEventListener("mousemove", this.move_cursor);
  },
  methods: {
    move_cursor(ev) {
      let container = document.getElementById("cursor-container");
      if (container.classList.contains("entered"))
        container.style.display = "block";
      this.velocity.x = ev.clientX;
      this.velocity.y = ev.clientY;
      this.dot.style.left = ev.clientX + "px";
      this.dot.style.top = ev.clientY + "px";
      this.overlayBox.style.left = ev.clientX + "px";
      this.overlayBox.style.top = ev.clientY + "px";

      anime({
        targets: "#cursor-container .border",
        transform: "translate",
      });
      if (!this.mouseMoved) {
        this.dot.style.opacity = "1.0";
        this.border.style.opacity = "1.0";
        this.overlayBox.style.opacity = "1.0";
        anime({
          targets: "#cursor-container .border",
          opacity: ["0.0", "1.0"],
          borderRadius: ["0%", "50%"],
          easing: "easeInOutQuad",
          duration: 500,
        });
        anime({
          targets: "#cursor-container .dot",
          opacity: ["0.0", "1.0"],
          easing: "easeInOutQuad",
          duration: 500,
        });
        /*anime({
                    targets: '#cursor-container #overlay-box',
                    opacity: ['0.0', '1.0'],
                    backgroundColor: [getComputedStyle(document.documentElement).getPropertyValue('--content') + '00', getComputedStyle(document.documentElement).getPropertyValue('--content') + 'FF'],
                    easing: 'easeInOutQuad',
                    duration: 500,
                });*/
        this.mouseMoved = true;
      }
    },
    animate() {
      this.cursor.x += (this.velocity.x - this.cursor.x) * this.speed;
      this.cursor.y += (this.velocity.y - this.cursor.y) * this.speed;

      this.border.style.left = this.cursor.x + "px";
      this.border.style.top = this.cursor.y + "px";

      requestAnimationFrame(this.animate);
    },
  },
};
</script>

<style lang="scss" scoped>
#cursor-container {
  display: none;
  position: static;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  pointer-events: none;

  & .border {
    position: fixed;
    z-index: 1000;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    border: 2px solid black;
    transform: translate(-50%, -50%);

    transition: opacity 1s easeOut;

    pointer-events: none;
  }

  & .dot {
    position: fixed;
    z-index: 1001;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    background-color: #0d0d19;
    transform: translate(-50%, -50%);

    transition: opacity 1s easeOut;

    pointer-events: none;
  }
  & #overlay-box {
    position: fixed;
    z-index: 999;
    top: 50%;
    left: 50%;
    background-color: var(--overlay-box);
    transform: translate(-125%, -50%);
    // transform: scale(0.5);

    padding: 2vh 2.2vh;
    border-radius: 2vh;

    min-width: 20em;

    // transition: opacity 1s easeOut;
    opacity: 0;

    pointer-events: none;

    & span {
      color: var(--overlay-box-content);
      font-size: 1.6rem;
      font-weight: 700;
      white-space: nowrap;
      text-align: center;
      display: block;
      margin-bottom: 1rem;
    }
    & div {
      text-align: center;
      font-size: 1.2em;
    }
    & .value {
      font-weight: 700;
    }
  }
}
</style>