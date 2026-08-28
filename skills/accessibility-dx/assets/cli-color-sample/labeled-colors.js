#!/usr/bin/env node
// Clean fixture: color always pairs with a text marker.
// The severity word carries the meaning; color is additive.
const chalk = require("chalk");

function emitError(code) {
  process.stderr.write(chalk.red(`ERROR: request ${code} failed`));
}

function emitSuccess(count) {
  process.stdout.write(`\x1b[32mSUCCESS: ${count} checks passed\x1b[0m\n`);
}

module.exports = { emitError, emitSuccess };
