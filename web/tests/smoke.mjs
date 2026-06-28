import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const dom = new JSDOM(html);

if (!dom.window.document.querySelector('[data-page="dashboard"]')) {
  throw new Error('Dashboard page is missing its page marker');
}

if (!dom.window.document.querySelector('[data-overview-summary]')) {
  throw new Error('Dashboard page is missing the overview summary host');
}

if (!dom.window.document.querySelector('#operations')) {
  throw new Error('Dashboard page is missing the operations section');
}

if (!dom.window.document.querySelector('#impact')) {
  throw new Error('Dashboard page is missing the impact section');
}

if (!dom.window.document.querySelector('[data-project-picker]')) {
  throw new Error('Dashboard page is missing the project picker');
}

const settingsHtml = readFileSync(new URL('../settings.html', import.meta.url), 'utf8');
if (!settingsHtml.includes('data-page="settings"')) {
  throw new Error('Settings page is missing its page marker');
}

const reportHtml = readFileSync(new URL('../report.html', import.meta.url), 'utf8');
if (reportHtml.includes('reports/latest.pdf')) {
  throw new Error('Report page must not ship a hard-coded PDF link');
}

const appSource = readFileSync(new URL('../src/app.js', import.meta.url), 'utf8');
for (const expected of [
  'report-status.json',
  'data-pdf-download',
  'reportStatus.project_id === data.project?.id',
  'API key invalid',
  'last successful collection: ${lastSuccess',
  'renderProjectConfig',
  "page === 'dashboard'",
  'data/projects.json',
  'data-project-picker',
  'resolveProjectId'
]) {
  if (!appSource.includes(expected)) {
    throw new Error(`App source is missing ${expected}`);
  }
}

for (const expected of [
  'renderSecurityHealth',
  'renderAdoptionMatrix',
  'renderCommunityStandards',
  'renderGovernanceHealth',
  'renderContributorDiversity',
  'renderTargetsProgress'
]) {
  if (!appSource.includes(expected)) {
    throw new Error(`UI render function is missing: ${expected}`);
  }
}

for (const expected of [
  'securityHealth',
  'adoptionMatrix',
  'communityStandards',
  'governanceHealth',
  'contributorDiversity',
  'targetsProgress'
]) {
  if (!settingsHtml.includes(expected)) {
    throw new Error(`Settings page is missing section: ${expected}`);
  }
}

console.log('frontend smoke ok');
