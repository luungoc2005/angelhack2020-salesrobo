const puppeteer = require('puppeteer');
const qs = require('qs');
const fs = require('fs');
const uuid = require('uuid');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 250 // slow down by 250ms
  });
  const page = await browser.newPage();

  const keyword = 'smartphone';
  const MAX_COMMENTS = 500;

  
})