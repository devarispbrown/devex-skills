#!/usr/bin/env node
// Defect fixture: severity is carried by chalk.red alone.
// There is no severity word on the line that emits it, so the meaning is
// visible only to people who see the color.
const chalk = require("chalk");

function emitError(code) {
  process.stderr.write(chalk.red(`request ${code}`));
}

module.exports = { emitError };
