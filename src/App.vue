<template>
  <div id="app">
    <h1>Splatoon2 Weapons Quiz</h1>
    <router-view/>
  </div>
</template>

<style lang="scss">
body {
  margin: 0;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
h1 {
  font-size: 1.0rem;
  text-align: left;
  padding: 6px 0.4rem;
  margin: 0 0 20px;
  background-color: #ddd;
}
</style>
