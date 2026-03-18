#!/usr/bin/env node
const os = require("os");
console.log(JSON.stringify({
  name: "ENVR Node probe",
  node: process.version,
  platform: os.platform(),
  arch: os.arch(),
  homedir: os.homedir(),
}, null, 2));
