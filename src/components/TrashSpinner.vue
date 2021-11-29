<template>
  <div id="trash-spinner" class="line-scale">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>

<style lang="scss" scoped>
$primary-color: var(--primary-color) !default;
$ball-size: 15px !default;
$margin: 2px !default;
$line-height: 20px !default;
$line-width: 3px !default;

@function delay($interval, $count, $index) {
  @return ($index * $interval) - ($interval * $count);
}

@mixin global-animation() {
  animation-fill-mode: both;
}
@mixin lines() {
  width: $line-width;
  height: $line-height;
  border-radius: 2px;
  margin: $margin;
  background-color: $primary-color;
}

@keyframes line-scale {
  0% {
    transform: scaley(1);
  }
  50% {
    transform: scaley(0.4);
  }
  100% {
    transform: scaley(1);
  }
}

@mixin line-scale($n: 5) {
  @for $i from 1 through $n {
    > div:nth-child(#{$i}) {
      animation: line-scale
        1s
        delay(0.1s, $n, $i)
        infinite
        cubic-bezier(0.2, 0.68, 0.18, 1.08);
    }
  }
}

.line-scale {
  @include line-scale();
  width: max-content;
  margin: auto;

  > div {
    @include lines();
    @include global-animation();

    display: inline-block;
  }
}
</style>