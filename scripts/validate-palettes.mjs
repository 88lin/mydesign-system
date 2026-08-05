import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = path.resolve(import.meta.dirname, '..');
const cssPath = path.join(root, 'assets', 'palettes.css');
const source = fs.readFileSync(cssPath, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
const keys = 'ABCDEFGHIJ'.split('');
const palettes = Object.fromEntries(keys.map(key => [key, {}]));

function declarations(body) {
  const result = {};
  const pattern = /(--[\w-]+)\s*:\s*([^;]+);/g;
  let match;
  while ((match = pattern.exec(body))) result[match[1]] = match[2].trim();
  return result;
}

const rulePattern = /([^{}]+)\{([^{}]*)\}/g;
let rule;
while ((rule = rulePattern.exec(source))) {
  const selectors = rule[1].split(',').map(value => value.trim());
  const values = declarations(rule[2]);
  const targets = new Set();

  if (selectors.includes(':root') || selectors.includes('[data-palette]')) {
    keys.forEach(key => targets.add(key));
  }
  for (const selector of selectors) {
    const match = selector.match(/^\[data-palette=["']([A-J])["']\]$/);
    if (match) targets.add(match[1]);
  }
  targets.forEach(key => Object.assign(palettes[key], values));
}

function resolve(key, name, seen = new Set()) {
  if (seen.has(name)) throw new Error(`${key}: circular token reference at ${name}`);
  const raw = palettes[key][name];
  if (!raw) return '';
  const nextSeen = new Set(seen).add(name);
  return raw.replace(/var\((--[\w-]+)(?:,[^)]+)?\)/g, (_, reference) => resolve(key, reference, nextSeen)).trim();
}

function rgb(value) {
  const normalized = value.trim();
  if (/^#[\da-f]{6}$/i.test(normalized)) {
    return [1, 3, 5].map(index => Number.parseInt(normalized.slice(index, index + 2), 16));
  }
  if (/^#[\da-f]{3}$/i.test(normalized)) {
    return normalized.slice(1).split('').map(channel => Number.parseInt(channel + channel, 16));
  }
  return null;
}

function luminance(value) {
  const channels = rgb(value);
  if (!channels) throw new Error(`Unsupported contrast color: ${value}`);
  const linear = channels.map(channel => {
    const normalized = channel / 255;
    return normalized <= 0.03928 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
  });
  return linear[0] * 0.2126 + linear[1] * 0.7152 + linear[2] * 0.0722;
}

function contrast(foreground, background) {
  const a = luminance(foreground);
  const b = luminance(background);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

const required = [
  '--brand-primary', '--brand-primary-deep', '--brand-primary-soft', '--brand-primary-rgb',
  '--brand-accent', '--brand-accent-soft', '--brand-accent-rgb',
  '--brand-pop', '--brand-pop-deep', '--brand-pop-soft', '--brand-pop-rgb',
  '--brand', '--brand-deep', '--brand-text', '--brand-surface', '--brand-border', '--brand-on-dark', '--brand-rgb',
  '--highlight', '--highlight-soft', '--highlight-rgb',
  '--pop', '--pop-deep', '--pop-text', '--pop-surface', '--pop-soft', '--pop-rgb',
  '--cream', '--cream-dark', '--card-bg', '--ink', '--ink-light', '--ink-faint', '--ink-rgb', '--dark-panel',
  '--border', '--hairline', '--on-brand', '--on-highlight', '--on-pop', '--on-dark', '--on-dark-dim',
  '--success', '--success-soft', '--warning', '--warning-soft', '--danger', '--danger-strong', '--danger-soft',
  '--info', '--info-soft', '--border-strong', '--focus-ring', '--highlighter'
];

const checks = [
  ['--brand-text', '--cream', 4.5, 'brand text / page'],
  ['--on-brand', '--brand-surface', 4.5, 'foreground / brand surface'],
  ['--pop-text', '--cream', 4.5, 'accent text / page'],
  ['--on-pop', '--pop-surface', 4.5, 'foreground / accent surface'],
  ['--ink', '--cream', 4.5, 'body / page'],
  ['--ink-light', '--cream', 4.5, 'secondary text / page'],
  ['--ink-faint', '--cream', 4.5, 'metadata / page'],
  ['--on-highlight', '--highlight', 4.5, 'foreground / highlight'],
  ['--on-dark', '--dark-panel', 4.5, 'body / dark panel'],
  ['--on-dark-dim', '--dark-panel', 4.5, 'secondary text / dark panel'],
  ['--brand-on-dark', '--dark-panel', 4.5, 'brand hint / dark panel'],
  ['--brand-border', '--cream', 3, 'brand border / page'],
  ['--success', '--success-soft', 4.5, 'success text / success surface'],
  ['--warning', '--warning-soft', 4.5, 'warning text / warning surface'],
  ['--danger-strong', '--danger-soft', 4.5, 'danger text / danger surface'],
  ['--info', '--cream', 4.5, 'information text / page'],
  ['--focus-ring', '--cream', 3, 'focus ring / page'],
  ['--brand', '--cream', 3, 'display brand / page'],
  ['--pop', '--cream', 3, 'decorative accent / page']
];

const failures = [];
for (const key of keys) {
  for (const token of required) {
    if (!resolve(key, token)) failures.push(`${key}: missing ${token}`);
  }

  for (const [colorToken, channelToken] of [['--brand', '--brand-rgb'], ['--highlight', '--highlight-rgb'], ['--pop', '--pop-rgb'], ['--ink', '--ink-rgb']]) {
    const color = rgb(resolve(key, colorToken));
    const channels = resolve(key, channelToken).split(',').map(value => Number(value.trim()));
    if (!color || channels.length !== 3 || color.some((value, index) => value !== channels[index])) {
      failures.push(`${key}: ${channelToken} does not match ${colorToken}`);
    }
  }

  const results = checks.map(([foreground, background, minimum, label]) => {
    const value = contrast(resolve(key, foreground), resolve(key, background));
    if (value + Number.EPSILON < minimum) {
      failures.push(`${key}: ${label} ${value.toFixed(2)}:1 < ${minimum}:1`);
    }
    return value;
  });
  const lowest = Math.min(...results);
  console.log(`${key}  ${checks.length} checks  lowest ${lowest.toFixed(2)}:1`);
}

if (failures.length) {
  console.error(`\nPalette validation failed (${failures.length}):`);
  failures.forEach(failure => console.error(`- ${failure}`));
  process.exitCode = 1;
} else {
  console.log(`\nPassed: ${keys.length} palettes, ${keys.length * checks.length} contrast checks, RGB channels synchronized.`);
}
