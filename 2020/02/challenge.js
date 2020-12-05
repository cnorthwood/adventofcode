#!/usr/bin/env node

const fs = require("fs");

const input = fs
    .readFileSync("input.txt", "utf8")
    .split("\n")
    .map((line) => {
        const match = line.match(/(?<lower>\d+)-(?<upper>\d+) (?<char>\w): (?<password>\w+)/);
        if (!match) return null;
        return {
            lower: parseInt(match.groups.lower, 10),
            upper: parseInt(match.groups.upper, 10),
            char: match.groups.char,
            password: match.groups.password,
        };
    })
    .filter(line => line !== null);

function isValidPartOne(line) {
    const charsInPassword = Array.from(line.password).filter(c => c === line.char).length;
    return line.lower <= charsInPassword && charsInPassword <= line.upper;
}

function isValidPartTwo(line) {
    const inPosOne = line.password[line.lower - 1] === line.char;
    const inPosTwo = line.password[line.upper - 1] === line.char;
    return (inPosOne && !inPosTwo) || (!inPosOne && inPosTwo);
}

console.log(`Part One: ${input.reduce((a, line) => isValidPartOne(line) ? a + 1 : a, 0)}`)
console.log(`Part Two: ${input.reduce((a, line) => isValidPartTwo(line) ? a + 1 : a, 0)}`)
