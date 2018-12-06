#!/usr/bin/env node

const fs = require('fs');

fs.readFile('./input.txt', 'utf8', function (err, data) {
    if (err) {
        throw err;
    }
    const nums = data.split('\n').filter(l => l !== '').map(n => parseInt(n, 10));
    console.log(`Part One: ${nums.reduce((a, c) => a + c, 0)}`);
    let c = 0;
    let i = 0;
    const seen = new Set([0]);
    while (true) {
        c += nums[i % nums.length];
        if (seen.has(c)) {
            console.log(`Part Two: ${c}`);
            break;
        }
        seen.add(c);
        i += 1;
    }
});
